import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { useSearchParams } from "react-router";

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    const jobBoardId = formData.get('job_board_id')
    await fetch(`/api/job-boards/${jobBoardId}`, {
        method: 'PUT',
        body: formData
    })
    return redirect('/job-boards')
}

export default function EditJobBoardForm(_: Route.ComponentProps) {
  const [searchParams] = useSearchParams();

  const job_board_id = searchParams.get("id") ?? "";
  const slug = searchParams.get("slug") ?? "";
  const logo_path = searchParams.get("logo");

  return (
    <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
        <FieldGroup>
          <FieldLegend>Edit Job Board</FieldLegend>
          { logo_path && <img src={logo_path} alt="logo"/>}
          <Field>
            <FieldLabel htmlFor="slug">
              Slug
            </FieldLabel>
            <Input
              id="slug"
              name="slug"
              value={slug}
              required
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="logo">
              Logo
            </FieldLabel>
            <Input
              id="logo"
              name="logo"
              type="file"
              required
            />
          </Field>
          <div className="float-right">
            <Field orientation="horizontal">
              <Button type="submit">Submit</Button>
              <Button variant="outline" type="button">
                <Link to="/job-boards">Cancel</Link>
              </Button>
            </Field>
          </div>
          <Input id="job_board_id" name="job_board_id" type="hidden" value={job_board_id}/>
        </FieldGroup>
      </Form>
    </div>
  );
}