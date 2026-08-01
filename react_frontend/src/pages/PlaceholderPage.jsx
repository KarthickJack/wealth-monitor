import { Paper, Typography } from "@mui/material";

export default function PlaceholderPage({ title, note }) {
  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight={700}>
        {title}
      </Typography>
      <Typography color="text.secondary">{note}</Typography>
    </Paper>
  );
}
