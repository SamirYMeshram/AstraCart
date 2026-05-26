'use client';
import { OrderPipeline } from '@/components/OrderPipeline';
import { OrderTimeline } from '@/components/OrderTimeline';
import { GlassCard } from '@/components/GlassCard';
import { Shell } from '@/components/Shell';
import { orders } from '@/lib/mock-data';
export default function Orders(){ return <Shell title="Order Management" subtitle="Kanban-style order lifecycle with customer details, payment state, timeline drawer and status transition actions."><OrderPipeline orders={orders}/><div className="mt-4 grid gap-4 lg:grid-cols-3"><GlassCard className="lg:col-span-2"><h2 className="mb-4 text-xl font-semibold text-white">Priority order timeline</h2><OrderTimeline steps={orders[0].timeline}/></GlassCard><GlassCard><h2 className="text-xl font-semibold text-white">Status action</h2><p className="mt-2 text-sm text-slate-400">Move selected orders through CONFIRMED → PAID → PACKED → SHIPPED → DELIVERED with RBAC-protected backend endpoints.</p><button className="mt-5 w-full rounded-2xl bg-cyan-300 px-5 py-3 font-semibold text-slate-950">Update order status</button></GlassCard></div></Shell> }
