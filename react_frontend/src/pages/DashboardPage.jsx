import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  CircularProgress,
  Paper,
  Typography,
} from "@mui/material";
import { getSummary } from "../api/finance";
import { formatMoney } from "../utils/format";

function StatCard({ label, value, helper }) {
  return (
    <Paper sx={{ p: 3, height: "100%" }}>
      <Typography color="text.secondary" gutterBottom>
        {label}
      </Typography>
      <Typography variant="h4" fontWeight={700}>
        {value}
      </Typography>
      {helper ? (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {helper}
        </Typography>
      ) : null}
    </Paper>
  );
}

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSummary()
      .then(setSummary)
      .catch((err) => setError(err.response?.data?.detail || "Failed to load summary"))
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
        Dashboard
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        Net wealth position = total income − total expenses.
      </Typography>
      {error ? <Alert severity="error">{error}</Alert> : null}
      {summary ? (
        <Box
          sx={{
            display: "grid",
            gap: 2,
            gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" },
          }}
        >
          <StatCard label="Total Income" value={formatMoney(summary.total_income)} />
          <StatCard label="Total Expense" value={formatMoney(summary.total_expense)} />
          <StatCard
            label="Net"
            value={formatMoney(summary.net)}
            helper="This is calculated, not stored as a single balance field."
          />
        </Box>
      ) : null}
    </Box>
  );
}
