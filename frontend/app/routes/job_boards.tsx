import { Link, useFetcher } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import type { Route } from "../+types/root";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Button } from "~/components/ui/button";
import { userContext } from "~/context";

export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards, isAdmin}
}

export async function clientAction({ request }: Route.ClientActionArgs) {
  const formData = await request.formData()
  const jobBoardId = formData.get('job_board_id')
  await fetch(`/api/job-boards/${jobBoardId}`, {
      method: 'DELETE'
  })
}

export default function JobBoards({loaderData}) {
  const fetcher = useFetcher()
  console.log(loaderData.isAdmin)

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 space-y-6">
      {loaderData.isAdmin ? (
        <div className="flex justify-end">
          <Button>
            <Link to="/job-boards/new">Add New Job Board</Link>
          </Button>
        </div>
      ) : null}

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <Table className="w-full table-fixed">
          <TableHeader>
            <TableRow className="bg-slate-50">
              <TableHead className="w-24 text-slate-600">Logo</TableHead>
              <TableHead className="w-64 text-slate-600">Slug</TableHead>
              {loaderData.isAdmin && <TableHead className="text-right text-slate-600">Actions</TableHead>}
            </TableRow>
          </TableHeader>
          <TableBody>
            {loaderData.jobBoards.map((jobBoard) => (
              <TableRow key={jobBoard.id} className="hover:bg-slate-50/80 transition">
                <TableCell className="py-4">
                  {jobBoard.logo_path ? (
                    <Avatar>
                      <AvatarImage src={jobBoard.logo_path}></AvatarImage>
                    </Avatar>
                  ) : null}
                </TableCell>
                <TableCell className="py-4 font-medium w-64 max-w-xs">
                  <Link
                    to={`/job-boards/${jobBoard.id}/job-posts`}
                    className="capitalize text-blue-600 hover:underline line-clamp-1"
                    title={jobBoard.slug}
                  >
                    {jobBoard.slug}
                  </Link>
                </TableCell>
                {loaderData.isAdmin && (
                  <TableCell className="py-4">
                    <div className="flex items-center justify-end gap-3">
                      <Link to={`/job-boards/${jobBoard.id}/edit`} className="text-sm text-blue-600 hover:underline">
                        Edit
                      </Link>
                      <fetcher.Form
                        method="post"
                        onSubmit={(event) => {
                          const response = confirm(
                            `Please confirm you want to delete this job board '${jobBoard.slug}'.`,
                          );
                          if (!response) {
                            event.preventDefault();
                          }
                        }}
                      >
                        <input name="job_board_id" type="hidden" value={jobBoard.id}></input>
                        <button className="text-sm text-red-600 hover:underline">Delete</button>
                      </fetcher.Form>
                    </div>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
