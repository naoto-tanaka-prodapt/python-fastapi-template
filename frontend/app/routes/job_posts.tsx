import { Link } from "react-router";
import { Button } from "~/components/ui/button";
import type { Route } from "../+types/root";
import { userContext } from "~/context";


export async function clientLoader({params, context}: Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  
  const company_id = params.companyId;
  const res = await fetch(`/api/job-boards/${company_id}/job-posts`);
  const jobPosts = await res.json();
  return {jobPosts, isAdmin, company_id}
}

export default function JobPosts({loaderData}) {
  return (
    <div>
      { loaderData.isAdmin ? 
      <Button className="">
        <Link to={`/job-boards/${loaderData.company_id}/add-job`}>Add New Job</Link>
      </Button>
      : <></>
      }
      {loaderData.jobPosts.map(
        (jobPost) => 
          <div>
            <h1>{jobPost.title}</h1>
            <p>{jobPost.description}</p>
          </div>
      )}
    </div>
  )
}