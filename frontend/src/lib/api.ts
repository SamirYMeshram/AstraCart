import { notifications, orders, products, serviceHealth } from './mock-data';
const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080';
async function safeGet<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${base}${path}`, { cache: 'no-store' });
    if (!res.ok) return fallback;
    const json = await res.json();
    return (json.data ?? fallback) as T;
  } catch { return fallback; }
}
export const api = {
  products: () => safeGet('/products', products),
  orders: () => safeGet('/orders', orders),
  notifications: () => safeGet('/notifications', notifications),
  health: () => safeGet('/health', { dependencies: serviceHealth })
};
