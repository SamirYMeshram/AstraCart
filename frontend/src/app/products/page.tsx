'use client';
import { Filter, Plus, Search } from 'lucide-react';
import { ProductTable } from '@/components/DataTable';
import { GlassCard } from '@/components/GlassCard';
import { ProductCard } from '@/components/ProductCard';
import { Shell } from '@/components/Shell';
import { products } from '@/lib/mock-data';
export default function Products(){ return <Shell title="Product Management" subtitle="Seller-ready catalog operations with search, category filters, thumbnails, low-stock badges and edit actions."><GlassCard className="mb-4"><div className="grid gap-3 lg:grid-cols-[1fr_auto_auto_auto]"><div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[.04] px-4 py-3 text-slate-400"><Search size={18}/> Search products, SKU, seller...</div><button className="rounded-2xl border border-white/10 bg-white/[.04] px-5 py-3 text-white"><Filter size={18} className="inline"/> Category</button><button className="rounded-2xl border border-white/10 bg-white/[.04] px-5 py-3 text-white">Stock filter</button><button className="rounded-2xl bg-cyan-300 px-5 py-3 font-semibold text-slate-950"><Plus size={18} className="inline"/> Add product</button></div></GlassCard><div className="grid gap-4 xl:grid-cols-[1.1fr_.9fr]"><GlassCard><h2 className="mb-4 text-xl font-semibold text-white">Catalog table</h2><ProductTable products={products}/></GlassCard><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-1">{products.slice(0,4).map(p=><ProductCard key={p.id} product={p}/>)}</div></div></Shell> }
