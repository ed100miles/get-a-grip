import * as Switch from "@radix-ui/react-switch";
import type { LoaderFunctionArgs } from "@remix-run/node";
import {
	Form,
	json,
	redirect,
	useLoaderData,
	useSubmit,
} from "@remix-run/react";
import { request as gqlRequest } from "graphql-request";
import GetPinches from "../../gqlQueries/getPinches";
import { getSession } from "../sessions";

export const loader = async ({ request }: LoaderFunctionArgs) => {
	const session = await getSession(request.headers.get("Cookie"));
	const jwtToken = session.get("accessToken");
	const userId = Number(session.get("userId"));

	if (!jwtToken) {
		return redirect("/home/login");
	}

	const url = new URL(request.url);

	const wideGrip = Boolean(url.searchParams.get("wideGrip")) || false;
	const deepGrip = Boolean(url.searchParams.get("deepGrip")) || false;
	const minWeight = Number(url.searchParams.get("minWeight")) || 0;
	const maxWeight = Number(url.searchParams.get("maxWeight")) || 1000;
	const minDuration = Number(url.searchParams.get("minDuration")) || 0;
	const maxDuration = Number(url.searchParams.get("maxDuration")) || 1000;

	const userPinches = await gqlRequest(
		"http://localhost:8000/graphql",
		GetPinches,
		{
			userId: userId,
			wide: wideGrip,
			deep: deepGrip,
			minWeight: minWeight,
			maxWeight: maxWeight,
			minDuration: minDuration,
			maxDuration: maxDuration,
		},
		{
			Authorization: `Bearer ${jwtToken}`,
			"Content-Type": "application/json",
		},
	);

	return json({ pinches: userPinches.pinches });
};

const Dashboard = () => {
	const { pinches } = useLoaderData<typeof loader>();
	const submit = useSubmit();
	return (
		<div className="h-screen w-screen flex">
			<div className="h-full w-1/4 border-r-8 border-slate-500 p-5">
				<div className="border-2 border-slate-300 flex h-full rounded-md">
					<Form
						className="p-4 h-1/2 flex flex-col justify-evenly"
						onChange={(event) => submit(event.currentTarget)}
					>
						<fieldset className="flex items-center">
							<label
								className="text-white text-[15px] leading-none pr-[15px]"
								htmlFor="wideGrip"
							>
								Wide Grip
							</label>
							<Switch.Root
								className="w-[42px] h-[25px] bg-slate-500 rounded-full relative shadow-md shadow-slate-700 focus:shadow-slate-900 data-[state=checked]:bg-slate-400 outline-none cursor-pointer"
								id="wideGrip"
								name="wideGrip"
							>
								<Switch.Thumb className="block w-[21px] h-[21px] bg-white rounded-full shadow-[0_2px_2px] shadow-slate-800 transition-transform duration-100 translate-x-0.5 will-change-transform data-[state=checked]:translate-x-[19px]" />
							</Switch.Root>
						</fieldset>
						<fieldset className="flex items-center">
							<label
								className="text-white text-[15px] leading-none pr-[15px]"
								htmlFor="deepGrip"
							>
								Deep Grip
							</label>
							<Switch.Root
								className="w-[42px] h-[25px] bg-slate-500 rounded-full relative shadow-md shadow-slate-700 focus:shadow-slate-900 data-[state=checked]:bg-slate-400 outline-none cursor-pointer"
								id="deepGrip"
								name="deepGrip"
							>
								<Switch.Thumb className="block w-[21px] h-[21px] bg-white rounded-full shadow-[0_2px_2px] shadow-slate-800 transition-transform duration-100 translate-x-0.5 will-change-transform data-[state=checked]:translate-x-[19px]" />
							</Switch.Root>
						</fieldset>
						<div className="mb-3 w-full flex justify-between">
							<fieldset className="mb-3 w-full flex flex-col justify-start">
								<label
									className="text-[15px] leading-none mb-2.5 text-white block"
									htmlFor="minWeight"
								>
									Min Weight (kg)
								</label>
								<input
									className="grow shrink-0 rounded px-2.5 w-2/3 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
									name="minWeight"
									id="minWeight"
									type="number"
									placeholder="0"
									defaultValue={0}
								/>
							</fieldset>
							<fieldset className="mb-3 w-full flex flex-col justify-start">
								<label
									className="text-[15px] leading-none mb-2.5 text-white block"
									htmlFor="maxWeight"
								>
									Max Weight (kg)
								</label>
								<input
									className="grow shrink-0 rounded px-2.5 w-2/3 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
									name="maxWeight"
									id="maxWeight"
									type="number"
									placeholder="0"
									defaultValue={1000}
								/>
							</fieldset>
						</div>
						<div className="mb-3 w-full flex justify-between">
							<fieldset className="mb-3 w-full flex flex-col justify-start">
								<label
									className="text-[15px] leading-none mb-2.5 text-white block"
									htmlFor="minWeight"
								>
									Min Duration (s)
								</label>
								<input
									className="grow shrink-0 rounded px-2.5 w-2/3 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
									name="minDuration"
									id="minDuration"
									type="number"
									placeholder="0"
									defaultValue={0}
								/>
							</fieldset>
							<fieldset className="mb-3 w-full flex flex-col justify-start">
								<label
									className="text-[15px] leading-none mb-2.5 text-white block"
									htmlFor="maxWeight"
								>
									Max Duration (s)
								</label>
								<input
									className="grow shrink-0 rounded px-2.5 w-2/3 text-[15px] leading-none text-slate-900 shadow-[0_0_0_1px] shadow-slate-900 h-[35px] focus:shadow-[0_0_0_1px] focus:shadow-slate-700 outline-none"
									name="maxDuration"
									id="maxDuration"
									type="number"
									placeholder="0"
									defaultValue={1000}
								/>
							</fieldset>
						</div>
					</Form>
				</div>
			</div>
			<div className="bg-slate-900 h-full w-3/4 overflow-auto flex flex-col items-center p-4">
				{pinches.map((pinch) => (
					<div key={pinch.id} className="text-slate-300 w-full flex">
						{pinch.wide ? "Wide" : "Narrow"} Grip{" "}
						{pinch.deep ? "Deep" : "Shallow"} Grip {pinch.weight}kg{" "}
						{pinch.duration}s
					</div>
				))}
			</div>
		</div>
	);
};

export default Dashboard;
