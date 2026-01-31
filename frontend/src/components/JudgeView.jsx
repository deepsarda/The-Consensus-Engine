import { AnimatePresence, motion } from "framer-motion";
import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

const JudgeView = ({ data }) => {
	// Extract correct data points based on user schema
	// data = { member_name: "...", output: { ... } }
	const output = data.output || {};
	const {
		final_verdict,
		verdict,
		explanation,
		summary,
		aggregated_confidence,
		model_evaluations,
	} = output;
	const currentVerdict = final_verdict || verdict || "Unknown";

	const isSafe =
		currentVerdict?.toLowerCase().includes("real") ||
		currentVerdict?.toLowerCase().includes("true");
	const isFake =
		currentVerdict?.toLowerCase().includes("fake") ||
		currentVerdict?.toLowerCase().includes("misinformation") ||
		currentVerdict?.toLowerCase().includes("mislabeled");

	const theme = isSafe
		? { border: "border-green-500", text: "text-green-400", bg: "bg-green-950" }
		: isFake
			? { border: "border-red-500", text: "text-red-400", bg: "bg-red-950" }
			: {
					border: "border-yellow-500",
					text: "text-yellow-400",
					bg: "bg-yellow-950",
				};

	const [showDetails, setShowDetails] = useState(false);

	return (
		<motion.div
			initial={{ opacity: 0, scale: 0.95 }}
			animate={{ opacity: 1, scale: 1 }}
			className={`border-2 ${theme.border} bg-black/60 relative overflow-hidden shadow-[0_0_30px_rgba(0,0,0,0.5)]`}
		>
			{/* Scanlines for the judge card */}
			<div className="absolute inset-0 pointer-events-none opacity-20 bg-[linear-gradient(transparent_2px,var(--color-bg)_2px)] bg-size-[100%_4px]"></div>

			<div
				className={`absolute top-0 left-0 w-full h-1 ${isSafe ? "bg-green-500 shadow-[0_0_10px_#22c55e]" : isFake ? "bg-red-500 shadow-[0_0_10px_#ef4444]" : "bg-yellow-500 shadow-[0_0_10px_#eab308]"}`}
			/>

			<div className="p-8 pb-4 relative z-10">
				<div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-8">
					<div className="flex-1">
						<h3 className="text-xs font-mono font-bold text-slate-500 uppercase tracking-widest mb-2 flex items-center gap-2">
							<span
								className={`w-2 h-2 rounded-full ${isSafe ? "bg-green-500" : isFake ? "bg-red-500" : "bg-yellow-500"} animate-pulse`}
							></span>
							Final_Adjudication_Output
						</h3>
						<h2
							className={`text-6xl font-display font-black uppercase tracking-tighter mb-4 ${theme.text} drop-shadow-sm leading-none glitch-text`}
							data-text={currentVerdict}
						>
							{currentVerdict}
						</h2>

						<div className="text-lg text-slate-300 border-l-4 border-slate-800 pl-6 my-6 prose prose-invert max-w-none font-mono">
							<ReactMarkdown>{explanation || summary}</ReactMarkdown>
						</div>
					</div>

					<div className="w-full md:w-auto bg-slate-950/80 p-6 border border-slate-800 space-y-4 min-w-50 shrink-0">
						<div>
							<div className="text-[10px] font-mono text-cyan-600 uppercase mb-1">
								Confidence_Level
							</div>
							<div className={`font-display text-4xl font-bold ${theme.text}`}>
								{aggregated_confidence || 0}%
							</div>
						</div>
						<div>
							<div className="text-[10px] font-mono text-cyan-600 uppercase mb-1">
								Case_Status
							</div>
							<div className="font-mono text-white inline-block px-2 py-0.5 border border-slate-700 text-xs bg-slate-900">
								[CLOSED]
							</div>
						</div>
					</div>
				</div>
			</div>

			{model_evaluations && (
				<div className="bg-black/40 border-t border-slate-800 relative z-10">
					<button
						onClick={() => setShowDetails(!showDetails)}
						className="w-full flex items-center justify-center gap-2 text-xs font-bold font-mono text-slate-500 uppercase tracking-widest hover:text-cyan-400 hover:bg-cyan-950/20 transition-colors py-3 group"
					>
						<span>
							{showDetails
								? "Hide_Council_Review_Logs"
								: "View_Council_Review_Logs"}
						</span>
						<span className="text-lg group-hover:translate-y-0.5 transition-transform">
							{showDetails ? "↑" : "↓"}
						</span>
					</button>

					<AnimatePresence>
						{showDetails && (
							<motion.div
								initial={{ height: 0, opacity: 0 }}
								animate={{ height: "auto", opacity: 1 }}
								exit={{ height: 0, opacity: 0 }}
								className="overflow-hidden"
							>
								<div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-slate-800 border-t border-slate-800">
									{model_evaluations.map((evalItem, idx) => (
										<div
											key={idx}
											className={`p-6 ${
												evalItem.status === "KEEP"
													? "bg-slate-950/80"
													: "bg-slate-950/40 opacity-50 grayscale"
											} hover:bg-slate-900 transition-colors`}
										>
											<div className="flex justify-between items-center mb-3">
												<div className="font-display font-bold text-slate-200 uppercase tracking-wider">
													{evalItem.model}
												</div>
												<div
													className={`text-[10px] font-mono font-bold px-2 py-0.5 border ${
														evalItem.status === "KEEP"
															? "bg-green-950/50 text-green-400 border-green-900"
															: "bg-slate-950 text-slate-500 border-slate-800"
													}`}
												>
													[{evalItem.status}]
												</div>
											</div>
											<div className="text-xs font-mono text-slate-400 leading-relaxed prose prose-invert prose-xs">
												<ReactMarkdown>{evalItem.reason}</ReactMarkdown>
											</div>
										</div>
									))}
								</div>
							</motion.div>
						)}
					</AnimatePresence>
				</div>
			)}
		</motion.div>
	);
};

export default JudgeView;
