from fastapi import APIRouter
from collections import Counter

candidates = [
    {
        "id": 1,
        "job_title": "Backend Engineer",
        "stage": "first",
        "rejected_reason": None,
    },
    {
        "id": 2,
        "job_title": "Backend Engineer",
        "stage": "rejected",
        "rejected_reason": "skill_mismatch",
    },
    {
        "id": 3,
        "job_title": "Frontend Engineer",
        "stage": "second",
        "rejected_reason": None,
    },
    {
        "id": 4,
        "job_title": "Backend Engineer",
        "stage": "hired",
        "rejected_reason": None,
    },
    {
        "id": 5,
        "job_title": "Data Scientist",
        "stage": "rejected",
        "rejected_reason": "culture_fit",
    },
]

router = APIRouter()

@router.get("/stage-summary")
async def stage_summary():
    total = len(candidates)

    # define the order of hiring
    hiring_order = [
        "applied", "screening", "first", "second", "offer", "hired", "rejected"
    ]

    # count per stages
    # stage_counts = {s: 0 for s in hiring_order}
    # for c in candidates:
    #     s = c["stage"]
    #     if s in stage_counts:
    #         stage_counts[s] += 1

    # functional programing
    # stages_only = map(lambda c: c["stage"], candidates) # execute lambda per candidate
    # stage_counts = Counter(stages_only) # count
    stage_counts = Counter(c["stage"] for c in candidates)

    stages = [
        {
            "stage": s,
            "count": stage_counts[s],
            "rate": stage_counts[s] / total if total else 0
        }
        for s in hiring_order
    ]

    return {
        "total_applicants": total,
        "stages": stages
    }


@router.get("/rejection-reasons")
def get_rejection_reasons():
    rejected = [c for c in candidates if c["stage"] == "rejected"]
    total_rejected = len(rejected)

    # reason_counts = {}
    # for c in rejected:
    #     r = c["rejected_reason"] or "other"
    #     reason_counts[r] = reason_counts.get(r, 0) + 1

    # functional programing
    # reason_only = map(lambda c: c["rejected_reason"] or "other", rejected)
    # reason_counts = Counter(reason_only) 
    reason_counts = Counter(c["rejected_reason"] or "other" for c in rejected)

    reasons = [
        {
            "reason": r,
            "count": cnt,
            "rate": cnt / total_rejected if total_rejected else 0
        }
        for r, cnt in reason_counts.items()
    ]

    return {
        "total_rejected": total_rejected,
        "reasons": reasons
    }