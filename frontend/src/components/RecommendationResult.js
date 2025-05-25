import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Rating,
  TextField,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

const RecommendationResult = ({ recommendation, onRecommend = () => {}, sx }) => {
  const [feedback, setFeedback] = useState({ rating: 0, comment: '' });

  // デバッグ用: recommendationの中身を出力
  console.log('RecommendationResult props:', recommendation);

  if (!recommendation) {
    return (
      <Box sx={{
        ...sx,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        minHeight: 0,
        minWidth: 0
      }}>
        <Typography variant="h6" sx={{ color: 'primary.main', opacity: 0.7, textAlign: 'center' }}>
          ここにレコメンド結果が表示されます
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ ...sx }}>
      <Paper elevation={3} sx={{ p: { xs: 2, md: 4 }, mb: { xs: 4, md: 4 }, borderRadius: 2 }}>
        <Box sx={{ 
          mb: { xs: 4, md: 4 }, 
          display: 'flex', 
          flexDirection: { xs: 'column', md: 'row' }, 
          justifyContent: 'space-between', 
          alignItems: { xs: 'stretch', md: 'center' }, 
          gap: 2 
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button
              variant="outlined"
              startIcon={<ArrowBackIcon />}
              onClick={() => onRecommend(null)}
              sx={{
                color: 'primary.main',
                borderColor: 'primary.main',
                '&:hover': {
                  borderColor: 'primary.dark',
                  backgroundColor: 'rgba(27, 94, 32, 0.04)'
                }
              }}
            >
              戻る
            </Button>
            <Typography variant="h4" component="h1" gutterBottom sx={{ 
              color: 'primary.main', 
              fontSize: { xs: '1.5rem', md: '2rem' }, 
              textAlign: { xs: 'center', md: 'left' }, 
              mb: { xs: 0, md: 1 },
              fontWeight: 700
            }}>
              レコメンデーション結果
            </Typography>
          </Box>
        </Box>
        <pre style={{ 
          color: '#333', 
          background: '#f5f5f5', 
          padding: 16, 
          borderRadius: 4, 
          fontSize: 14,
          overflow: 'auto',
          '&::-webkit-scrollbar': { width: '6px' },
          '&::-webkit-scrollbar-thumb': { backgroundColor: 'grey.400' }
        }}>
          {JSON.stringify(recommendation, null, 2)}
        </pre>
      </Paper>
    </Box>
  );
};

export default RecommendationResult; 