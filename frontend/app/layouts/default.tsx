import { NavLink, Link, Outlet } from "react-router";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "~/components/ui/navigation-menu";

export default function DefaultLayout() { 
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
              <NavLink to="/">
                <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                  Home
                </NavigationMenuLink>
              </NavLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <NavLink to="/job-boards">
                <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                  JobBoards
                </NavigationMenuLink>
              </NavLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
        </div>
      </header>
      <Outlet/>
    </main>
  );
}

 