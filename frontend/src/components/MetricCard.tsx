'use client';
import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';
import { GlassCard } from './GlassCard';
export function MetricCard({ label, value, trend, icon: Icon, delay=0 }: { label: string; value: string; trend: string; icon: any; delay?: number }) {
  return <GlassCard delay={delay} className="overflow-hidden relative"><div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-cyan-400/10 blur-2xl" /><div className="flex items-start justify-between"><div><p className="text-sm text-slate-400">{label}</p><motion.h3 initial={{opacity:0}} animate={{opacity:1}} transition={{delay:.2+delay}} className="mt-3 text-3xl font-semibold tracking-tight text-white">{value}</motion.h3></div><div className="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 p-3 text-cyan-200"><Icon size={22}/></div></div><div className="mt-5 inline-flex items-center gap-1 rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-xs text-emerald-200"><ArrowUpRight size={14}/>{trend}</div></GlassCard>;
}
