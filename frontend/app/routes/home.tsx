import { Link } from "react-router";

export default function Home() {
    return (
        <main>
            <h1 className="text-3xl font-bold">Welcome to Jobify!</h1>
            <p className="text-xl mt-4">You can find next job</p>
            {/* <Link to="/job-boards">Job Boards</Link> */}
        </main>
    )
}