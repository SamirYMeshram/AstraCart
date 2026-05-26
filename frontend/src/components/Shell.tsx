'use client';
import { motion } from 'framer-motion';
import { AnimatedSidebar } from './AnimatedSidebar';
import { CommandSearch } from './CommandSearch';
export function Shell({ children, title, subtitle }: { children: React.ReactNode; title: string; subtitle: string }) { return <div className="flex min-h-screen"><AnimatedSidebar/><main className="min-w-0 flex-1 p-4 lg:p-8"><motion.div initial={{opacity:0,y:-12}} animate={{opacity:1,y:0}} className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><p className="text-sm uppercase tracking-[.35em] text-cyan-200/70">AstraCart OS</p><h1 className="mt-2 text-3xl font-semibold tracking-tight text-white lg:text-5xl">{title}</h1><p className="mt-3 max-w-2xl text-slate-400">{subtitle}</p></div><CommandSearch/></motion.div>{children}</main></div> }
