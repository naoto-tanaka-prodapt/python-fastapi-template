import { Form, Link, redirect } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";
import { Textarea } from "~/components/ui/textarea";
import { useState } from "react";

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
    const reviewed = formData.get("reviewed")
    if (reviewed == "false"){
      const response = await fetch('/api/review-job-description', {
        method: 'POST',
        body: formData
      })
      const reviewResponse = await response.json()
      return { reviewResponse }
    } else {
      await fetch('/api/job-posts', {
        method: 'POST',
        body: formData
      })
      const job_board_id = formData.get("job_board_id")
      return redirect(`/job-boards/${job_board_id}/job-posts`)
    }
    
}

export default function NewJobPostForm({loaderData, actionData}: Route.ComponentProps) {
  const [reviewed, setReviewed] = useState("false")
  const [summary, setSummary] = useState("")
  if (actionData && actionData.reviewResponse && reviewed === "false"){
    setReviewed("true")
    setSummary(actionData.reviewResponse.overall_summary)
  }

  return (
    <main className="min-h-[200px] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Form method="post" encType="multipart/form-data">
          <FieldGroup>
            <FieldLegend className="text-center">Add New Job</FieldLegend>
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
              <Textarea
                id="description"
                name="description"
                placeholder="Engineer for AI"
                required
              />
            </Field>
            <Input id="job_board_id" name="job_board_id" type="hidden" value={loaderData.jobBoardId}/>
            <Input id="reviewed" name="reviewed" type="hidden" value={reviewed}/>
            {
              summary && (
                <div className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-900">
                  <p className="whitespace-pre-wrap">{summary}</p>
                </div>
              )
            }
            <div className="float-right">
              <Field orientation="horizontal">
                <Button type="submit">{ reviewed === "false" ? "Review" : "Submit"}</Button>
                <Button variant="outline" type="button">
                  <Link to={`/job-boards/${loaderData.jobBoardId}/job-posts`}>Cancel</Link>
                </Button>
              </Field>
            </div>
          </FieldGroup>
        </Form>
      </div>
    </main>
  );
}