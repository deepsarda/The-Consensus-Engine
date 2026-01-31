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
			const reader = new FileReader();
			reader.onloadend = () => {
				setPreview(reader.result);
			};
			reader.readAsDataURL(file);
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
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			className="w-full max-w-2xl bg-slate-800/50 backdrop-blur-xl p-8 rounded-2xl border border-slate-700 shadow-2xl"
		>
			<h2 className="text-2xl font-bold mb-6 bg-linear-to-r from-cyan-400 to-blue-600 bg-clip-text text-transparent">
				Initiate Investigation
			</h2>

			<form onSubmit={handleSubmit} className="space-y-6">
				<div>
					<label className="block text-sm font-medium text-slate-300 mb-2">
						Claim / Statement
					</label>
					<textarea
						value={claim}
						onChange={(e) => setClaim(e.target.value)}
						className="w-full bg-slate-900/50 border border-slate-700 rounded-xl p-4 text-white focus:ring-2 focus:ring-cyan-500 outline-none transition-all placeholder:text-slate-600"
						placeholder="e.g. A shark swimming in a flooded subway station..."
						rows={3}
						required
					/>
				</div>

				<div>
					<label className="block text-sm font-medium text-slate-300 mb-2">
						Evidence (Image)
					</label>
					<div
						onClick={() => fileInputRef.current?.click()}
						className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
							preview
								? "border-cyan-500/50 bg-cyan-900/10"
								: "border-slate-700 hover:border-slate-500 hover:bg-slate-800/50"
						}`}
					>
						<input
							type="file"
							ref={fileInputRef}
							onChange={handleImageChange}
							className="hidden"
							accept="image/*"
						/>

						<AnimatePresence mode="wait">
							{preview ? (
								<motion.div
									key="preview"
									initial={{ opacity: 0, scale: 0.9 }}
									animate={{ opacity: 1, scale: 1 }}
									exit={{ opacity: 0, scale: 0.9 }}
									className="relative"
								>
									<img
										src={preview}
										alt="Preview"
										className="max-h-64 mx-auto rounded-lg shadow-lg"
									/>
									<button
										type="button"
										onClick={(e) => {
											e.stopPropagation();
											setPreview(null);
											setImage(null);
										}}
										className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
									>
										<svg
											className="w-4 h-4"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												strokeLinecap="round"
												strokeLinejoin="round"
												strokeWidth="2"
												d="M6 18L18 6M6 6l12 12"
											/>
										</svg>
									</button>
								</motion.div>
							) : (
								<motion.div
									key="placeholder"
									initial={{ opacity: 0 }}
									animate={{ opacity: 1 }}
									exit={{ opacity: 0 }}
									className="space-y-2 text-slate-400"
								>
									<svg
										className="w-12 h-12 mx-auto text-slate-600"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth="1.5"
											d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
										/>
									</svg>
									<p>Click to upload or drag and drop</p>
									<p className="text-xs text-slate-500">SVG, PNG, JPG or GIF</p>
								</motion.div>
							)}
						</AnimatePresence>
					</div>
				</div>

				<button
					type="submit"
					disabled={!claim || !preview}
					className={`w-full py-4 rounded-xl font-bold tracking-wide transition-all ${
						claim && preview
							? "bg-linear-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 transform hover:-translate-y-0.5"
							: "bg-slate-800 text-slate-500 cursor-not-allowed"
					}`}
				>
					ANALYZE
				</button>
			</form>
		</motion.div>
	);
};

export default InputSection;
