import { Link, useFetcher } from "react-router";
import type { Route } from "../+types/root";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Button } from "~/components/ui/button";

export async function clientLoader() {
  const res = await fetch(`/api/job-applications`);
  const jobApplications = await res.json();
  return {jobApplications}
}

export async function clientAction({ request }: Route.ClientActionArgs) {
  const formData = await request.formData()
  const jobApplicationId = formData.get('job_application_id')
  await fetch(`/api/job-applications/${jobApplicationId}`, {
      method: 'DELETE'
  })
}

export default function JobApplications({ loaderData }: Route.ComponentProps) {
  const fetcher = useFetcher()

  return (
    <>
    <Button className="">
      <Link to="/job-applications/new">Add New Job Application</Link>
    </Button>
    <Table className="w-1/2">
      <TableHeader>
        <TableRow>
          <TableHead>Job Post ID</TableHead>
          <TableHead>First Name</TableHead>
          <TableHead>Last Name</TableHead>
          <TableHead>Email</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {loaderData.jobApplications.map(
          (jobApplication) => 
            <TableRow key={jobApplication.id}>
              <TableCell>{jobApplication.job_post_id}</TableCell>
              <TableCell>{jobApplication.first_name}</TableCell>
              <TableCell>{jobApplication.last_name}</TableCell>
              <TableCell>{jobApplication.email}</TableCell>
              <TableCell>
                <Link to={`/job-applications/${jobApplication.id}/edit`}>Edit</Link>
                <fetcher.Form method="post"
                  onSubmit={(event) => {
                    const response = confirm(
                      `Please confirm you want to delete this job board '${jobApplication.first_name} ${jobApplication.last_name}'.`,
                    );
                    if (!response) {
                      event.preventDefault();
                    }
                  }}
                >
                  <input name="job_application_id" type="hidden" value={jobApplication.id}></input>
                  <button>Delete</button>
                </fetcher.Form>
              </TableCell>
            </TableRow>
        )}
      </TableBody>
    </Table>
    </>
  )
}