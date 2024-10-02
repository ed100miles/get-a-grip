export const formatDateTime = (
	datetime: string,
	short: boolean,
	ymd = false,
) => {
	const date = new Date(datetime);
	if (ymd) {
		const day = String(date.getDate()).padStart(2, "0");
		const month = String(date.getMonth() + 1).padStart(2, "0");
		const year = String(date.getFullYear());
		return `${year}-${month}-${day}`;
	}
	if (short) {
		const day = String(date.getDate()).padStart(2, "0");
		const month = String(date.getMonth() + 1).padStart(2, "0");
		const year = String(date.getFullYear()).slice(2);
		return `${day}-${month}-${year}`;
	}
	return date.toLocaleString();
};
