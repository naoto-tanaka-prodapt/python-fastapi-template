export async function clientLoader({params}) {
  const company_id = params.companyId;
  const res = await fetch(`/api/job-boards/${company_id}/job-posts`);
  const jobPosts = await res.json();
  return {jobPosts}
}

export default function JobPosts({loaderData}) {
  return (
    <div>
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