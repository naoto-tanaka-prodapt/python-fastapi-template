from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
EVAL_CSV_PATH = BASE_DIR.parent / "test" / "eval.output.csv"
ANNOTATIONS_PATH = BASE_DIR / "data" / "annotations.json"


def load_eval_rows() -> List[Dict[str, str]]:
    """Load eval samples from the CSV file."""
    if not EVAL_CSV_PATH.exists():
        raise FileNotFoundError(f"Eval CSV not found at {EVAL_CSV_PATH}")

    rows: List[Dict[str, str]] = []
    with EVAL_CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        # Skip header row; first column is an index placeholder
        next(reader, None)
        for raw in reader:
            if not raw:
                continue
            # Pad any short rows to expected length
            while len(raw) < 5:
                raw.append("")
            row_id = raw[0] or str(len(rows))
            rows.append(
                {
                    "id": row_id,
                    "job_description": raw[1],
                    "summary": raw[2],
                    "fixed_description": raw[3],
                    "fb": raw[4],
                }
            )
    return rows


def load_annotations() -> Dict[str, Dict[str, str]]:
    """Load saved annotations from disk."""
    if not ANNOTATIONS_PATH.exists():
        return {}
    try:
        return json.loads(ANNOTATIONS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # Corrupt or empty file fallback
        return {}


def save_annotations(annotations: Dict[str, Dict[str, str]]) -> None:
    """Persist annotations to disk."""
    ANNOTATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ANNOTATIONS_PATH.write_text(
        json.dumps(annotations, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_next_unannotated_id(
    records: List[Dict[str, str]],
    annotations: Dict[str, Dict[str, str]],
    current_id: Optional[str] = None,
) -> Optional[str]:
    """Return the next unannotated sample id, scanning after current_id first."""
    start = 0
    if current_id is not None:
        for idx, record in enumerate(records):
            if record["id"] == current_id:
                start = idx + 1
                break
    for record in records[start:]:
        if record["id"] not in annotations:
            return record["id"]
    for record in records[:start]:
        if record["id"] not in annotations:
            return record["id"]
    return None


app = FastAPI(title="Eval UI")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/")
def index(request: Request):
    records = load_eval_rows()
    annotations = load_annotations()
    total = len(records)
    done = len(annotations)
    remaining = total - done
    next_id = get_next_unannotated_id(records, annotations)

    # Build a light summary for the table
    summary_rows = [
        {
            "id": r["id"],
            "job_description": r["job_description"],
            "annotated": r["id"] in annotations,
            "verdict": annotations.get(r["id"], {}).get("verdict"),
        }
        for r in records
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "total": total,
            "done": done,
            "remaining": remaining,
            "next_id": next_id,
            "rows": summary_rows,
        },
    )


@app.get("/sample/{item_id}")
def sample(request: Request, item_id: str):
    records = load_eval_rows()
    annotations = load_annotations()
    record = next((r for r in records if r["id"] == item_id), None)
    if record is None:
        raise HTTPException(status_code=404, detail="Sample not found")

    total = len(records)
    done = len(annotations)
    remaining = total - done
    next_id = get_next_unannotated_id(records, annotations, current_id=item_id)

    return templates.TemplateResponse(
        "sample.html",
        {
            "request": request,
            "record": record,
            "annotation": annotations.get(item_id),
            "total": total,
            "done": done,
            "remaining": remaining,
            "next_id": next_id,
        },
    )


@app.post("/sample/{item_id}")
def annotate_sample(
    item_id: str,
    verdict: str = Form(...),
    reason: str = Form(""),
):
    verdict = verdict.lower()
    if verdict not in {"pass", "fail"}:
        raise HTTPException(status_code=400, detail="Invalid verdict")
    if verdict == "fail" and not reason.strip():
        raise HTTPException(status_code=400, detail="Please provide a reason for fail")

    records = load_eval_rows()
    if not any(r["id"] == item_id for r in records):
        raise HTTPException(status_code=404, detail="Sample not found")

    annotations = load_annotations()
    annotations[item_id] = {"verdict": verdict, "reason": reason.strip()}
    save_annotations(annotations)

    next_id = get_next_unannotated_id(records, annotations, current_id=item_id)
    if next_id:
        return RedirectResponse(f"/sample/{next_id}", status_code=303)
    return RedirectResponse("/", status_code=303)
