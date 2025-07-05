import { API_BASE } from "./api";

export async function fetchStatus(token: string) {
  const res = await fetch(`${API_BASE}/status?token=${token}`);
  if (!res.ok) {
    throw new Error("Invalid token or failed to fetch status.");
  }
  return await res.json();
}

export async function triggerRetrain(token: string) {
  const res = await fetch(`${API_BASE}retrain/`, {
    method: "POST",
    body: new URLSearchParams({ token }),
  });
  if (!res.ok) {
    throw new Error("Retraining failed.");
  }
  return await res.json();
}