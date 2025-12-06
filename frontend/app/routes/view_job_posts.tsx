import { Form, Link, useNavigation } from "react-router";
import { Button } from "~/components/ui/button";
import type { Route } from "../+types/root";
import { userContext } from "~/context";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Input } from "~/components/ui/input";

export async function clientLoader({ params, context }: Route.ClientLoaderArgs) {
  const me = context.get(userContext);
  const isAdmin = me && me.is_admin;

  const jobPostId = params.jobPostId;
  const res = await fetch(`/api/job-posts/${jobPostId}`);
  const jobPost = await res.json();
  return { jobPost, isAdmin };
}

export async function clientAction({ request }: Route.ClientActionArgs) {
  const formData = await request.formData();
  const jobPostId = formData.get("job_post_id");

  const response = await fetch(`/api/job-posts/${jobPostId}/recommend`);
  if (!response.ok) {
    return null;
  }
  const recommendedApplicant = await response.json();
  return { recommendedApplicant };
}

export default function ViewJobPosts({ loaderData, actionData }: Route.ComponentProps) {
  const { job_post: jobPost, job_applications: jobApplications } = loaderData.jobPost;
  const navigation = useNavigation();
  const isRecommendationLoading = navigation.state === "submitting";

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 space-y-8">
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col gap-6 p-6 md:flex-row md:items-start">
          <div className="flex-1 space-y-4">
            <p className="text-sm font-semibold text-blue-600">Job #{jobPost.id}</p>
            <h1 className="text-3xl font-semibold text-slate-900">{jobPost.title}</h1>
            <p className="text-base leading-relaxed text-slate-700">{jobPost.description}</p>
          </div>
          <div className="md:w-52">
            <Button className="w-full" disabled={loaderData.isAdmin}>
              <Link to={`/job-applications/new?jobPostId=${jobPost.id}`}>Apply Now</Link>
            </Button>
          </div>
        </div>
      </div>

      {loaderData.isAdmin && (
        <>
          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 bg-slate-50 px-6 py-4">
              <div>
                <h2 className="text-base font-semibold text-slate-900">Applicants</h2>
                <p className="text-sm text-slate-500">{jobApplications.length} application(s) received</p>
              </div>
              <Form method="post">
                <Input id="job_post_id" name="job_post_id" type="hidden" value={jobPost.id}/>
                <Button className="min-w-[180px]" variant="outline" type="submit" disabled={isRecommendationLoading}>
                  {isRecommendationLoading ? "Loading..." : "Show Recommendation"}
                </Button>
              </Form>
            </div>
            {jobApplications.length > 0 ? (
              <div className="relative overflow-x-auto">
                <Table className="w-full mx-4">
                  <TableHeader>
                    <TableRow className="bg-white">
                      <TableHead className="w-64 text-slate-600">Name</TableHead>
                      <TableHead className="w-72 text-slate-600">Email</TableHead>
                      <TableHead className="text-slate-600">Resume</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {jobApplications.map((jobApplication) => (
                      <TableRow key={jobApplication.id} className="hover:bg-slate-50/80 transition">
                        <TableCell className="py-4 font-medium">
                          {jobApplication.first_name} {jobApplication.last_name}
                        </TableCell>
                        <TableCell className="py-4 text-sm text-slate-700">{jobApplication.email}</TableCell>
                        <TableCell className="py-4">
                          <a
                            href={jobApplication.resume_path}
                            className="text-sm font-medium text-blue-600 hover:underline"
                            target="_blank"
                            rel="noreferrer"
                          >
                            View Resume
                          </a>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <div className="px-6 py-8 text-center text-sm text-slate-500">No applications yet.</div>
            )}
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-100 bg-slate-50 px-6 py-3">
              <h2 className="text-base font-semibold text-slate-900">Recommendation</h2>
            </div>
            <div className="space-y-3 px-6 py-5">
              { actionData && actionData.recommendedApplicant ? (
                <>
                  <div className="text-lg font-semibold text-slate-900">
                    {actionData.recommendedApplicant.first_name} {actionData.recommendedApplicant.last_name}
                  </div>
                  <p className="text-sm text-slate-600">{actionData.recommendedApplicant.email}</p>
                  <a
                    href={actionData.recommendedApplicant.resume_path}
                    className="text-sm font-medium text-blue-600 hover:underline"
                    target="_blank"
                    rel="noreferrer"
                  >
                    View Resume
                  </a>
                </>
              ) : (
                <p className="text-sm text-slate-600">Click "Show Recommendation" to see a suggested applicant.</p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
