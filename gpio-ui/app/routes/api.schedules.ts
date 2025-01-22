import { json } from "@remix-run/node";
import * as fs from "fs";
import * as path from "path";
import crypto from "crypto";

const SCHEDULE_FILE = path.join(process.cwd(), "..", "pin_schedules.json");

interface Schedule {
	id: string;
	pin: string;
	label: string;
	on_time: string;
	off_time: string;
}

interface ScheduleFile {
	schedules: Schedule[];
}

function generateId(): string {
	return crypto.randomBytes(16).toString("hex");
}

function loadSchedules(): ScheduleFile {
	try {
		if (fs.existsSync(SCHEDULE_FILE)) {
			const data = fs.readFileSync(SCHEDULE_FILE, "utf8");
			return JSON.parse(data);
		}
		return { schedules: [] };
	} catch (error) {
		console.error("Error loading schedules:", error);
		return { schedules: [] };
	}
}

function saveSchedules(scheduleFile: ScheduleFile): boolean {
	try {
		fs.writeFileSync(SCHEDULE_FILE, JSON.stringify(scheduleFile, null, 2));
		return true;
	} catch (error) {
		console.error("Error saving schedules:", error);
		return false;
	}
}

export async function loader() {
	const scheduleFile = loadSchedules();
	return json(scheduleFile);
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

			const scheduleFile = loadSchedules();
			const newSchedule: Schedule = {
				id: generateId(),
				pin,
				label,
				on_time,
				off_time,
			};

			scheduleFile.schedules.push(newSchedule);

			if (saveSchedules(scheduleFile)) {
				return json({ message: "Schedule added successfully" });
			}
			return json({ error: "Failed to save schedule" }, { status: 500 });
		}

		case "delete": {
			const id = formData.get("id") as string;
			if (!id) {
				return json({ error: "Schedule ID is required" }, { status: 400 });
			}

			const scheduleFile = loadSchedules();
			const scheduleIndex = scheduleFile.schedules.findIndex(s => s.id === id);

			if (scheduleIndex !== -1) {
				scheduleFile.schedules.splice(scheduleIndex, 1);
				if (saveSchedules(scheduleFile)) {
					return json({ message: "Schedule deleted successfully" });
				}
			}
			return json({ error: "Failed to delete schedule" }, { status: 500 });
		}

		default:
			return json({ error: "Invalid intent" }, { status: 400 });
	}
}
