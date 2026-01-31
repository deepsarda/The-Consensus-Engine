import { AnimatePresence, motion } from "framer-motion";
import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

const ReasoningStep = ({ step, index }) => (
	<div className="mb-4 relative pl-6 border-l border-slate-700 ml-2">
		<div className="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full bg-slate-800 border border-slate-600"></div>
		<div className="text-xs font-bold text-cyan-400 mb-1 tracking-wide uppercase">
			{step.step}
		</div>
		<div className="text-sm text-slate-300 leading-relaxed prose prose-invert prose-sm max-w-none">
			{typeof step.observation === "string" ? (
				<ReactMarkdown>{step.observation}</ReactMarkdown>
			) : (
				JSON.stringify(step.observation)
			)}
		</div>
	</div>
);

const MemberCard = ({ member, index }) => {
	const [expanded, setExpanded] = useState(false);

	// Check if reasoning_steps exists, otherwise fall back to reasoning string
	const steps = member.output?.reasoning_steps;
	const reasoningText = member.output?.reasoning;

	const verdictColor = member.output?.verdict?.toLowerCase().includes("fact")
		? "text-green-400 border-green-500/50 shadow-[0_0_10px_rgba(34,197,94,0.2)]"
		: member.output?.verdict?.toLowerCase().includes("misinformation") ||
				member.output?.verdict?.toLowerCase().includes("fake")
			? "text-red-400 border-red-500/50 shadow-[0_0_10px_rgba(239,68,68,0.2)]"
			: "text-yellow-400 border-yellow-500/50 shadow-[0_0_10px_rgba(234,179,8,0.2)]";

	return (
		<motion.div
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: index * 0.1 }}
			className="bg-black/50 backdrop-blur border border-cyan-500/30 overflow-hidden hover:border-cyan-400/60 transition-colors flex flex-col h-full group clip-path-angle relative"
		>
			<div className="absolute top-0 right-0 p-1 opacity-50 group-hover:opacity-100 transition-opacity">
				<div className="w-2 h-2 bg-current text-cyan-500"></div>
			</div>

			<div className="p-5 flex-1 relative z-10">
				<div className="flex flex-col sm:flex-row justify-between items-start mb-4 gap-3">
					<div className="flex items-center gap-3 min-w-0">
						
						<div className="min-w-0">
							<h3 className="font-display font-bold text-slate-200 leading-tight uppercase tracking-wider truncate">
								{member.member_name}
							</h3>
							<div className="text-[10px] text-cyan-600 uppercase tracking-[0.2em]">
								// Council_Unit_{index + 1}
							</div>
						</div>
					</div>
					<div
						className={`px-2 py-0.5 text-[10px] font-bold border uppercase tracking-wider shrink-0 ${verdictColor} bg-black/50 self-start sm:self-auto max-w-full truncate`}
					>
						{member.output?.verdict || "ANALYZING..."}
					</div>
				</div>

				<div className="mb-6">
					<div className="flex justify-between text-[10px] font-mono text-cyan-600 mb-1 uppercase">
						<span>Calculation_Confidence</span>
						<span>{member.output?.confidence_score}%</span>
					</div>
					<div className="w-full bg-slate-900 h-1 overflow-hidden relative">
						<div
							className={`h-full ${verdictColor.split(" ")[0].replace("text", "bg")}`}
							style={{ width: `${member.output?.confidence_score}%` }}
						></div>
						{/* Progress Bar Scanline */}
						<div className="absolute inset-0 bg-white/20 animate-[loading_1s_ease-in-out_infinite] w-full transform -translate-x-full"></div>
					</div>
				</div>

				{steps ? (
					<div className="space-y-4">
						<button
							onClick={() => setExpanded(!expanded)}
							className="w-full flex items-center justify-between text-xs font-mono font-bold text-cyan-500/70 uppercase tracking-widest hover:text-cyan-400 transition-colors bg-cyan-950/10 p-2 border border-cyan-500/20 hover:bg-cyan-950/30"
						>
							<span>&gt; Trace_Log [{steps.length}]</span>
							<span className="text-lg leading-none">
								{expanded ? "−" : "+"}
							</span>
						</button>

						<AnimatePresence>
							{expanded && (
								<motion.div
									initial={{ height: 0, opacity: 0 }}
									animate={{ height: "auto", opacity: 1 }}
									exit={{ height: 0, opacity: 0 }}
									className="overflow-hidden"
								>
									<div className="pt-4 pb-2 border-t border-cyan-900/50 mt-2 font-mono text-xs">
										{Array.isArray(steps) &&
											steps.map((step, idx) =>
												typeof step === "object" ? (
													<ReasoningStep key={idx} step={step} index={idx} />
												) : null,
											)}
									</div>
									{member.output?.conclusion && (
										<div className="bg-cyan-950/20 p-3 border-l-2 border-cyan-500 text-xs text-slate-300 mt-2 font-mono">
											<span className="text-cyan-500 mr-2">&gt;&gt;</span>"
											{member.output.conclusion}"
										</div>
									)}
								</motion.div>
							)}
						</AnimatePresence>
					</div>
				) : (
					<div className="text-sm text-slate-300 prose prose-invert font-mono text-xs">
						<ReactMarkdown>{reasoningText}</ReactMarkdown>
					</div>
				)}
			</div>

			{!expanded && steps && (
				<div className="px-5 pb-5 pt-0">
					<div className="text-xs text-slate-500 font-mono max-h-64 overflow-y-auto pl-2 border-l border-slate-800">
						<span className="text-slate-600 mr-1">&gt;</span>
						{member.output?.conclusion ||
							(steps[0]?.observation
								? steps[0].observation.substring(0, 100) + "..."
								: "")}
					</div>
				</div>
			)}
		</motion.div>
	);
};

const CouncilView = ({ data }) => {
	if (!data) return null;
	const validMembers = Array.isArray(data) ? data : [];

	return (
		<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
			{validMembers.map((member, idx) => (
				<MemberCard key={idx} member={member} index={idx} />
			))}
		</div>
	);
};
export default CouncilView;
