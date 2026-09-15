import { NavLink } from "react-router-dom";
import {
  Home,
  History,
  Bookmark,
  Settings, 
  Play,
  Bot,
} from "lucide-react";

const navigation = [
  { name: "Home", path: "/", icon: Home },
  { name: "History", path: "/history", icon: History },
  { name: "Saved Videos", path: "/saved", icon: Bookmark },
  { name: "Settings", path: "/settings", icon: Settings },
];


export default function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col bg-slate-950 p-4 text-white md:flex">
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="rounded-xl bg-red-600 p-2">
          <Play size={22} />
        </div>

        <div>
          <h1 className="font-bold">YouTube AI</h1>
          <p className="text-xs text-slate-400">Chatbot</p>
        </div>
      </div>

      <nav className="space-y-2">
        {navigation.map(({ name, path, icon: Icon }) => (
          <NavLink
            key={name}
            to={path}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >
            <Icon size={19} />
            {name}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto rounded-xl border border-slate-700 p-4">
        <Bot className="mb-2 text-blue-400" size={22} />
        <p className="text-sm font-medium">Powered by LangChain</p>
        <p className="mt-1 text-xs text-slate-400">
          Ask questions about YouTube videos using AI.
        </p>
      </div>
    </aside>
  );
}