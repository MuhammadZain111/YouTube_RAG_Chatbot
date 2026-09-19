import { Menu, UserCircle } from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <Menu className="text-slate-500 md:hidden" size={22} />
        <h2 className="text-lg font-semibold">YouTube AI Workspace</h2>
      </div>

      <div className="flex items-center gap-2 text-sm text-slate-600">
        <UserCircle size={24} />
        <span className="hidden sm:block">Guest User</span>
      </div>
    </header>
  );
}
