import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";

const RootLayout = () => (
  <div className="min-h-screen">
    <div className="bg-gray-300 p-2 flex gap-2">
      <Link to="/" className="[&.active]:font-bold">
        Home
      </Link>{" "}
      <Link to="/about" className="[&.active]:font-bold">
        About
      </Link>{" "}
      <Link to="/contact" className="[&.active]:font-bold">
        contact
      </Link>{" "}
      <Link to="/exposed-or-not" className="[&.active]:font-bold">
        Exposed or Not
      </Link>
    </div>
    <hr />
    <div className="p-2 min-h-[200px]">
      <Outlet />
    </div>
    <TanStackRouterDevtools />
  </div>
);

export const Route = createRootRoute({ component: RootLayout });
