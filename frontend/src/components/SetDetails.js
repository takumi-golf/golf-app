import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Avatar,
} from '@mui/material';

// ブランドごとの色とロゴファイル名
const brandStyles = {
  'タイトリスト': { color: '#222', logo: 'titleist.svg' },
  'テーラーメイド': { color: '#222222', logo: 'taylormade.svg' },
  'キャロウェイ': { color: '#1a5e9a', logo: 'callaway.svg' },
  'ミズノ': { color: '#005bac', logo: 'mizuno.svg' },
  'ピン': { color: '#111', logo: 'ping.svg' },
  'コブラ': { color: '#f9b233', logo: 'cobra.svg' },
  'クリーブランド': { color: '#003366', logo: 'cleveland.svg' },
  'ボブ・ボッシュ': { color: '#bfa46d', logo: 'vokey.svg' },
  'その他': { color: '#888', logo: '' },
};

// クラブ種別ごとのアイコン（簡易版）
const clubIcons = {
  'ドライバー': '🏌️‍♂️',
  '3W': '🌲',
  '4W': '🌲',
  '5W': '🌲',
  '7W': '🌲',
  '9W': '🌲',
  '2U': '🔷',
  '3U': '🔷',
  '4U': '🔷',
  '5U': '🔷',
  '6U': '🔷',
  '3H': '🔷',
  '4H': '🔷',
  '5H': '🔷',
  '2I': '🏑',
  '3I': '🏑',
  '4I': '🏑',
  '5I': '🏑',
  '6I': '🏑',
  '7I': '🏑',
  '8I': '🏑',
  '9I': '🏑',
  'PW': '🪓',
  'AW': '🪓',
  'GW': '🪓',
  'SW': '🪓',
  'LW': '🪓',
  'パター': '⛳',
};

const SetDetails = () => {
  const location = useLocation();
  const navigate = useNavigate();
  // セット情報はlocation.stateから受け取る想定
  const { recommendation } = location.state || {};

  if (!recommendation) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography>セット情報が見つかりません。</Typography>
        <Button variant="contained" onClick={() => navigate(-1)}>戻る</Button>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Paper elevation={4} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h4" color="primary" gutterBottom sx={{ fontWeight: 700 }}>
          {recommendation.brand}
        </Typography>
        <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
          合計金額: <span style={{ color: '#1B5E20' }}>¥{recommendation.total_price.toLocaleString()}</span>
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 3, fontSize: 18 }}>
          マッチングスコア: <span style={{ color: '#F57C00', fontWeight: 700 }}>{Math.round(recommendation.match_score * 100)}%</span>
        </Typography>
        <Grid container spacing={3}>
          {Object.entries(recommendation.clubs).map(([type, club]) => {
            const brand = club.brand || 'その他';
            const style = brandStyles[brand] || brandStyles['その他'];
            return (
              <Grid item xs={12} sm={6} md={4} key={type}>
                <Paper sx={{ p: 2, display: 'flex', alignItems: 'center', borderRadius: 2, boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
                  <Avatar sx={{ bgcolor: style.color, mr: 2, width: 56, height: 56 }}>
                    {style.logo ? (
                      <img src={`/brand-logos/${style.logo}`} alt={brand} style={{ width: 40, height: 40 }} />
                    ) : (
                      <span style={{ fontSize: 32 }}>{clubIcons[type] || type[0]}</span>
                    )}
                  </Avatar>
                  <Box>
                    <Typography variant="subtitle1" color="primary" sx={{ fontWeight: 600 }}>
                      {type}
                    </Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      <b>{club.brand}</b> {club.model}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      ロフト: {club.loft} / シャフト: {club.shaft} / 硬さ: {club.flex}
                    </Typography>
                  </Box>
                </Paper>
              </Grid>
            );
          })}
        </Grid>
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button variant="contained" color="primary" onClick={() => navigate(-1)} sx={{ px: 6, py: 1.5, fontSize: 18 }}>
            戻る
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default SetDetails; 