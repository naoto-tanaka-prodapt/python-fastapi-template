import { layout, prefix, route, type RouteConfig } from "@react-router/dev/routes";

// export default [
//     route("job-boards", "routes/job_boards.tsx"),
//     route("job-boards/:companyId/job-posts", "routes/job_posts.tsx"),
// ] satisfies RouteConfig;

export default [
  layout("layouts/default.tsx", [
    route("/", "routes/home.tsx"),
    ...prefix("job-boards", [
        route("", "routes/job_boards.tsx"),                    // /job-boards
        route(":companyId/job-posts", "routes/job_posts.tsx"), // /job-boards/:companyId/job-posts
        route("/new", "routes/new_job_boards.tsx"), // /job-boards/new
        route("/edit", "routes/edit_job_boards.tsx"), // /job-boards/edit
    ]),
  ])
] satisfies RouteConfig;
