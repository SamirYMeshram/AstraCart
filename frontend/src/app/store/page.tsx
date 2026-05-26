'use client';
import { useState } from 'react';
import { CartDrawer } from '@/components/CartDrawer';
import { CheckoutStepper } from '@/components/CheckoutStepper';
import { GlassCard } from '@/components/GlassCard';
import { ProductCard } from '@/components/ProductCard';
import { Shell } from '@/components/Shell';
import { products } from '@/lib/mock-data';
import type { Product } from '@/lib/types';
export default function Store(){ const [cart,setCart]=useState<Product[]>([]); const [open,setOpen]=useState(false); return <Shell title="Customer Storefront" subtitle="Responsive storefront with category filters, product grid, cart drawer, checkout steps, mock payment and order confirmation flow."><GlassCard className="mb-4"><div className="flex flex-wrap items-center justify-between gap-3"><div className="flex flex-wrap gap-2">{['All','Electronics','Gaming','Fitness','Travel'].map(c=><button key={c} className="rounded-2xl border border-white/10 bg-white/[.04] px-4 py-2 text-sm text-slate-200">{c}</button>)}</div><button onClick={()=>setOpen(true)} className="rounded-2xl bg-cyan-300 px-5 py-3 font-semibold text-slate-950">Open Cart ({cart.length})</button></div></GlassCard><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{products.slice(0,12).map(p=><ProductCard key={p.id} product={p} onAdd={(prod)=>{setCart([...cart,prod]); setOpen(true)}}/>)}</div><GlassCard className="mt-4"><h2 className="mb-4 text-xl font-semibold text-white">Checkout flow</h2><CheckoutStepper/></GlassCard><CartDrawer open={open} items={cart} onClose={()=>setOpen(false)}/></Shell> }
