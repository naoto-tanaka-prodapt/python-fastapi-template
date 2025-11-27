import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";

export async function clientLoader({params, context} : Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  if (!isAdmin){
    return redirect("/admin-login")
  }

  const jobApplicationId = params.jobApplicationId;
  const res = await fetch(`/api/job-applications/${jobApplicationId}`);
  const jobApplication = await res.json();
  return {jobApplication}
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    const jobApplicationId = formData.get('job_application_id')
    await fetch(`/api/job-applications/${jobApplicationId}`, {
        method: 'PUT',
        body: formData
    })
    return redirect('/job-applications')
}

export default function EditJobApplicationForm({ loaderData }: Route.ComponentProps) {
  const job_application_id = loaderData.jobApplication.id;
  const job_post_id = loaderData.jobApplication.job_post_id;
  const first_name = loaderData.jobApplication.first_name ?? "";
  const last_name = loaderData.jobApplication.last_name ?? "";
  const email = loaderData.jobApplication.email ?? "";

  return (
    <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
        <FieldGroup>
          <FieldLegend>Edit Job Application</FieldLegend>
          <Field>
            <FieldLabel htmlFor="job_post_id">
              Job Post ID
            </FieldLabel>
            <Input
              id="job_post_id"
              name="job_post_id"
              defaultValue={job_post_id}
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
              defaultValue={first_name}
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
              defaultValue={last_name}
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
              defaultValue={email}
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
          <Input id="job_application_id" name="job_application_id" type="hidden" value={job_application_id}/>
        </FieldGroup>
      </Form>
    </div>
  );
}