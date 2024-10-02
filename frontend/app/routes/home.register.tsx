import type { ActionFunctionArgs } from "@remix-run/node";
import { Form, json, useActionData } from "@remix-run/react";

export const action = async ({ request }: ActionFunctionArgs) => {
	const formData = await request.formData();
	const { username, email, password1, password2 } =
		Object.fromEntries(formData);
	if (!username || !email || !password1 || !password2) {
		return json({ error: "All fields are required", success: false });
	}
	if (password1 !== password2) {
		return json({ error: "Passwords do not match", success: false });
	}
	const response = await fetch("http://127.0.0.1:8000/user/create", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Accept: "application/json",
		},
		body: JSON.stringify({
			username: username,
			email: email,
			password: password1,
		}),
	});
	if (!response.ok) {
		const errorMessage = await response.json();
		return json({ error: errorMessage.detail, success: false });
	}
	return json({ success: true, error: null });
};

const Register = () => {
	const actionData = useActionData<typeof action>();
	return (
		<Form method="post">
			<p className="mb-5 text-white text-[15px] leading-normal">
				Sign up to start training - it's free!
			</p>
			<fieldset className="mb-3 w-full flex flex-col justify-start">
				<label
					className="text-[13px] leading-none mb-2.5 text-white block"
					htmlFor="name"
				>
					Username
				</label>
				<input
					className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
					id="username"
					name="username"
					placeholder="ed"
				/>
			</fieldset>
			<fieldset className="mb-3 w-full flex flex-col justify-start">
				<label
					className="text-[13px] leading-none mb-2.5 text-white block"
					htmlFor="name"
				>
					Email
				</label>
				<input
					className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
					id="email"
					name="email"
					placeholder="ed@mail.com"
				/>
			</fieldset>
			<fieldset className="mb-3 w-full flex flex-col justify-start">
				<label
					className="text-[13px] leading-none mb-2.5 text-white block"
					htmlFor="name"
				>
					Password
				</label>
				<input
					className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
					id="password1"
					name="password1"
					type="password"
					placeholder="test"
				/>
			</fieldset>
			<fieldset className="mb-3 w-full flex flex-col justify-start">
				<label
					className="text-[13px] leading-none mb-2.5 text-white block"
					htmlFor="name"
				>
					Confirm Password
				</label>
				<input
					className="grow shrink-0 rounded px-2.5 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
					id="password2"
					name="password2"
					type="password"
					placeholder="test"
				/>
			</fieldset>
			<div className="flex justify-center mt-5">
				<button
					type="submit"
					className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5"
				>
					Sign Up
				</button>
			</div>
			{actionData?.error && (
				<div className="text-red-500">{String(actionData?.error)}</div>
			)}
			{actionData?.success && (
				<div className="text-green-500">
					{"You're signed up! Validate your email and you're all set."}
				</div>
			)}
		</Form>
	);
};

export default Register;
