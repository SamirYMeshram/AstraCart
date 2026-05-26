import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AstraCart Enterprise Platform',
  description: 'Premium microservices e-commerce SaaS platform demo'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en" className="dark"><body>{children}</body></html>;
}
