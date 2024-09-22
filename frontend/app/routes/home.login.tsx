import type { ActionFunctionArgs, LoaderFunctionArgs } from "@remix-run/node";
import { Form, json, redirect, useLoaderData } from "@remix-run/react";
import { commitSession, getSession } from "../sessions";

export async function loader({
    request,
}: LoaderFunctionArgs) {
    const session = await getSession(
        request.headers.get("Cookie")
    );

    if (session.has("userId") && session.has("accessToken")) {
        return redirect("/dashboard");
    }

    const data = { error: session.get("error") };

    return json(data, {
        headers: {
            "Set-Cookie": await commitSession(session),
        },
    });
}


export const action = async ({ request }: ActionFunctionArgs) => {
    const session = await getSession(
        request.headers.get("Cookie")
    );
    const formData = await request.formData();
    const { username, password } = Object.fromEntries(formData)

    const params = new URLSearchParams();
    params.append('username', username as string);
    params.append('password', password as string);

    const tokenResponse = await fetch('http://127.0.0.1:8000/user/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        },
        body: params.toString(),
    });

    const tokenData = await tokenResponse.json();
    const { access_token, user_id } = tokenData;

    if (!access_token || !user_id) {
        session.flash("error", "Invalid username/password");
        return redirect("/home/login", {
            headers: {
                "Set-Cookie": await commitSession(session),
            },
        });
    }
    session.set("userId", user_id);
    session.set("accessToken", access_token);
    return redirect("/dashboard", {
        headers: {
            "Set-Cookie": await commitSession(session),
        },
    });
}


const Login = () => {
    const { error } = useLoaderData<typeof loader>();
    return (
        <Form method="post">
            <p className="mb-5 text-white text-[15px] leading-normal">
                Login to your account to start training.
            </p>
            <fieldset className="mb-3 w-full flex flex-col justify-start">
                <label className="text-[13px] leading-none mb-2.5 text-white block" htmlFor="name">
                    Username
                </label>
                <input
                    className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
                    id="username"
                    name='username'
                    placeholder="ed"
                />
            </fieldset>
            <fieldset className="mb-3 w-full flex flex-col justify-start">
                <label className="text-[13px] leading-none mb-2.5 text-white block" htmlFor="username">
                    Password
                </label>
                <input
                    className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
                    name="password"
                    id="password"
                    type="password"
                    placeholder="******"
                />
            </fieldset>
            <div className="flex justify-center mt-5">
                <button type="submit" className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5">
                    Login
                </button>
            </div>
            {error ? <div className="text-red-500">{error}</div> : null}
        </Form>
    )
}

export default Login;
