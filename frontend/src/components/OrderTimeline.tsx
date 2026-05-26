'use client';
export function OrderTimeline({ steps }: { steps: string[] }) { return <div className="space-y-4">{steps.map((s,i)=><div key={s} className="flex gap-3"><div className="mt-1 h-3 w-3 rounded-full bg-cyan-300 shadow-glow"/><div><div className="text-sm font-medium text-white">{s}</div><div className="text-xs text-slate-500">Audit event #{i+1}</div></div></div>)}</div> }
