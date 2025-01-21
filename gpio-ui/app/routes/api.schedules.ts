import { json } from "@remix-run/node";
import * as fs from "fs";
import * as path from "path";

const SCHEDULE_FILE = path.join(process.cwd(), "..", "pin_schedules.json");

function loadSchedules() {
	try {
		if (fs.existsSync(SCHEDULE_FILE)) {
			const data = fs.readFileSync(SCHEDULE_FILE, "utf8");
			return JSON.parse(data);
		}
		return {};
	} catch (error) {
		console.error("Error loading schedules:", error);
		return {};
	}
}

function saveSchedules(schedules: any) {
	try {
		fs.writeFileSync(SCHEDULE_FILE, JSON.stringify(schedules, null, 2));
		return true;
	} catch (error) {
		console.error("Error saving schedules:", error);
		return false;
	}
}

export async function loader() {
	const schedules = loadSchedules();
	return json(schedules);
}

export async function action({ request }: { request: Request }) {
	const formData = await request.formData();
	const intent = formData.get("intent");

	switch (intent) {
		case "add": {
			const pin = formData.get("pin") as string;
			const label = formData.get("label") as string;
			const on_time = formData.get("on_time") as string;
			const off_time = formData.get("off_time") as string;

			if (!pin || !label || !on_time || !off_time) {
				return json({ error: "Missing required fields" }, { status: 400 });
			}

			const schedules = loadSchedules();
			schedules[pin] = { label, on_time, off_time };

			if (saveSchedules(schedules)) {
				return json({ message: "Schedule added successfully" });
			}
			return json({ error: "Failed to save schedule" }, { status: 500 });
		}

		case "delete": {
			const pin = formData.get("pin") as string;
			if (!pin) {
				return json({ error: "Pin is required" }, { status: 400 });
			}

			const schedules = loadSchedules();
			if (pin in schedules) {
				delete schedules[pin];
				if (saveSchedules(schedules)) {
					return json({ message: "Schedule deleted successfully" });
				}
			}
			return json({ error: "Failed to delete schedule" }, { status: 500 });
		}

		default:
			return json({ error: "Invalid intent" }, { status: 400 });
	}
}
