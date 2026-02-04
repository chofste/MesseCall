const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "API request failed");
  }
  return response.json();
};

export const fetchEvents = async () =>
  handleResponse(await fetch(`${API_BASE}/events`));

export const fetchPublicEvents = async (churchId) =>
  handleResponse(await fetch(`${API_BASE}/public/churches/${churchId}/events`));

export const createSwapRequest = async (payload) =>
  handleResponse(
    await fetch(`${API_BASE}/swap-requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
  );
