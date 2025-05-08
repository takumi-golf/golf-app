import React, { useState, useMemo, useCallback } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  MenuItem,
  Typography,
  Paper,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Avatar,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { getRecommendations } from '../api/client';
import { api } from '../api/client';



const initialFormState = {
  height: '170',
  weight: '65',
  age: '40',
  gender: 'male',
  handicap: '20',
  headSpeed: '40',
  ballSpeed: '50',
  launchAngle: '15',
  swingIssue: 'none',
  budget: 150000,
};

const genderOptions = [
  { value: 'male', label: '男性' },
  { value: 'female', label: '女性' },
];

const swingIssueOptions = [
  { value: 'slice', label: 'スライス' },
  { value: 'hook', label: 'フック' },
  { value: 'thin', label: 'トップ' },
  { value: 'fat', label: 'ダフリ' },
  { value: 'none', label: '特になし' },
];

// ブランドごとの色とロゴファイル名
const brandStyles = {
  'タイトリスト': { 
    color: '#000000', 
    logo: 'titleist.svg',
    alt: 'Titleist Logo',
    isSvg: true,
    bgColor: '#000000',
    textColor: '#FFFFFF'
  },
  'テーラーメイド': { 
    color: '#000000', 
    logo: 'TaylorMade.png',
    alt: 'TaylorMade Logo',
    isSvg: false,
    bgColor: '#000000',
    textColor: '#FFFFFF'
  },
  'キャロウェイ': { 
    color: '#1a5e9a', 
    logo: 'callaway.svg',
    alt: 'Callaway Logo',
    isSvg: true,
    bgColor: '#1a5e9a',
    textColor: '#FFFFFF'
  },
  'ミズノ': { 
    color: '#005bac', 
    logo: 'mizuno.jpg',
    alt: 'Mizuno Logo',
    isSvg: false,
    bgColor: '#005bac',
    textColor: '#FFFFFF'
  },
  'ピン': { 
    color: '#000000', 
    logo: 'ping.webp',
    alt: 'PING Logo',
    isSvg: false,
    bgColor: '#000000',
    textColor: '#FFFFFF'
  },
  'コブラ': { 
    color: '#f9b233', 
    logo: 'cobra.png',
    alt: 'Cobra Logo',
    isSvg: false,
    bgColor: '#f9b233',
    textColor: '#000000'
  },
  'クリーブランド': { 
    color: '#003366', 
    logo: 'cleveland.png',
    alt: 'Cleveland Logo',
    isSvg: false,
    bgColor: '#003366',
    textColor: '#FFFFFF'
  },
  'ボブ・ボッシュ': { 
    color: '#bfa46d', 
    logo: 'Vokey.png',
    alt: 'Vokey Logo',
    isSvg: false,
    bgColor: '#bfa46d',
    textColor: '#000000'
  },
  'その他': { 
    color: '#888888', 
    logo: '',
    alt: 'Default Logo',
    isSvg: false,
    bgColor: '#888888',
    textColor: '#FFFFFF'
  },
};

const clubIcons = {
  'ドライバー': '🏌️‍♂️',
  '3W': '🌲', '4W': '🌲', '5W': '🌲', '7W': '🌲', '9W': '🌲',
  '2U': '🔷', '3U': '🔷', '4U': '🔷', '5U': '🔷', '6U': '🔷',
  '3H': '🔷', '4H': '🔷', '5H': '🔷',
  '2I': '🏑', '3I': '🏑', '4I': '🏑', '5I': '🏑', '6I': '🏑', '7I': '🏑', '8I': '🏑', '9I': '🏑',
  'PW': '🪓', 'AW': '🪓', 'GW': '🪓', 'SW': '🪓', 'LW': '🪓',
  'パター': '⛳',
};

