'use client';
import { motion } from 'framer-motion';
import type { Order, Status } from '@/lib/types';
import { money } from '@/lib/utils';
import { StatusBadge } from './StatusBadge';
const cols: Status[] = ['PENDING','PAID','SHIPPED','DELIVERED'];
export function OrderPipeline({ orders }: { orders: Order[] }) { return <div className="grid gap-4 xl:grid-cols-4">{cols.map((c,idx)=><div key={c} className="rounded-3xl border border-white/10 bg-white/[.03] p-4"><div className="mb-4 flex items-center justify-between"><StatusBadge status={c}/><span className="text-xs text-slate-500">{orders.filter(o=>o.status===c).length} orders</span></div><div className="space-y-3">{orders.filter(o=>o.status===c).map((o,i)=><motion.div key={o.id} initial={{opacity:0,y:16}} animate={{opacity:1,y:0}} transition={{delay:(idx+i)*.05}} whileHover={{scale:1.02}} className="rounded-2xl border border-white/10 bg-slate-950/70 p-4"><div className="flex justify-between text-sm"><span className="font-semibold text-white">{o.id}</span><span>{money(o.total)}</span></div><p className="mt-2 text-sm text-slate-400">{o.customer}</p><p className="text-xs text-slate-500">{o.items} items • {o.payment}</p></motion.div>)}</div></div>)}</div> }
