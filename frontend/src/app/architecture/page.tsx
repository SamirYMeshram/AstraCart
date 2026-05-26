'use client';
import { ArchitectureDiagram } from '@/components/ArchitectureDiagram';
import { GlassCard } from '@/components/GlassCard';
import { ServiceHealthCard } from '@/components/ServiceHealthCard';
import { Shell } from '@/components/Shell';
import { serviceHealth } from '@/lib/mock-data';
export default function Architecture(){ return <Shell title="System Architecture" subtitle="Animated map of gateway, services, Redis, PostgreSQL and Celery workers with health indicators and communication paths."><ArchitectureDiagram/><GlassCard className="mt-4"><h2 className="mb-4 text-xl font-semibold text-white">Runtime nodes</h2><div className="grid gap-3 md:grid-cols-3 xl:grid-cols-5">{serviceHealth.map(s=><ServiceHealthCard key={s.name} service={s}/>)}</div></GlassCard></Shell> }
