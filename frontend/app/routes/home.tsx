import { Link, NavLink } from "react-router";
import { Button } from "~/components/ui/button";

export default function Home() {
    return (
        <main className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center text-center">
            <h1 className="text-3xl font-bold">Welcome to Jobify!</h1>
            <p className="text-xl mt-4">You can find next job</p>
            <Button className="mt-4 min-w-[100px]"><NavLink to="/admin-login">Login</NavLink></Button>
            
            {/* <Link to="/job-boards">Job Boards</Link> */}
        </main>
    )
}