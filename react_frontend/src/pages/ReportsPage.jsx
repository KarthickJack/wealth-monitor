import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { getCategoryReport, getMonthReport } from "../api/finance";
import { formatMoney, monthName, typeLabel } from "../utils/format";

export default function ReportsPage() {
  const [byCategory, setByCategory] = useState([]);
  const [byMonth, setByMonth] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCategoryReport(), getMonthReport()])
      .then(([categories, months]) => {
        setByCategory(categories);
        setByMonth(months);
      })
      .catch((err) => setError(err.response?.data?.detail || "Failed to load reports"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: "grid", placeItems: "center", minHeight: 240 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Reports
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        Totals are aggregated from non-deleted transactions.
      </Typography>
      {error ? (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      ) : null}

      <Paper sx={{ p: 2, mb: 3, overflowX: "auto" }}>
        <Typography variant="h6" gutterBottom>
          By category
        </Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Category</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {byCategory.length === 0 ? (
              <TableRow>
                <TableCell colSpan={3}>No data yet</TableCell>
              </TableRow>
            ) : (
              byCategory.map((row) => (
                <TableRow key={`${row.category_id}-${row.transaction_type}-${row.category_name}`}>
                  <TableCell>{row.category_name}</TableCell>
                  <TableCell>{typeLabel(row.transaction_type)}</TableCell>
                  <TableCell align="right">{formatMoney(row.total)}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Paper>

      <Paper sx={{ p: 2, overflowX: "auto" }}>
        <Typography variant="h6" gutterBottom>
          By month
        </Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Month</TableCell>
              <TableCell align="right">Income</TableCell>
              <TableCell align="right">Expense</TableCell>
              <TableCell align="right">Net</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {byMonth.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4}>No data yet</TableCell>
              </TableRow>
            ) : (
              byMonth.map((row) => (
                <TableRow key={`${row.year}-${row.month}`}>
                  <TableCell>
                    {monthName(row.month)} {row.year}
                  </TableCell>
                  <TableCell align="right">{formatMoney(row.total_income)}</TableCell>
                  <TableCell align="right">{formatMoney(row.total_expense)}</TableCell>
                  <TableCell align="right">{formatMoney(row.net)}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
