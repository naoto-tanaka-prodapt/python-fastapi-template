import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";

export async function clientLoader({context} : Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  if (!isAdmin){
    return redirect("/admin-login")
  }
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    await fetch('/api/job-applications', {
        method: 'POST',
        body: formData
    })
    return redirect('/job-applications')
}

export default function NewJobApplicationForm(_: Route.ComponentProps) {
  return (
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
  );
}