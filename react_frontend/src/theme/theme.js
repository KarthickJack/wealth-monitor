import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#0B6E4F",
    },
    secondary: {
      main: "#1F2933",
    },
    background: {
      default: "#F4F7F5",
      paper: "#FFFFFF",
    },
  },
  typography: {
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif',
    h4: { letterSpacing: "-0.02em" },
  },
  shape: {
    borderRadius: 10,
  },
});

export default theme;
