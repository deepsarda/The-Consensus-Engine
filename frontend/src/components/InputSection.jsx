import { AnimatePresence, motion } from "framer-motion";
import React, { useRef, useState } from "react";

const InputSection = ({ onSubmit }) => {
	const [claim, setClaim] = useState("");
	const [image, setImage] = useState(null);
	const [preview, setPreview] = useState(null);
	const fileInputRef = useRef(null);

	const handleImageChange = (e) => {
		const file = e.target.files[0];
		if (file) {
			setImage(file);
			if (file.type.startsWith("video/")) {
				const video = document.createElement("video");
				video.preload = "metadata";
				video.onloadedmetadata = () => {
					video.currentTime = 0.1; // Small offset to avoid black frames
				};
				video.onseeked = () => {
					const canvas = document.createElement("canvas");
					canvas.width = video.videoWidth;
					canvas.height = video.videoHeight;
					const ctx = canvas.getContext("2d");
					ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
					setPreview(canvas.toDataURL("image/jpeg"));
					URL.revokeObjectURL(video.src);
				};
				video.onerror = () => {
					console.error("Error loading video");
					alert("Failed to process video file.");
					URL.revokeObjectURL(video.src);
				};
				video.src = URL.createObjectURL(file);
			} else {
				const reader = new FileReader();
				reader.onloadend = () => {
					setPreview(reader.result);
				};
				reader.readAsDataURL(file);
			}
		}
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		if (claim && preview) {
			onSubmit(claim, preview);
		}
	};

	return (
		<motion.div
			initial={{ opacity: 0, scale: 0.95 }}
			animate={{ opacity: 1, scale: 1 }}
			className="w-full max-w-2xl relative group"
		>
			<div className="relative bg-black/80 backdrop-blur-xl p-8 border border-cyan-500/30 w-full clip-path-angle">
				<div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-cyan-400"></div>
				<div className="absolute top-0 right-0 w-2 h-2 border-t-2 border-r-2 border-cyan-400"></div>
				<div className="absolute bottom-0 left-0 w-2 h-2 border-b-2 border-l-2 border-cyan-400"></div>
				<div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-cyan-400"></div>

				<h2
					className="text-2xl font-display font-bold mb-8 text-cyan-400 uppercase tracking-[0.2em] glitch-text"
					data-text="Initiate Investigation"
				>
					Initiate Investigation
				</h2>

				<form onSubmit={handleSubmit} className="space-y-8">
					<div className="group/input">
						<label className="block text-xs font-mono text-cyan-500/70 mb-2 uppercase tracking-widest group-focus-within/input:text-cyan-400 transition-colors">
							&gt; Target_Statement
						</label>
						<div className="relative">
							<textarea
								value={claim}
								onChange={(e) => setClaim(e.target.value)}
								className="w-full bg-slate-900/50 border-b border-slate-700 text-slate-200 font-mono p-4 focus:border-cyan-500 focus:bg-cyan-950/20 outline-none transition-all placeholder:text-slate-700 resize-none h-32"
								placeholder="// Enter claim for verification..."
								required
							/>
							<div className="absolute bottom-0 left-0 h-[1px] w-0 bg-cyan-500 transition-all duration-500 group-focus-within/input:w-full"></div>
						</div>
					</div>

					<div className="group/evidence">
						<label className="block text-xs font-mono text-cyan-500/70 mb-2 uppercase tracking-widest group-focus-within/evidence:text-cyan-400 transition-colors">
							&gt; Visual_Evidence
						</label>
						<div
							onClick={() => fileInputRef.current?.click()}
							className={`relative border border-dashed p-8 text-center cursor-pointer transition-all overflow-hidden ${
								preview
									? "border-cyan-500 bg-cyan-950/30"
									: "border-slate-700 hover:border-cyan-500/50 hover:bg-slate-900/50"
							}`}
						>
							{/* Scanline for upload area */}
							<div className="absolute inset-0 bg-linear-to-b from-transparent via-cyan-500/5 to-transparent bg-size[100%_200%] animate-scanline pointer-events-none"></div>

							<input
								type="file"
								ref={fileInputRef}
								onChange={handleImageChange}
								className="hidden"
								accept="image/*,video/*"
							/>

							<AnimatePresence mode="wait">
								{preview ? (
									<motion.div
										key="preview"
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										exit={{ opacity: 0 }}
										className="relative"
									>
										<div className="relative inline-block border border-cyan-500/50 p-1">
											<img
												src={preview}
												alt="Preview"
												className="max-h-64 mx-auto opacity-80"
											/>
											{/* Image overlay effect */}
											<div className="absolute inset-0 bg-cyan-500/10 mix-blend-overlay"></div>
										</div>
										<button
											type="button"
											onClick={(e) => {
												e.stopPropagation();
												setPreview(null);
												setImage(null);
											}}
											className="absolute -top-3 -right-3 bg-slate-900 border border-red-500 text-red-500 hover:bg-red-500 hover:text-white transition-colors w-6 h-6 flex items-center justify-center font-mono text-xs"
										>
											X
										</button>
									</motion.div>
								) : (
									<motion.div
										key="placeholder"
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										exit={{ opacity: 0 }}
										className="space-y-2"
									>
										<div className="w-12 h-12 mx-auto border border-slate-600 flex items-center justify-center text-slate-600 group-hover/evidence:border-cyan-500 group-hover/evidence:text-cyan-500 transition-colors">
											<span className="text-2xl font-thin">+</span>
										</div>
										<p className="font-mono text-sm text-slate-500 group-hover/evidence:text-cyan-400 transition-colors">
											[UPLOAD_FILE]
										</p>
									</motion.div>
								)}
							</AnimatePresence>
						</div>
					</div>

					<button
						type="submit"
						disabled={!claim || !preview}
						className={`w-full py-4 font-display text-xl tracking-widest uppercase transition-all relative overflow-hidden group/btn ${
							claim && preview
								? "bg-cyan-600/20 border border-cyan-500 text-cyan-400 hover:bg-cyan-500 hover:text-black hover:shadow-[0_0_20px_rgba(34,211,238,0.5)]"
								: "bg-slate-900/50 border border-slate-800 text-slate-600 cursor-not-allowed"
						}`}
					>
						<span className="relative z-10">
							{claim && preview ? "Execute_Analysis" : "Awaiting_Input..."}
						</span>
						{claim && preview && (
							<div className="absolute inset-0 -translate-x-full group-hover/btn:translate-x-0 bg-cyan-500 transition-transform duration-300 ease-out -z-0"></div>
						)}
					</button>
				</form>
			</div>
		</motion.div>
	);
};

export default InputSection;
