export const TYPE_EXPENSE = 0;
export const TYPE_INCOME = 1;

export function formatMoney(value) {
  const amount = Number(value || 0);
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(amount);
}

export function typeLabel(type) {
  return Number(type) === TYPE_INCOME ? "Income" : "Expense";
}

export function toDateInputValue(value) {
  const date = value ? new Date(value) : new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function monthName(monthNumber) {
  return new Date(2000, monthNumber - 1, 1).toLocaleString("en", { month: "short" });
}
