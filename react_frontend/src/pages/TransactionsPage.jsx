import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import {
  createTransaction,
  deleteTransaction,
  listCategories,
  listParties,
  listTransactions,
  updateTransaction,
} from "../api/finance";
import {
  TYPE_EXPENSE,
  TYPE_INCOME,
  formatMoney,
  toDateInputValue,
  typeLabel,
} from "../utils/format";

const emptyForm = {
  transaction_date: toDateInputValue(),
  transaction_type: TYPE_EXPENSE,
  amount: "",
  category_id: "",
  party_id: "",
  description: "",
};

export default function TransactionsPage() {
  const [rows, setRows] = useState([]);
  const [categories, setCategories] = useState([]);
  const [parties, setParties] = useState([]);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = async () => {
    const [txns, cats, parts] = await Promise.all([
      listTransactions(),
      listCategories(),
      listParties(),
    ]);
    setRows(txns);
    setCategories(cats);
    setParties(parts);
  };

  useEffect(() => {
    load().catch((err) => setError(err.response?.data?.detail || "Failed to load data"));
  }, []);

  const filteredCategories = useMemo(
    () => categories.filter((c) => c.transaction_type === Number(form.transaction_type)),
    [categories, form.transaction_type],
  );

  const categoryName = (id) => categories.find((c) => c.id === id)?.name || "—";
  const partyName = (id) => parties.find((p) => p.id === id)?.name || "—";

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setOpen(true);
  };

  const openEdit = (row) => {
    setEditing(row);
    setForm({
      transaction_date: toDateInputValue(row.transaction_date),
      transaction_type: row.transaction_type,
      amount: String(row.amount),
      category_id: row.category_id || "",
      party_id: row.party_id || "",
      description: row.description || "",
    });
    setOpen(true);
  };

  const onSave = async () => {
    setSaving(true);
    setError("");
    const payload = {
      transaction_date: new Date(`${form.transaction_date}T12:00:00`).toISOString(),
      transaction_type: Number(form.transaction_type),
      amount: form.amount,
      category_id: form.category_id || null,
      party_id: form.party_id || null,
      description: form.description || null,
    };
    try {
      if (editing) {
        await updateTransaction(editing.id, payload);
      } else {
        await createTransaction(payload);
      }
      setOpen(false);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const onDelete = async (row) => {
    if (!window.confirm("Soft-delete this transaction?")) return;
    try {
      await deleteTransaction(row.id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <Box>
      <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" gap={2} mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Transactions
          </Typography>
          <Typography color="text.secondary">
            Amount is always positive. Type decides income vs expense.
          </Typography>
        </Box>
        <Button variant="contained" onClick={openCreate}>
          Add transaction
        </Button>
      </Stack>

      {error ? (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      ) : null}

      <Box sx={{ overflowX: "auto", bgcolor: "background.paper", borderRadius: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Party</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7}>
                  <Typography color="text.secondary" sx={{ py: 3 }}>
                    No transactions yet. Add salary income or a food expense to begin.
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row) => (
                <TableRow key={row.id} hover>
                  <TableCell>{toDateInputValue(row.transaction_date)}</TableCell>
                  <TableCell>{typeLabel(row.transaction_type)}</TableCell>
                  <TableCell>{formatMoney(row.amount)}</TableCell>
                  <TableCell>{categoryName(row.category_id)}</TableCell>
                  <TableCell>{partyName(row.party_id)}</TableCell>
                  <TableCell>{row.description || "—"}</TableCell>
                  <TableCell align="right">
                    <Button size="small" onClick={() => openEdit(row)}>
                      Edit
                    </Button>
                    <Button size="small" color="error" onClick={() => onDelete(row)}>
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Box>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>{editing ? "Edit transaction" : "Add transaction"}</DialogTitle>
        <DialogContent sx={{ display: "grid", gap: 2, pt: 1 }}>
          <TextField
            label="Date"
            type="date"
            value={form.transaction_date}
            onChange={(e) => setForm((f) => ({ ...f, transaction_date: e.target.value }))}
            InputLabelProps={{ shrink: true }}
          />
          <FormControl>
            <InputLabel>Type</InputLabel>
            <Select
              label="Type"
              value={form.transaction_type}
              onChange={(e) =>
                setForm((f) => ({
                  ...f,
                  transaction_type: e.target.value,
                  category_id: "",
                }))
              }
            >
              <MenuItem value={TYPE_EXPENSE}>Expense</MenuItem>
              <MenuItem value={TYPE_INCOME}>Income</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Amount"
            type="number"
            inputProps={{ min: 0.01, step: "0.01" }}
            value={form.amount}
            onChange={(e) => setForm((f) => ({ ...f, amount: e.target.value }))}
          />
          <FormControl>
            <InputLabel>Category</InputLabel>
            <Select
              label="Category"
              value={form.category_id}
              onChange={(e) => setForm((f) => ({ ...f, category_id: e.target.value }))}
            >
              <MenuItem value="">None</MenuItem>
              {filteredCategories.map((c) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl>
            <InputLabel>Party / channel</InputLabel>
            <Select
              label="Party / channel"
              value={form.party_id}
              onChange={(e) => setForm((f) => ({ ...f, party_id: e.target.value }))}
            >
              <MenuItem value="">None</MenuItem>
              {parties.map((p) => (
                <MenuItem key={p.id} value={p.id}>
                  {p.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            label="Description"
            value={form.description}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={onSave} disabled={saving || !form.amount}>
            {saving ? "Saving..." : "Save"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
