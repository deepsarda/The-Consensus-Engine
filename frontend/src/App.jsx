import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import CouncilView from "./components/CouncilView";
import ForensicsView from "./components/ForensicsView";
import InputSection from "./components/InputSection";
import JudgeView from "./components/JudgeView";

function App() {
	const [status, setStatus] = useState("idle"); // idle, processing, complete
	const [progress, setProgress] = useState([]);
	const [results, setResults] = useState({
		forensics: null,
		council: null,
		judge: null,
	});
	const wsRef = useRef(null);

	useEffect(() => {
		connectWs();
		return () => wsRef.current?.close();
	}, []);

	const connectWs = () => {
		wsRef.current = new WebSocket("ws://localhost:8000/ws/analyze");

		wsRef.current.onopen = () => {
			console.log("Connected to WebSocket");
		};

		wsRef.current.onmessage = (event) => {
			const data = JSON.parse(event.data);
			console.log("WS Message:", data);

			if (data.type === "progress") {
				setProgress((prev) => [...prev, data]);
			} else if (data.type === "result") {
				setResults((prev) => ({
					...prev,
					[data.step]: data.data,
				}));
			} else if (data.type === "complete") {
				setStatus("complete");
			} else if (data.type === "error") {
				console.error("Error:", data.message);
				alert(data.message);
				setStatus("idle");
			}
		};

		wsRef.current.onclose = () => {
			console.log("WS Closed");
		};
	};

	const handleStartAnalysis = (claim, imageBase64) => {
		if (wsRef.current?.readyState === WebSocket.OPEN) {
			setStatus("processing");
			setResults({ forensics: null, council: null, judge: null });
			setProgress([]);

			wsRef.current.send(
				JSON.stringify({
					claim,
					image: imageBase64,
				}),
			);
		} else {
			alert("Connection lost. Reconnecting...");
			connectWs();
		}
	};

	return (
		<div className="h-screen bg-slate-950 text-white selection:bg-cyan-500/30 font-inter flex flex-col">
			<header className="flex items-center justify-between p-5 shrink-0">
					<div className="flex items-center gap-3">
						<div className="w-8 h-8 rounded bg-linear-to-br from-cyan-400 to-blue-600 shadow-lg shadow-cyan-500/20"></div>
						<h1 className="text-xl font-bold tracking-wide text-slate-200">
							THE CONSENSUS ENGINE
						</h1>
					</div>
			</header>

			<div className="container mx-auto px-4 overflow-y-auto grow">
				<AnimatePresence mode="wait">
					{status === "idle" && (
						<motion.div
							key="input"
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							exit={{ opacity: 0 }}
							className="flex justify-center items-center py-12"
						>
							<InputSection onSubmit={handleStartAnalysis} />
						</motion.div>
					)}

					{(status === "processing" || status === "complete") && (
						<motion.div
							key="results"
							initial={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							className="max-w-4xl mx-auto space-y-8"
						>
							<div className="flex items-center justify-between">
								<h2 className="text-3xl font-bold bg-clip-text text-transparent bg-linear-to-r from-white to-slate-400">
									Investigation In Progress
								</h2>
								{status === "processing" && (
									<div className="flex items-center gap-2">
										<span className="relative flex h-3 w-3">
											<span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
											<span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
										</span>
										<span className="text-cyan-400 text-sm font-mono animate-pulse">
											LIVE PROCESSING
										</span>
									</div>
								)}
							</div>

							{/* Timeline / Steps */}
							<div className="space-y-6">
								{/* Forensics Step */}
								<motion.div
									initial={{ opacity: 0, x: -20 }}
									animate={{ opacity: 1, x: 0 }}
									className="border-l-2 border-slate-800 pl-6 pb-6 relative"
								>
									<div
										className={`absolute -left-[9px] top-0 w-4 h-4 rounded-full border-2 transition-colors ${results.forensics ? "bg-green-500 border-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" : "bg-slate-900 border-slate-600"}`}
									></div>
									<h3
										className={`font-mono text-sm uppercase tracking-wider mb-2 ${results.forensics ? "text-green-400" : "text-slate-500"}`}
									>
										01. Forensic Analysis
									</h3>
									{results.forensics ? (
										<ForensicsView data={results.forensics} />
									) : (
										<div className="h-12 flex items-center text-slate-600 text-sm italic border-l-2 border-slate-800/50 pl-4">
											Scanning image metadata and content...
										</div>
									)}
								</motion.div>

								{/* Council Step */}
								<motion.div
									initial={{ opacity: 0, x: -20 }}
									animate={{ opacity: 1, x: 0 }}
									transition={{ delay: 0.2 }}
									className="border-l-2 border-slate-800 pl-6 pb-6 relative"
								>
									<div
										className={`absolute -left-[9px] top-0 w-4 h-4 rounded-full border-2 transition-colors ${results.council ? "bg-blue-500 border-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" : "bg-slate-900 border-slate-600"}`}
									></div>
									<h3
										className={`font-mono text-sm uppercase tracking-wider mb-2 ${results.council ? "text-blue-400" : "text-slate-500"}`}
									>
										02. Council Deliberation
									</h3>
									{results.council ? (
										<CouncilView data={results.council} />
									) : (
										<div className="h-12 flex items-center text-slate-600 text-sm italic border-l-2 border-slate-800/50 pl-4">
											Waiting for council assembly...
										</div>
									)}
								</motion.div>

								{/* Judge Step */}
								<motion.div
									initial={{ opacity: 0, x: -20 }}
									animate={{ opacity: 1, x: 0 }}
									transition={{ delay: 0.4 }}
									className="border-l-2 border-slate-800 pl-6 relative"
								>
									<div
										className={`absolute -left-[9px] top-0 w-4 h-4 rounded-full border-2 transition-colors ${results.judge ? "bg-purple-500 border-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]" : "bg-slate-900 border-slate-600"}`}
									></div>
									<h3
										className={`font-mono text-sm uppercase tracking-wider mb-2 ${results.judge ? "text-purple-400" : "text-slate-500"}`}
									>
										03. Final Judgement
									</h3>
									{results.judge ? (
										<JudgeView data={results.judge} />
									) : (
										<div className="h-12 flex items-center text-slate-600 text-sm italic border-l-2 border-slate-800/50 pl-4">
											Pending adjudication...
										</div>
									)}
								</motion.div>
							</div>
						</motion.div>
					)}
				</AnimatePresence>
			</div>
		</div>
	);
}

export default App;
