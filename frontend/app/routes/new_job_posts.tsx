import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";

export async function clientLoader({context, params} : Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  if (!isAdmin){
    return redirect("/admin-login")
  }

  const jobBoardId = params.companyId;
  return { jobBoardId }
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    await fetch('/api/job-posts', {
        method: 'POST',
        body: formData
    })
    debugger
    const job_board_id = formData.get("job_board_id")
    return redirect(`/job-boards/${job_board_id}/job-posts`)
}

export default function NewJobPostForm({loaderData}: Route.ComponentProps) {
  return (
    <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
        <FieldGroup>
          <FieldLegend>Add New Job</FieldLegend>
          <Field>
            <FieldLabel htmlFor="title">
              Job Name
            </FieldLabel>
            <Input
              id="title"
              name="title"
              placeholder="AI Engineer"
              required
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="description">
              Job Description
            </FieldLabel>
            <Input
              id="description"
              name="description"
              placeholder="Engineer for AI"
              required
            />
          </Field>
          <Input id="job_board_id" name="job_board_id" type="hidden" value={loaderData.jobBoardId}/>
          <div className="float-right">
            <Field orientation="horizontal">
              <Button type="submit">Submit</Button>
              <Button variant="outline" type="button">
                <Link to={`/job-boards/${loaderData.jobBoardId}/job-posts`}>Cancel</Link>
              </Button>
            </Field>
          </div>
        </FieldGroup>
      </Form>
    </div>
  );
}