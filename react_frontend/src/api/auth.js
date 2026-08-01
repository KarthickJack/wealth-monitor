import api from "./client";

export async function registerUser(username, password) {
  const { data } = await api.post("/auth/register", { username, password });
  return data;
}

export async function loginUser(username, password) {
  const { data } = await api.post("/auth/login", { username, password });
  return data;
}

export async function fetchMe() {
  const { data } = await api.get("/auth/me");
  return data;
}
