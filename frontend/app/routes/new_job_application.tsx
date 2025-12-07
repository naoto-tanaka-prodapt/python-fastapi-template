import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";

export async function clientLoader({ request }: Route.ClientLoaderArgs) {
  const url = new URL(request.url)
  const jobPostId = url.searchParams.get("jobPostId")

  return { jobPostId }
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    await fetch('/api/job-applications', {
        method: 'POST',
        body: formData
    })
    return redirect(`/job-posts/${formData.get("job_post_id")}`)
}

export default function NewJobApplicationForm({ loaderData }: Route.ComponentProps) {
  return (
    <main className="min-h-[200px] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Form method="post" encType="multipart/form-data">
          <FieldGroup>
            <FieldLegend>Add New Job Application</FieldLegend>
            <Field>
              <FieldLabel htmlFor="job_post_id">
                Job Post ID
              </FieldLabel>
              <Input
                id="job_post_id"
                name="job_post_id"
                placeholder="1"
                defaultValue={loaderData && loaderData.jobPostId ? loaderData.jobPostId : ""}
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="first_name">
                First Name
              </FieldLabel>
              <Input
                id="first_name"
                name="first_name"
                placeholder="Samantha"
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="last_name">
                Last Name
              </FieldLabel>
              <Input
                id="last_name"
                name="last_name"
                placeholder="Lee"
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="email">
                Email
              </FieldLabel>
              <Input
                id="email"
                name="email"
                placeholder="dummy@example.com"
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="resume">
                Resume
              </FieldLabel>
              <Input
                id="resume"
                name="resume"
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
          </FieldGroup>
        </Form>
      </div>
    </main>
  );
}