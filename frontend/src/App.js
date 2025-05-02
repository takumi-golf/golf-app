import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import RecommendationForm from './components/RecommendationForm';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1B5E20', // ゴルフコースのグリーンをイメージした深い緑
    },
    secondary: {
      main: '#F57C00', // アクセントカラーとしてオレンジ
    },
    background: {
      default: '#F5F5F5',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: [
      'Noto Sans JP',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h3: {
      fontWeight: 700,
      letterSpacing: '0.05em',
    },
    h5: {
      fontWeight: 500,
      letterSpacing: '0.02em',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #E8F5E9 0%, #F5F5F5 100%)',
          py: 4,
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ mb: 6, textAlign: 'center' }}>
            <Typography
              variant="h3"
              component="h1"
              gutterBottom
              sx={{
                color: 'primary.main',
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
              }}
            >
              SwingFit Pro
            </Typography>
            <Typography
              variant="h5"
              component="h2"
              gutterBottom
              color="text.secondary"
              sx={{ mb: 2 }}
            >
              あなたに最適なゴルフクラブセットを見つけましょう
            </Typography>
            <Typography
              variant="subtitle1"
              color="text.secondary"
              sx={{ maxWidth: '800px', mx: 'auto' }}
            >
              スイングデータとプレイスタイルを分析し、あなたのゴルフをレベルアップするクラブセットを提案します
            </Typography>
          </Box>
          <RecommendationForm />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 