import { NavLink, Link, Outlet } from "react-router";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "~/components/ui/navigation-menu";
import { userContext } from "~/context";
import type { Route } from "../+types/root";

export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  const me = context.get(userContext)
  const isAdmin = me && me.is_admin
  return {isAdmin}
}

export default function DefaultLayout( {loaderData}: Route.ComponentProps ) { 
  return (
    <main>
      <header className="border-b mb-4">
        <div className="mx-auto flex h-16 justify-between px-4">
        <Link to="/" className="flex items-center gap-2">
          <img
            src="/header-icon.jpg"
            width={32}
            height={32}
          />
          <span className="text-lg font-bold">Jobify</span>
        </Link>
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <NavLink to="/" className={navigationMenuTriggerStyle()}>
                  Home
                </NavLink>
              </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <NavLink to="/job-boards" className={navigationMenuTriggerStyle()}>
                  JobBoards
                </NavLink>
              </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <NavLink to="/job-applications" className={navigationMenuTriggerStyle()}>
                  JobApplications
                </NavLink>
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
            { loaderData.isAdmin ?
              <NavigationMenuLink asChild>
                <NavLink to="/admin-logout" className={navigationMenuTriggerStyle()}>
                  Logout
                </NavLink>
              </NavigationMenuLink>
            : <NavigationMenuLink asChild>
                <NavLink to="/admin-login" className={navigationMenuTriggerStyle()}>
                  Login
                </NavLink>
              </NavigationMenuLink>
            }
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
        </div>
      </header>
      <Outlet/>
    </main>
  );
}

 
