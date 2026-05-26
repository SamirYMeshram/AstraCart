'use client';
import { Search, Sparkles } from 'lucide-react';
export function CommandSearch(){ return <div className="flex min-w-72 items-center gap-3 rounded-2xl border border-white/10 bg-white/[.04] px-4 py-3 text-slate-400 shadow-panel backdrop-blur-xl"><Search size={18}/><span className="flex-1 text-sm">Search orders, products, users...</span><kbd className="rounded-lg border border-white/10 bg-white/[.06] px-2 py-1 text-xs">⌘K</kbd><Sparkles className="text-cyan-200" size={16}/></div> }
