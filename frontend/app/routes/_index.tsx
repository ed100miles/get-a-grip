import { redirect } from "@remix-run/node";

export const loader = async () => {
	return redirect("/home");
};

export default function Index() {
	return null;
}
