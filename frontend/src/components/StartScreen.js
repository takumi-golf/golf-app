import React from 'react';
import { Box, Typography, Chip, Button } from '@mui/material';

export default function StartScreen({ onStart }) {
  return (
    <Box
      sx={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        px: 3,
        py: 4,
        textAlign: 'center',
      }}
    >
      <Typography sx={{ fontWeight: 700, fontSize: 26, color: '#1976D2', mb: 1, letterSpacing: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
        AIゴルフクラブ診断
        <Chip label="β版" size="small" sx={{ fontWeight: 700, fontSize: 12, letterSpacing: 1, bgcolor: '#69f0ae', color: '#222', height: 22, ml: 1 }} />
      </Typography>
      <Typography sx={{ fontSize: 16, color: '#444', mb: 2, fontWeight: 400, letterSpacing: 0.2 }}>
        あなたに最適なゴルフクラブセットをAIが提案します。<br />
        いくつかの質問に答えるだけでOK！
      </Typography>
      <Button
        variant="contained"
        color="primary"
        size="large"
        sx={{
          borderRadius: '999px',
          fontWeight: 700,
          fontSize: 18,
          px: 5,
          py: 1.5,
          boxShadow: '0 2px 8px rgba(25,118,210,0.10)',
          textTransform: 'none',
          letterSpacing: 1,
          mt: 3
        }}
        onClick={onStart}
      >
        診断をはじめる
      </Button>
      <Typography sx={{ 
        fontSize: 13, 
        color: '#666', 
        textAlign: 'center',
        maxWidth: '80%',
        lineHeight: 1.6,
        mt: 1
      }}>
        ボタンを押すことで
        <a href="/terms" style={{ color: '#1976D2', textDecoration: 'underline' }}>利用規約</a>
        および
        <a href="/privacy" style={{ color: '#1976D2', textDecoration: 'underline' }}>プライバシーポリシー</a>
        に同意したものとみなします。
      </Typography>
    </Box>
  );
} 