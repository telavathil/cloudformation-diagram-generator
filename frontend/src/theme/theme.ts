import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  components: {
    MuiContainer: {
      styleOverrides: {
        root: {
          maxWidth: '100%',
          width: '100%',
          margin: 0,
        },
      },
    },
  },
  palette: {
    mode: 'dark',
    primary: {
      main: '#646cff',
      dark: '#535bf2',
    },
    background: {
      default: '#242424',
      paper: '#fff',
    },
  },
}); 