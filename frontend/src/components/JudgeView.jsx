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
		currentVerdict?.toLowerCase().includes("misinformation");

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
			className={`rounded-xl border ${theme.border} bg-slate-900/50 relative overflow-hidden shadow-2xl`}
		>
			<div
				className={`absolute top-0 left-0 w-full h-1 ${isSafe ? "bg-green-500" : isFake ? "bg-red-500" : "bg-yellow-500"}`}
			/>

			<div className="p-8 pb-4">
				<div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-8">
					<div className="flex-1">
						<h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">
							Final Adjudication
						</h3>
						<h2
							className={`text-4xl md:text-5xl font-black uppercase tracking-tighter mb-4 ${theme.text} drop-shadow-sm leading-none`}
						>
							{currentVerdict}
						</h2>

						<div className="text-lg text-slate-300 font-light border-l-2 border-slate-700 pl-6 my-6 prose prose-invert max-w-none">
							<ReactMarkdown>{explanation || summary}</ReactMarkdown>
						</div>
					</div>

					<div className="w-full md:w-auto bg-slate-950/80 rounded-lg p-6 border border-slate-800 space-y-4 min-w-50 shrink-0">
						<div>
							<div className="text-xs text-slate-500 uppercase mb-1">
								Confidence
							</div>
							<div className={`font-mono text-3xl font-bold ${theme.text}`}>
								{aggregated_confidence || 0}%
							</div>
						</div>
						<div>
							<div className="text-xs text-slate-500 uppercase mb-1">
								Status
							</div>
							<div className="font-mono text-white inline-block px-2 py-0.5 rounded bg-slate-800 text-xs border border-slate-700">
								CASE CLOSED
							</div>
						</div>
					</div>
				</div>
			</div>

			{model_evaluations && (
				<div className="bg-slate-950/30 border-t border-slate-800">
					<button
						onClick={() => setShowDetails(!showDetails)}
						className="w-full flex items-center justify-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-widest hover:text-white hover:bg-slate-800/50 transition-colors py-3"
					>
						<span>
							{showDetails ? "Hide Council Review" : "View Council Review"}
						</span>
						<span className="text-lg">{showDetails ? "↑" : "↓"}</span>
					</button>

					<AnimatePresence>
						{showDetails && (
							<motion.div
								initial={{ height: 0, opacity: 0 }}
								animate={{ height: "auto", opacity: 1 }}
								exit={{ height: 0, opacity: 0 }}
								className="overflow-hidden"
							>
								<div className="grid grid-cols-1 md:grid-cols-3 gap-0 divide-y md:divide-y-0 md:divide-x divide-slate-800 border-t border-slate-800">
									{model_evaluations.map((evalItem, idx) => (
										<div
											key={idx}
											className={`p-6 ${
												evalItem.status === "KEEP"
													? "bg-slate-900/10"
													: "bg-slate-950/50 opacity-60 grayscale-[0.5]"
											}`}
										>
											<div className="flex justify-between items-center mb-3">
												<div className="font-bold text-slate-200">
													{evalItem.model}
												</div>
												<div
													className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
														evalItem.status === "KEEP"
															? "bg-green-950 text-green-400 border-green-900"
															: "bg-slate-900 text-slate-500 border-slate-700"
													}`}
												>
													{evalItem.status}
												</div>
											</div>
											<div className="text-xs text-slate-400 leading-relaxed prose prose-invert prose-xs">
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
