'use client';
import { CheckCircle2 } from 'lucide-react';
export function CheckoutStepper(){ return <div className="grid gap-3 md:grid-cols-4">{['Cart validated','Order created','Payment simulated','Confirmation sent'].map((s,i)=><div key={s} className="rounded-2xl border border-white/10 bg-white/[.04] p-4 text-sm text-slate-300"><CheckCircle2 className="mb-3 text-emerald-300" size={20}/>{s}<div className="mt-1 text-xs text-slate-500">Step {i+1}</div></div>)}</div> }
