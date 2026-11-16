import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#070B14] text-white p-4 text-center">
      <div className="w-16 h-16 rounded-2xl bg-[#E80071]/20 border border-[#E80071]/40 flex items-center justify-center text-3xl mb-4">
        👑
      </div>
      <h2 className="text-3xl font-extrabold font-display">404 - Page Not Found</h2>
      <p className="text-sm text-slate-400 mt-2 max-w-md">
        The requested scouting dossier or war room view does not exist.
      </p>
      <Link
        href="/"
        className="mt-6 px-5 py-2.5 rounded-xl bg-[#E80071] hover:bg-[#B80059] text-white font-bold text-xs uppercase tracking-wider transition-all"
      >
        Return to War Room
      </Link>
    </div>
  );
}
