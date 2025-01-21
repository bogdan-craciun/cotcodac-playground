import { json, type LoaderFunction } from "@remix-run/node";
import { useLoaderData, useFetcher } from "@remix-run/react";
import { useState, useEffect } from "react";
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "~/components/ui/table";
import { useToast } from "~/hooks/use-toast";
import { Toaster } from "~/components/ui/toaster";

interface Schedule {
	on_time: string;
	off_time: string;
}

interface Schedules {
	[pin: string]: Schedule;
}

export const loader: LoaderFunction = async () => {
	const response = await fetch("http://localhost:5173/api/schedules");
	const schedules = await response.json();
	return json({ schedules, ENV: { API_ROOT: process.env.API_ROOT } });
};

export default function Index() {
	const { schedules: initialSchedules, ENV } = useLoaderData<typeof loader>();
	const { toast } = useToast();
	const fetcher = useFetcher();
	const [schedules, setSchedules] = useState<Schedules>(initialSchedules);
	const [newSchedule, setNewSchedule] = useState({
		pin: "",
		on_time: "",
		off_time: "",
	});

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const formData = new FormData();
		formData.append("intent", "add");
		formData.append("pin", newSchedule.pin);
		formData.append("on_time", newSchedule.on_time);
		formData.append("off_time", newSchedule.off_time);

		fetcher.submit(formData, {
			method: "post",
			action: "/api/schedules",
		});

		if (!fetcher.data?.error) {
			toast({
				title: "Success",
				description: "Schedule added successfully",
			});
			setNewSchedule({ pin: "", on_time: "", off_time: "" });
			// Refresh schedules
			const response = await fetch("/api/schedules");
			const newSchedules = await response.json();
			setSchedules(newSchedules);
		} else {
			toast({
				title: "Error",
				description: fetcher.data.error,
				variant: "destructive",
			});
		}
	};

	const handleDelete = async (pin: string) => {
		const formData = new FormData();
		formData.append("intent", "delete");
		formData.append("pin", pin);

		fetcher.submit(formData, {
			method: "post",
			action: "/api/schedules",
		});

		if (!fetcher.data?.error) {
			toast({
				title: "Success",
				description: "Schedule deleted successfully",
			});
			// Refresh schedules
			const response = await fetch("/api/schedules");
			const newSchedules = await response.json();
			setSchedules(newSchedules);
		} else {
			toast({
				title: "Error",
				description: fetcher.data.error,
				variant: "destructive",
			});
		}
	};

	const handleManualControl = async (pin: string, state: boolean) => {
		try {
			const response = await fetch(`${ENV.API_ROOT}/pin/${pin}`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ state }),
			});

			if (!response.ok) throw new Error("Failed to control pin");

			toast({
				title: "Success",
				description: `Pin ${pin} ${state ? "turned ON" : "turned OFF"}`,
			});
		} catch (error) {
			toast({
				title: "Error",
				description: "Failed to control pin",
				variant: "destructive",
			});
		}
	};

	return (
		<div className="container mx-auto p-4">
			<h1 className="text-3xl font-bold mb-8">GPIO Scheduler</h1>

			<div className="grid gap-8">
				<Card>
					<CardHeader>
						<CardTitle>Add New Schedule</CardTitle>
					</CardHeader>
					<CardContent>
						<form onSubmit={handleSubmit} className="space-y-4">
							<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
								<div className="space-y-2">
									<Label htmlFor="pin">GPIO Pin</Label>
									<Input
										id="pin"
										type="number"
										value={newSchedule.pin}
										onChange={e => setNewSchedule(prev => ({ ...prev, pin: e.target.value }))}
										required
									/>
								</div>
								<div className="space-y-2">
									<Label htmlFor="on_time">On Time (HH:MM)</Label>
									<Input
										id="on_time"
										type="time"
										value={newSchedule.on_time}
										onChange={e => setNewSchedule(prev => ({ ...prev, on_time: e.target.value }))}
										required
									/>
								</div>
								<div className="space-y-2">
									<Label htmlFor="off_time">Off Time (HH:MM)</Label>
									<Input
										id="off_time"
										type="time"
										value={newSchedule.off_time}
										onChange={e => setNewSchedule(prev => ({ ...prev, off_time: e.target.value }))}
										required
									/>
								</div>
							</div>
							<Button type="submit">Add Schedule</Button>
						</form>
					</CardContent>
				</Card>

				<Card>
					<CardHeader>
						<CardTitle>Current Schedules</CardTitle>
					</CardHeader>
					<CardContent>
						<Table>
							<TableHeader>
								<TableRow>
									<TableHead>Pin</TableHead>
									<TableHead>On Time</TableHead>
									<TableHead>Off Time</TableHead>
									<TableHead>Actions</TableHead>
								</TableRow>
							</TableHeader>
							<TableBody>
								{Object.entries(schedules).map(([pin, schedule]) => (
									<TableRow key={pin}>
										<TableCell>{pin}</TableCell>
										<TableCell>{schedule.on_time}</TableCell>
										<TableCell>{schedule.off_time}</TableCell>
										<TableCell>
											<div className="space-x-2">
												<Button
													variant="outline"
													size="sm"
													onClick={() => handleManualControl(pin, true)}
												>
													Turn On
												</Button>
												<Button
													variant="outline"
													size="sm"
													onClick={() => handleManualControl(pin, false)}
												>
													Turn Off
												</Button>
												<Button variant="destructive" size="sm" onClick={() => handleDelete(pin)}>
													Delete
												</Button>
											</div>
										</TableCell>
									</TableRow>
								))}
							</TableBody>
						</Table>
					</CardContent>
				</Card>
			</div>
			<Toaster />
		</div>
	);
}
