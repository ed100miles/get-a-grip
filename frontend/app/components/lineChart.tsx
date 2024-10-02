import type { PinchType } from "gql/graphql";
import {
	ResponsiveContainer,
	LineChart,
	Line,
	CartesianGrid,
	XAxis,
	YAxis,
	Tooltip,
} from "recharts";

export const PinchLineChart = ({ data }: { data: PinchType[] }) => (
	<ResponsiveContainer className="p-4">
		<LineChart data={data}>
			<Line type="monotone" dataKey="weight" stroke="#8884d8" />
			<CartesianGrid stroke="#ccc" />
			<XAxis dataKey="createdAt" />
			<YAxis />
			<Tooltip />
		</LineChart>
	</ResponsiveContainer>
);
