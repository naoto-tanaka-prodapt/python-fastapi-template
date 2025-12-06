import { Link } from "react-router";
import { Button } from "~/components/ui/button";
import type { Route } from "../+types/root";
import { userContext } from "~/context";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";


export async function clientLoader({params, context}: Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  
  const company_id = params.companyId;
  const res = await fetch(`/api/job-boards/${company_id}/job-posts`);
  const jobPosts = await res.json();
  return {jobPosts, isAdmin, company_id}
}

export default function JobPosts({loaderData}: Route.ComponentProps) {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10 space-y-6">
      { loaderData.isAdmin ? (
        <div className="flex justify-end">
          <Button>
            <Link to={`/job-boards/${loaderData.company_id}/add-job`}>Add New Job</Link>
          </Button>
        </div>
      ): <></>}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <Table className="w-full table-fixed">
          <TableHeader>
            <TableRow className="bg-slate-50">
              <TableHead className="w-64 text-slate-600">Title</TableHead>
              <TableHead className="text-slate-600">Description</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loaderData.jobPosts.map((jobPost) => (
              <TableRow key={jobPost.id ?? jobPost.title} className="hover:bg-slate-50/80 transition">
                <TableCell className="py-4 font-medium w-64 max-w-xs">
                  <span className="line-clamp-1" title={jobPost.title}>{jobPost.title}</span>
                </TableCell>
                <TableCell className="py-4">
                  <span className="text-sm text-slate-700 line-clamp-2" title={jobPost.description}>{jobPost.description}</span>
                </TableCell>
                <TableCell className="py-4">
                  <Link to={`/job-posts/${jobPost.id}`} className="text-sm font-medium text-blue-600 hover:underline">See more...</Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}