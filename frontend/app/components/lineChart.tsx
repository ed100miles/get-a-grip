import type { PinchType } from "gql/graphql";
import {
	CartesianGrid,
	Label,
	Line,
	LineChart,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from "recharts";
import type { TooltipProps } from "recharts";
import type {
	NameType,
	ValueType,
} from "recharts/types/component/DefaultTooltipContent";

const formatDateTime = (datetime: string, short: boolean) => {
	const date = new Date(datetime);
	if (short) {
		const day = String(date.getDay()).padStart(2, "0");
		const month = String(date.getMonth() + 1).padStart(2, "0");
		const year = String(date.getFullYear()).slice(2);
		return `${day}-${month}-${year}`;
	}
	return date.toLocaleString();
};

// biome-ignore lint/suspicious/noExplicitAny: <type narrowing>
const isPinchType = (payload: any): payload is PinchType => {
	return (
		payload &&
		typeof payload.id === "number" &&
		typeof payload.userId === "number" &&
		typeof payload.weight === "number" &&
		typeof payload.duration === "number" &&
		typeof payload.createdAt === "string"
	);
};

const PinchTooltip = ({
	active,
	payload,
}: TooltipProps<ValueType, NameType>) => {
	if (active && payload && isPinchType(payload[0].payload)) {
		const pinch = payload[0].payload;
		const weight = pinch.weight;
		const duration = pinch.duration;
		const date = formatDateTime(pinch.createdAt, false);
		return (
			<div className="bg-slate-900 p-2 border border-slate-300 shadow-md rounded-md text-slate-300 text-sm">
				<p>{`Time: ${date}`}</p>
				<p>{`Duration: ${duration.toPrecision(2)} seconds`}</p>
				<p>{`Weight: ${weight.toPrecision(2)} kilograms`}</p>
			</div>
		);
	}
	return null;
};

export const PinchLineChart = ({ data }: { data: PinchType[] }) => (
	<ResponsiveContainer className="p-4">
		<LineChart
			data={data}
			margin={{
				top: 5,
				right: 30,
				left: 30,
				bottom: 100,
			}}
		>
			<Line type="monotone" dataKey="weight" stroke="#f1c40f" />
			<CartesianGrid stroke="#7b7d7d" />
			<XAxis
				stroke="#7b7d7d"
				dataKey="createdAt"
				tickFormatter={(tick) => formatDateTime(tick, true)}
				angle={-45}
				dy={50}
			>
				<Label value="Time" position="insideBottom" dy={1} />
			</XAxis>
			<YAxis stroke="#7b7d7d">
				<Label value="Weight (kg)" position="insideLeft" angle={-90} />
			</YAxis>
			<Tooltip content={<PinchTooltip />} />
		</LineChart>
	</ResponsiveContainer>
);
