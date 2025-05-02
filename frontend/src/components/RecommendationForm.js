import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  MenuItem,
  Typography,
  Paper,
  CircularProgress,
  Card,
} from '@mui/material';
import { getRecommendations } from '../api/client';

const formatNumber = (value) => {
  if (value === null || value === undefined) return '';
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

const unformatNumber = (value) => {
  return value.replace(/,/g, '');
};

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

const RecommendationForm = () => {
  const [formData, setFormData] = useState(initialFormState);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'budget') {
      let num = parseInt(unformatNumber(value), 10);
      if (isNaN(num)) num = '';
      setFormData(prev => ({ ...prev, [name]: num }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleBudgetBlur = () => {
    setFormData(prev => ({
      ...prev,
      budget: !prev.budget || prev.budget < 30000 ? 30000 : prev.budget > 500000 ? 500000 : prev.budget
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      let budget = Number(formData.budget);
      if (!budget || budget < 30000) budget = 30000;
      if (budget > 500000) budget = 500000;
      const sendData = { ...formData, budget };
      const data = await getRecommendations(sendData);
      setRecommendations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderRecommendations = () => {
    if (!recommendations) return null;

    return (
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          おすすめのクラブセット
        </Typography>
        {recommendations.recommendations.map((rec, index) => (
          <Card key={index} sx={{ mb: 3, p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Box>
                <Typography variant="h6" color="primary">
                  {rec.brand}
                </Typography>
                <Typography variant="subtitle1" color="text.secondary">
                  マッチングスコア: {Math.round(rec.match_score * 100)}%
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'right' }}>
                <Typography variant="h6" color="primary">
                  ¥{rec.total_price.toLocaleString()}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    size="small"
                    onClick={() => window.open(`/set-details/${rec.id}`, '_blank')}
                    sx={{ mr: 1 }}
                  >
                    セット詳細
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    size="small"
                    onClick={() => window.open(`https://www.google.com/search?q=${encodeURIComponent(rec.brand + ' ' + Object.values(rec.clubs).map(c => c.model).join(' '))}`, '_blank')}
                  >
                    セット購入
                  </Button>
                </Box>
              </Box>
            </Box>

            <Grid container spacing={2}>
              {Object.entries(rec.clubs).map(([type, club]) => (
                <Grid item xs={12} sm={6} md={4} key={type}>
                  <Paper sx={{ p: 2, height: '100%' }}>
                    <Typography variant="subtitle1" color="primary" gutterBottom>
                      {type}
                    </Typography>
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        メーカー: {club.brand}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        モデル: {club.model}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        ロフト: {club.loft}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        シャフト: {club.shaft}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        硬さ: {club.flex}
                      </Typography>
                    </Box>
                    <Button
                      variant="text"
                      color="primary"
                      size="small"
                      onClick={() => window.open(`https://www.google.com/search?q=${encodeURIComponent(club.brand + ' ' + club.model)}`, '_blank')}
                      sx={{ mt: 1 }}
                    >
                      個別購入
                    </Button>
                  </Paper>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                セットの特徴
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {rec.features}
              </Typography>
            </Box>

            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                マッチング詳細
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    スイングスピード: {Math.round(rec.match_details.swing_speed_match * 100)}%
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    スキルレベル: {Math.round(rec.match_details.skill_level_match * 100)}%
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    好み: {Math.round(rec.match_details.preference_match * 100)}%
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Typography variant="body2" color="text.secondary">
                    予算: {Math.round(rec.match_details.budget_match * 100)}%
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          </Card>
        ))}
      </Box>
    );
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Paper elevation={3} sx={{ p: 4, mb: 4, borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom sx={{ mb: 3, color: 'primary.main' }}>
          あなたのゴルフスタイルを教えてください
        </Typography>
        <Grid container spacing={3}>
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
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
            disabled={loading}
            sx={{ px: 4, py: 1.5 }}
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
        <Typography color="error" align="center" gutterBottom>
          {error}
        </Typography>
      )}

      {renderRecommendations()}
    </Box>
  );
}

export default RecommendationForm; 