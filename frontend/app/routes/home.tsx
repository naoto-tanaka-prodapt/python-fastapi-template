import { Link, NavLink } from "react-router";
import { Button } from "~/components/ui/button";

export default function Home() {
    return (
        <main className="text-center">
            <h1 className="text-3xl font-bold">Welcome to Jobify!</h1>
            <p className="text-xl mt-4">You can find next job</p>
            <Button className="mt-4"><NavLink to="/admin-login">Login</NavLink></Button>
            
            {/* <Link to="/job-boards">Job Boards</Link> */}
        </main>
    )
}