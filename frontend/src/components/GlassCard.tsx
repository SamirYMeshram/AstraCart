'use client';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
export function GlassCard({ children, className, delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  return <motion.div initial={{ opacity: 0, y: 18, scale: .98 }} animate={{ opacity: 1, y: 0, scale: 1 }} transition={{ duration: .55, delay }} whileHover={{ y: -4 }} className={cn('glass neon-border rounded-3xl p-5', className)}>{children}</motion.div>;
}
