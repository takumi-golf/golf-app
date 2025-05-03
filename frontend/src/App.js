import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import RecommendationForm from './components/RecommendationForm';
import SetDetails from './components/SetDetails';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Badge from '@mui/material/Badge';
import IconButton from '@mui/material/IconButton';
import Modal from '@mui/material/Modal';
import Button from '@mui/material/Button';
import MenuIcon from '@mui/icons-material/Menu';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';

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
  const [open, setOpen] = useState(false);
  const [unread, setUnread] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const handleOpen = () => {
    setOpen(true);
    setUnread(false);
  };
  const handleClose = () => setOpen(false);
  const handleDrawerOpen = () => setDrawerOpen(true);
  const handleDrawerClose = () => setDrawerOpen(false);

  return (
    <Router>
      <Routes>
        <Route path="/" element={
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
                <Box sx={{ mb: 6, textAlign: 'center', position: 'relative' }}>
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
                  <Box sx={{ position: 'absolute', top: 0, right: 0, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <IconButton color="inherit" onClick={handleOpen} aria-label="使い方案内">
                      <Badge color="error" variant="dot" invisible={!unread}>
                        <NotificationsIcon fontSize="large" />
                      </Badge>
                    </IconButton>
                    <IconButton color="inherit" onClick={handleDrawerOpen} aria-label="メニュー">
                      <MenuIcon fontSize="large" />
                    </IconButton>
                  </Box>
                </Box>
                <RecommendationForm />
                <Modal open={open} onClose={handleClose} aria-labelledby="howto-modal-title" aria-describedby="howto-modal-desc">
                  <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    bgcolor: 'background.paper',
                    borderRadius: 3,
                    boxShadow: 24,
                    p: { xs: 3, sm: 4 },
                    minWidth: { xs: 280, sm: 400 },
                    maxWidth: '90vw',
                  }}>
                    <Typography id="howto-modal-title" variant="h5" sx={{ mb: 2, fontWeight: 700 }}>
                      SwingFit Pro 使い方ガイド
                    </Typography>
                    <Typography id="howto-modal-desc" sx={{ mb: 2 }}>
                      1. あなたの身長・体重・年齢・ゴルフ経験などを入力してください。<br />
                      2. 「最適なクラブセットを見つける」ボタンを押すと、AIがあなたに合った14本のクラブセットを提案します。<br />
                      3. おすすめセットはアコーディオン形式で詳細を確認できます。<br />
                      4. ブランドロゴやスペックを見ながら、最適なクラブ構成を比較してください。
                    </Typography>
                    <Box sx={{ textAlign: 'right' }}>
                      <Button variant="contained" color="primary" onClick={handleClose}>閉じる</Button>
                    </Box>
                  </Box>
                </Modal>
                <Drawer anchor="right" open={drawerOpen} onClose={handleDrawerClose}>
                  <Box sx={{ width: 220 }} role="presentation" onClick={handleDrawerClose}>
                    <List>
                      <ListItem button>
                        <ListItemText primary="ホーム" />
                      </ListItem>
                      <ListItem button>
                        <ListItemText primary="使い方ガイド" />
                      </ListItem>
                      <ListItem button>
                        <ListItemText primary="お問い合わせ" />
                      </ListItem>
                    </List>
                  </Box>
                </Drawer>
              </Container>
            </Box>
          </ThemeProvider>
        } />
        <Route path="/set-details/:id" element={<SetDetails />} />
      </Routes>
    </Router>
  );
}

export default App; 