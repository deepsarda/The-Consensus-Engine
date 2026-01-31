import { motion } from "framer-motion";
import React from "react";
import ReactMarkdown from "react-markdown";

// Helper to format keys (e.g., "fake_prob" -> "Fake Prob")
const formatKey = (key) => {
	return key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
};

const DataNode = ({ value, depth = 0 }) => {
	if (value === null || value === undefined)
		return <span className="text-slate-500 italic">null</span>;

	// Handle specific boolean cases
	if (typeof value === "boolean") {
		return (
			<span className={value ? "text-green-400 font-bold" : "text-slate-400"}>
				{value.toString()}
			</span>
		);
	}

	if (Array.isArray(value)) {
		return (
			<div className="space-y-1">
				{value.map((item, idx) => (
					<div key={idx} className="pl-2 border-l border-slate-700">
						<DataNode value={item} depth={depth + 1} />
					</div>
				))}
			</div>
		);
	}

	if (typeof value === "object") {
		if (Object.keys(value).length === 0)
			return <span className="text-slate-600 font-mono">{"{}"}</span>;
		return (
			<div className="space-y-1">
				{Object.entries(value).map(([subKey, subValue]) => (
					<div key={subKey} className="ml-2">
						<span className="text-slate-500 text-xs font-mono mr-2">
							{formatKey(subKey)}:
						</span>
						<div className="inline-block align-top">
							<DataNode value={subValue} depth={depth + 1} />
						</div>
					</div>
				))}
			</div>
		);
	}

	// String handling - check for Markdown-like content or long text
	if (typeof value === "string") {
		// If it's a long text or contains newlines, render as markdown block
		if (value.includes("\n") || value.length > 50) {
			return (
				<div className="prose prose-invert prose-xl max-w-none text-slate-300 bg-slate-950/30 p-2 rounded border border-slate-800/50 mt-1 max-h-48 overflow-y-auto">
					<ReactMarkdown>{value}</ReactMarkdown>
				</div>
			);
		}
		// Short string
		return <span className="text-slate-200 font-medium">{value}</span>;
	}

	// Numbers
	return <span className="text-cyan-300 font-mono">{value}</span>;
};

const ForensicCard = ({ title, data, delay }) => {
	let parsedData = data;
	try {
		if (typeof data === "string") {
			parsedData = JSON.parse(data);
		}
	} catch (e) {
		parsedData = { raw: data };
	}

	return (
		<motion.div
			initial={{ opacity: 0, y: 10 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: delay * 0.1 }}
			className="bg-slate-900/40 p-5 rounded-xl border border-slate-700/50 hover:border-slate-500/50 transition-colors shadow-sm overflow-hidden"
		>
			<div className="text-xs font-bold text-cyan-400 uppercase tracking-widest mb-4 border-b border-slate-800 pb-2 flex justify-between items-center">
				{title}
				{parsedData.verdict && (
					<span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
						{parsedData.verdict}
					</span>
				)}
			</div>

			<div className="space-y-3">
				{Object.entries(parsedData).map(([key, value]) => {
					// Skip redundant keys
					if (key === "tool" || key === "verdict") return null;

					return (
						<div key={key}>
							<div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
								{formatKey(key)}
							</div>
							<div className="text-sm">
								<DataNode value={value} />
							</div>
						</div>
					);
				})}
			</div>
		</motion.div>
	);
};

const ForensicsView = ({ data }) => {
	if (!data) return null;
	return (
		<div className="bg-slate-950/30 rounded-xl border border-slate-800 overflow-hidden">
			<div className="p-4 bg-slate-900/50 border-b border-slate-800 flex justify-between items-center">
				<h4 className="font-bold text-slate-200">Evidence Analysis</h4>
				<div className="flex gap-2">
					<div className="hidden sm:block text-xs font-mono text-slate-500">
						{Object.keys(data).length} TOOLS RAN
					</div>
				</div>
			</div>

			<div className="p-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
				{Object.entries(data).map(([key, value], idx) => (
					<ForensicCard
						key={key}
						title={key.replace(/_/g, " ")}
						data={value}
						delay={idx}
					/>
				))}
			</div>
		</div>
	);
};
export default ForensicsView;