const RecommendationForm = () => {
  const [formData, setFormData] = useState(initialFormState);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);

  // メモ化されたフォーマット関数
  const formatNumber = useCallback((value) => {
    if (value === null || value === undefined) return '';
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }, []);

  // メモ化された数値のフォーマット解除関数
  const unformatNumber = useCallback((value) => {
    return value.replace(/,/g, '');
  }, []);

  // メモ化されたハンドラー
  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    if (name === 'budget') {
      let num = parseInt(unformatNumber(value), 10);
      if (isNaN(num)) num = '';
      setFormData(prev => ({ ...prev, [name]: num }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  }, [unformatNumber]);

  const handleBudgetBlur = useCallback(() => {
    setFormData(prev => ({
      ...prev,
      budget: !prev.budget || prev.budget < 30000 ? 30000 : prev.budget > 500000 ? 500000 : prev.budget
    }));
  }, []);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      let budget = Number(formData.budget);
      if (!budget || budget < 30000) budget = 30000;
      if (budget > 500000) budget = 500000;
  
      // バックエンドのスキーマに合わせてデータを整形
      const sendData = {
        name: `${formData.gender === 'male' ? '男性' : '女性'}向けカスタムセット`,
        description: `${formData.age}歳、ハンディキャップ${formData.handicap}の${formData.gender === 'male' ? '男性' : '女性'}向けセット`,
        total_price: budget,
        match_score: 0.8, // 仮の値
        reason: `${formData.swingIssue === 'none' ? 'バランスの取れた' : 'スイングの課題に合わせた'}セット構成`,
        purchase_url: null,
        clubs: [
          {
            name: "ドライバー",
            type: "ドライバー",
            loft: 10.5,
            length: 45.75,
            flex: "R",
            weight: 300,
            brand: "タイトリスト",
            price: 50000,
            description: "高反発ドライバー"
          }
        ] // 仮のデータ
      };
  
      const response = await api.createRecommendation(sendData);
      setRecommendations([response.data]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [formData]);

  // メモ化されたレコメンデーション表示
  const renderRecommendations = useMemo(() => {
    if (!recommendations || !Array.isArray(recommendations)) return null;
    return (
      <Box sx={{ mt: 4, px: { xs: 1, sm: 2, md: 3 } }}>
        <Typography variant="h5" gutterBottom sx={{ 
          fontSize: { xs: '1.5rem', sm: '1.75rem', md: '2rem' },
          textAlign: { xs: 'center', sm: 'left' }
        }}>
          おすすめのクラブセット
        </Typography>
        {recommendations.map((rec, index) => {
          // 必要なプロパティの存在チェックとデフォルト値の設定
          const features = rec.features || 'バランス型カスタムセット';
          const brand = rec.brand || 'その他';
          const matchScore = rec.match_score || 0;
          const totalPrice = rec.total_price || 0;
          const clubs = rec.clubs || {};

          return (
            <Accordion
              key={`rec-${index}`}
              expanded={expanded === index}
              onChange={() => setExpanded(expanded === index ? false : index)}
              sx={{ 
                mb: 2, 
                borderRadius: 2, 
                boxShadow: '0 2px 8px rgba(0,0,0,0.07)',
                '&:before': { display: 'none' },
                '& .MuiAccordionSummary-root': {
                  transition: 'background 0.2s',
                  cursor: 'pointer',
                  bgcolor: expanded === index ? '#E8F5E9' : '#fff',
                  '&:hover': { bgcolor: '#F1F8E9' },
                  borderRadius: 2,
                  p: { xs: 1, sm: 2 },
                },
                '& .MuiAccordionSummary-expandIconWrapper': {
                  color: expanded === index ? '#1B5E20' : '#888',
                  fontSize: { xs: 28, sm: 36 },
                  transition: 'color 0.2s',
                },
              }}
            >
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box sx={{ 
                  width: '100%', 
                  display: 'flex', 
                  flexDirection: { xs: 'column', sm: 'row' },
                  justifyContent: 'space-between', 
                  alignItems: { xs: 'flex-start', sm: 'center' },
                  gap: { xs: 1, sm: 0 }
                }}>
                  <Box>
                    <Typography variant="h6" color="primary" sx={{ 
                      fontWeight: 700,
                      fontSize: { xs: '1.1rem', sm: '1.25rem' }
                    }}>
                      {brand}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ 
                      mb: 1,
                      fontSize: { xs: '0.875rem', sm: '1rem' }
                    }}>
                      コンセプト: {features.split('、')[0] || 'バランス型カスタムセット'}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary" sx={{ 
                      fontWeight: 600,
                      fontSize: { xs: '0.875rem', sm: '1rem' }
                    }}>
                      マッチングスコア: <span style={{ color: '#F57C00' }}>{Math.round(matchScore * 100)}%</span>
                    </Typography>
                    <Typography variant="h6" color="primary" sx={{ 
                      fontWeight: 700,
                      fontSize: { xs: '1.1rem', sm: '1.25rem' }
                    }}>
                      ¥{totalPrice.toLocaleString()}
                    </Typography>
                  </Box>
                  <Box sx={{ 
                    textAlign: { xs: 'left', sm: 'right' },
                    minWidth: { xs: 'auto', sm: 120 }
                  }}>
                    <Typography variant="caption" color="text.secondary" sx={{ 
                      fontSize: { xs: 12, sm: 14 }
                    }}>
                      {expanded === index ? 'クリックで閉じる' : 'クリックで詳細表示'}
                    </Typography>
                  </Box>
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ p: { xs: 1, sm: 2 } }}>
                <Grid container spacing={{ xs: 1, sm: 2 }}>
                  {Object.entries(clubs).map(([type, club]) => {
                    const clubBrand = club.brand || 'その他';
                    const style = brandStyles[clubBrand] || brandStyles['その他'];
                    return (
                      <Grid item xs={12} sm={6} md={4} key={`club-${type}`}>
                        <Paper sx={{ 
                          p: { xs: 1.5, sm: 2 }, 
                          display: 'flex', 
                          alignItems: 'center', 
                          borderRadius: 2, 
                          boxShadow: '0 2px 8px rgba(0,0,0,0.07)'
                        }}>
                          <Avatar sx={{ 
                            bgcolor: style.bgColor, 
                            mr: { xs: 1.5, sm: 2 }, 
                            width: { xs: 48, sm: 56 }, 
                            height: { xs: 48, sm: 56 },
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            overflow: 'hidden',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                            '&:hover': {
                              '& img': {
                                transform: 'scale(1.1)',
                              }
                            }
                          }}>
                            {style.logo ? (
                              <img 
                                src={`/brand-logos/${style.logo}`} 
                                alt={style.alt}
                                loading="lazy"
                                style={{ 
                                  width: style.isSvg ? '60%' : '80%', 
                                  height: style.isSvg ? '60%' : '80%',
                                  objectFit: 'contain',
                                  transition: 'all 0.3s ease',
                                  transform: 'scale(1)',
                                  filter: style.textColor === '#FFFFFF' ? 'brightness(0) invert(1)' : 'none',
                                }} 
                              />
                            ) : (
                              <span style={{ 
                                fontSize: { xs: 24, sm: 32 },
                                color: style.textColor
                              }}>
                                {clubIcons[type] || type[0]}
                              </span>
                            )}
                          </Avatar>
                          <Box>
                            <Typography variant="subtitle1" color="primary" sx={{ 
                              fontWeight: 600,
                              fontSize: { xs: '0.875rem', sm: '1rem' }
                            }}>
                              {type}
                            </Typography>
                            <Typography variant="body1" sx={{ 
                              fontWeight: 500,
                              fontSize: { xs: '0.875rem', sm: '1rem' }
                            }}>
                              <b>{clubBrand}</b> {club.model || ''}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{
                              fontSize: { xs: '0.75rem', sm: '0.875rem' }
                            }}>
                              ロフト: {club.loft || '-'} / シャフト: {club.shaft || '-'} / 硬さ: {club.flex || '-'}
                            </Typography>
                          </Box>
                        </Paper>
                      </Grid>
                    );
                  })}
                </Grid>
              </AccordionDetails>
            </Accordion>
          );
        })}
      </Box>
    );
  }, [recommendations, expanded]);

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Paper elevation={3} sx={{ 
        p: { xs: 2, sm: 3, md: 4 }, 
        mb: 4, 
        borderRadius: 2,
        mx: { xs: 1, sm: 2, md: 3 }
      }}>
        <Typography variant="h5" gutterBottom sx={{ 
          mb: 3, 
          color: 'primary.main',
          fontSize: { xs: '1.5rem', sm: '1.75rem', md: '2rem' },
          textAlign: { xs: 'center', sm: 'left' }
        }}>
          あなたのゴルフスタイルを教えてください
        </Typography>
        <Grid container spacing={{ xs: 2, sm: 3 }}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="身長 (cm)"
              name="height"
              type="number"
              value={formData.height}
              onChange={handleChange}
              required
              inputProps={{ min: 140, max: 200 }}
              helperText="140cm〜200cmの範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="体重 (kg)"
              name="weight"
              type="number"
              value={formData.weight}
              onChange={handleChange}
              required
              inputProps={{ min: 40, max: 120 }}
              helperText="40kg〜120kgの範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="年齢"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              required
              inputProps={{ min: 18, max: 80 }}
              helperText="18歳〜80歳の範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="性別"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
            >
              {genderOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="ハンディキャップ"
              name="handicap"
              type="number"
              value={formData.handicap}
              onChange={handleChange}
              required
              inputProps={{ min: 0, max: 54 }}
              helperText="0〜54の範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="ヘッドスピード (m/s)"
              name="headSpeed"
              type="number"
              value={formData.headSpeed}
              onChange={handleChange}
              required
              inputProps={{ min: 30, max: 60 }}
              helperText="30m/s〜60m/sの範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="ボールスピード (m/s)"
              name="ballSpeed"
              type="number"
              value={formData.ballSpeed}
              onChange={handleChange}
              required
              inputProps={{ min: 40, max: 80 }}
              helperText="40m/s〜80m/sの範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="打ち出し角 (度)"
              name="launchAngle"
              type="number"
              value={formData.launchAngle}
              onChange={handleChange}
              required
              inputProps={{ min: 5, max: 25 }}
              helperText="5度〜25度の範囲で入力してください"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="スイングの課題"
              name="swingIssue"
              value={formData.swingIssue}
              onChange={handleChange}
              required
            >
              {swingIssueOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="予算 (円)"
              name="budget"
              type="text"
              value={formatNumber(formData.budget)}
              onChange={handleChange}
              onBlur={handleBudgetBlur}
              required
              inputProps={{ min: 30000, max: 500000, step: 10000, inputMode: 'numeric', pattern: '[0-9,]*' }}
              helperText="3万円〜50万円の範囲で入力してください"
            />
          </Grid>
        </Grid>
        <Box sx={{ 
          mt: 4, 
          display: 'flex', 
          justifyContent: 'center',
          px: { xs: 1, sm: 2 }
        }}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
            disabled={loading}
            sx={{ 
              px: { xs: 3, sm: 4 }, 
              py: { xs: 1, sm: 1.5 },
              width: { xs: '100%', sm: 'auto' }
            }}
          >
            {loading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              '最適なクラブセットを見つける'
            )}
          </Button>
        </Box>
      </Paper>

      {error && (
        <Typography color="error" align="center" gutterBottom sx={{ px: 2 }}>
          {error}
        </Typography>
      )}

      {renderRecommendations}
    </Box>
  );
};

export default React.memo(RecommendationForm); 