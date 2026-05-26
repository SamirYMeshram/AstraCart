'use client';
import { BellRing, Mail, MessageSquareText } from 'lucide-react';
import { GlassCard } from '@/components/GlassCard';
import { Shell } from '@/components/Shell';
import { notifications } from '@/lib/mock-data';
export default function Notifications(){ return <Shell title="Notifications" subtitle="Mock email, SMS and in-app notification center backed by Celery-ready notification-service tasks."><GlassCard><div className="space-y-3">{notifications.map(n=><div key={n.id} className={`rounded-3xl border p-4 ${n.read?'border-white/10 bg-white/[.03]':'border-cyan-300/30 bg-cyan-300/10'}`}><div className="flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10 text-cyan-200">{n.channel==='EMAIL'?<Mail/>:n.channel==='SMS'?<MessageSquareText/>:<BellRing/>}</div><div className="flex-1"><div className="font-semibold text-white">{n.title}</div><div className="text-sm text-slate-400">{n.message}</div></div><span className="text-xs text-slate-500">{n.time}</span></div></div>)}</div></GlassCard></Shell> }
