export type Status = 'PENDING' | 'CONFIRMED' | 'PAID' | 'PACKED' | 'SHIPPED' | 'OUT_FOR_DELIVERY' | 'DELIVERED' | 'CANCELLED' | 'REFUNDED';
export type Product = { id: string; title: string; category: string; price: number; discount_price?: number; stock_quantity: number; rating: number; image: string; status: string; sku: string };
export type Order = { id: string; customer: string; email: string; total: number; status: Status; payment: 'SUCCESS' | 'FAILED' | 'INITIATED' | 'REFUNDED'; items: number; timeline: string[] };
export type Notification = { id: string; title: string; message: string; read: boolean; event: string; channel: string; time: string };
export type ServiceHealth = { name: string; latency: string; healthy: boolean; cpu: number; memory: number };
