import { History as HistoryIcon } from "lucide-react";

export default function History() {
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="text-2xl font-bold">History</h1>

      <div className="mt-6 rounded-2xl border bg-white p-8 text-center">
        <HistoryIcon className="mx-auto mb-3 text-slate-400" size={40} />
        <p className="text-slate-500">
          Your video and chat history will appear here.
        </p>
      </div>
    </div>
  );
}
