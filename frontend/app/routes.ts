import { layout, prefix, route, type RouteConfig } from "@react-router/dev/routes";

// export default [
//     route("job-boards", "routes/job_boards.tsx"),
//     route("job-boards/:companyId/job-posts", "routes/job_posts.tsx"),
// ] satisfies RouteConfig;

export default [
  layout("layouts/default.tsx", [
    route("/", "routes/home.tsx"),
    route("/admin-login", "routes/admin_login_form.tsx"),
    route("/admin-logout", "routes/admin_logout.tsx"),
    ...prefix("job-boards", [
        route("", "routes/job_boards.tsx"),                       // /job-boards
        route(":companyId/job-posts", "routes/job_posts.tsx"),    // /job-boards/:companyId/job-posts
        route("/new", "routes/new_job_boards.tsx"),               // /job-boards/new
        route("/:companyId/edit", "routes/edit_job_boards.tsx"),  // /job-boards/:companyId/edit
        route("/:companyId/add-job", "routes/new_job_posts.tsx"), // /job-boards/:companyId/add-job
    ]),
    ...prefix("job-posts", [
        route("/:jobPostId", "routes/view_job_posts.tsx"),         // /job-posts/:jobPostId
    ]),
    ...prefix("job-applications", [
        route("", "routes/job_applications.tsx"),                 // /job-applications
        route("/new", "routes/new_job_application.tsx"),          // /job-applications/new
        route("/:jobApplicationId/edit", "routes/edit_job_application.tsx"), // /job-applications/edit
    ]),
  ])
] satisfies RouteConfig;
