import { Link, useFetcher } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import type { Route } from "../+types/root";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Button } from "~/components/ui/button";

export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
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

  return (
    <>
    <Button className="">
      <Link to="/job-boards/new">Add New Job Board</Link>
    </Button>
    <Table className="w-1/2">
      <TableHeader>
        <TableRow>
          <TableHead>Logo</TableHead>
          <TableHead>Slug</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
          {loaderData.jobBoards.map(
          (jobBoard) => 
            <TableRow key={jobBoard.id}>
              <TableCell>
                {jobBoard.logo_path
                ?  <Avatar><AvatarImage src={jobBoard.logo_path}></AvatarImage></Avatar>
                : <></>}
              </TableCell>
              <TableCell><Link to={`/job-boards/${jobBoard.id}/job-posts`} className="capitalize">{jobBoard.slug}</Link></TableCell>
              <TableCell>
                <Link to={`/job-boards/edit?id=${jobBoard.id}&slug=${jobBoard.slug}&logo=${jobBoard.logo_path}`}>Edit</Link>
                <fetcher.Form method="post"
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