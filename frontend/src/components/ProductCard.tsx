'use client';
import { motion } from 'framer-motion';
import { ShoppingCart, Star } from 'lucide-react';
import type { Product } from '@/lib/types';
import { money } from '@/lib/utils';
import { StatusBadge } from './StatusBadge';
export function ProductCard({ product, onAdd }: { product: Product; onAdd?: (p: Product)=>void }) { return <motion.div whileHover={{y:-7, scale:1.01}} className="glass overflow-hidden rounded-3xl"><div className="h-44 bg-gradient-to-br from-cyan-400/20 via-fuchsia-400/10 to-emerald-400/20 p-4"><div className="h-full rounded-2xl border border-white/10 bg-slate-950/50" /></div><div className="p-5"><div className="flex items-start justify-between gap-3"><div><h3 className="font-semibold text-white">{product.title}</h3><p className="text-sm text-slate-400">{product.category}</p></div><StatusBadge status={product.stock_quantity<=5?'LOW_STOCK':'ACTIVE'}/></div><div className="mt-4 flex items-center justify-between"><div><p className="text-xl font-semibold text-white">{money(product.discount_price || product.price)}</p><p className="flex items-center gap-1 text-xs text-amber-200"><Star size={14} fill="currentColor"/> {product.rating.toFixed(1)}</p></div><button onClick={()=>onAdd?.(product)} className="rounded-2xl bg-cyan-300 px-4 py-3 text-slate-950 shadow-glow transition hover:bg-cyan-200"><ShoppingCart size={18}/></button></div></div></motion.div> }
