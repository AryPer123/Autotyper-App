// Simple helper functions to make API calls to the Flask backend.

const BASE_URL = "http://127.0.0.1:5000";  // or wherever your Flask server is running

export async function registerUser(email, password) {
  const response = await fetch(`${BASE_URL}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
}

export async function loginUser(email, password) {
  const response = await fetch(`${BASE_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
}

export async function subscribeUser(email, days) {
  const response = await fetch(`${BASE_URL}/api/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, days }),
  });
  return response.json();
}

export async function verifySubscription(email) {
  const response = await fetch(`${BASE_URL}/api/verify?email=${email}`, {
    method: "GET",
  });
  return response.json();
}
