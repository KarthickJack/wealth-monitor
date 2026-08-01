import api from "./client";

export async function getSummary() {
  const { data } = await api.get("/reports/summary");
  return data;
}

export async function getCategoryReport() {
  const { data } = await api.get("/reports/by-category");
  return data;
}

export async function getMonthReport() {
  const { data } = await api.get("/reports/by-month");
  return data;
}

export async function listCategories() {
  const { data } = await api.get("/categories");
  return data;
}

export async function listParties() {
  const { data } = await api.get("/parties");
  return data;
}

export async function listTransactions() {
  const { data } = await api.get("/transactions");
  return data;
}

export async function createTransaction(payload) {
  const { data } = await api.post("/transactions", payload);
  return data;
}

export async function updateTransaction(id, payload) {
  const { data } = await api.put(`/transactions/${id}`, payload);
  return data;
}

export async function deleteTransaction(id) {
  await api.delete(`/transactions/${id}`);
}
