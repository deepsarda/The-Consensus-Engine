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
		? "text-green-400 bg-green-950/30 border-green-900/50"
		: member.output?.verdict?.toLowerCase().includes("misinformation") ||
				member.output?.verdict?.toLowerCase().includes("fake")
			? "text-red-400 bg-red-950/30 border-red-900/50"
			: "text-yellow-400 bg-yellow-950/30 border-yellow-900/50";

	return (
		<motion.div
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: index * 0.1 }}
			className="bg-slate-900/60 backdrop-blur border border-slate-700 rounded-xl overflow-hidden hover:border-slate-500 transition-colors flex flex-col h-full"
		>
			<div className="p-5 flex-1">
				<div className="flex justify-between items-start mb-4 gap-4">
					<div className="flex items-center gap-3">
						<div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-600 flex items-center justify-center font-bold text-slate-300 shrink-0">
							{member.member_name.split(" ")[1] || member.member_name.charAt(0)}
						</div>
						<div>
							<h3 className="font-bold text-white leading-tight">
								{member.member_name}
							</h3>
							<div className="text-xs text-slate-500 uppercase tracking-wider">
								Council Member
							</div>
						</div>
					</div>
					<div
						className={`px-2 py-1 rounded text-[10px] font-bold border uppercase tracking-wider shrink-0 ${verdictColor}`}
					>
						{member.output?.verdict || "PENDING"}
					</div>
				</div>

				<div className="mb-6">
					<div className="flex justify-between text-xs text-slate-500 mb-1">
						<span>Confidence</span>
						<span>{member.output?.confidence_score}%</span>
					</div>
					<div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
						<div
							className={`h-full ${verdictColor.split(" ")[0].replace("text", "bg").replace("-400", "-500")}`}
							style={{ width: `${member.output?.confidence_score}%` }}
						></div>
					</div>
				</div>

				{steps ? (
					<div className="space-y-4">
						<button
							onClick={() => setExpanded(!expanded)}
							className="w-full flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-widest hover:text-white transition-colors bg-slate-950/30 p-2 rounded border border-slate-800"
						>
							<span>Analysis Trace ({steps.length} Steps)</span>
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
									<div className="pt-4 pb-2 border-t border-slate-800 mt-2">
										{Array.isArray(steps) &&
											steps.map((step, idx) =>
												typeof step === "object" ? (
													<ReasoningStep key={idx} step={step} index={idx} />
												) : null,
											)}
									</div>
									{member.output?.conclusion && (
										<div className="bg-slate-950/50 p-3 rounded border border-slate-800 text-sm text-slate-300 mt-2 italic">
											"{member.output.conclusion}"
										</div>
									)}
								</motion.div>
							)}
						</AnimatePresence>
					</div>
				) : (
					<div className="text-sm text-slate-300 prose prose-invert">
						<ReactMarkdown>{reasoningText}</ReactMarkdown>
					</div>
				)}
			</div>

			{!expanded && steps && (
				<div className="px-5 pb-5 pt-0">
					<div className="text-sm text-slate-400 italic max-h-64 overflow-y-auto">
						"
						{member.output?.conclusion ||
							(steps[0]?.observation
								? steps[0].observation.substring(0, 100) + "..."
								: "")}
						"
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
