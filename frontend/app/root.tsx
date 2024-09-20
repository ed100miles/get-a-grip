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
				<link rel="icon" href="data:image/x-icon;base64,AA" />
				<Meta />
				<Links />
			</head>
			<body className="bg-slate-900">
				<h1 className="text-3xl font-bold underline text-cyan-400">Hello world</h1>
				<Outlet />

				<Scripts />
			</body>
		</html>
	);
}
