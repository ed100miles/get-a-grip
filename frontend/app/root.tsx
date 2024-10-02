import type { LinksFunction } from "@remix-run/node";
import { Links, Meta, Outlet, Scripts } from "@remix-run/react";
import stylesheet from "./tailwind.css?url";


export const links: LinksFunction = () => [
	{ rel: "stylesheet", href: stylesheet },
];


export default function App() {
	return (
		<html lang="en">
			<head>
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<Meta />
				<Links />
			</head>
			<body className="bg-slate-900">
				<Outlet />
				<Scripts />
			</body>
		</html>
	);
}
