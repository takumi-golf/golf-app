import React, { useState, useCallback } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  MenuItem,
  Typography,
  CircularProgress
} from '@mui/material';
import { createRecommendation } from '../api/client';
import InfoIcon from '@mui/icons-material/Info';
import SportsGolfIcon from '@mui/icons-material/SportsGolf';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';

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

// 設問内容を配列で管理
const chatQuestions = [
  {
    key: 'golfHistory',
    label: 'ゴルフ歴はどれくらいですか？',
    options: ['半年未満', '1～3年', '3年以上', '覚えていない']
  },
  {
    key: 'score',
    label: '平均スコア（またはベストスコア）は？',
    options: ['120以上', '110～119', '100～109', '90～99', '89以下', '分からない']
  },
  {
    key: 'trouble',
    label: '今、ゴルフで一番悩んでいることは何ですか？',
    options: ['方向性', '飛距離', '安定性', 'アプローチ', 'パター', '特にない']
  },
  {
    key: 'confidentClub',
    label: 'コースや練習で"自信がある"または"よく当たる"クラブはどれですか？',
    options: ['ドライバー', 'アイアン', 'ウェッジ', 'パター', '特にない']
  },
  {
    key: 'missClub',
    label: '最近、一番"ミスが多い"と感じるのはどのクラブですか？',
    options: ['ドライバー', 'アイアン', 'ウェッジ', 'パター', '特にない']
  },
  {
    key: 'goal',
    label: 'どんなゴルフを目指したいですか？',
    options: ['スコアアップ', '楽しくラウンド', '飛距離アップ', '仲間と上達', '特にない']
  },
  {
    key: 'budget',
    label: 'クラブ購入に考えている予算帯は？（スキップ可）',
    options: ['1万円未満', '1～3万円', '3～5万円', '5万円以上', 'まだ決めていない', 'スキップ']
  }
];

const RecommendationForm = ({ onRecommend = () => {} }) => {
  const [answers, setAnswers] = useState({});
  const [step, setStep] = useState(0);

  const handleSelect = (value) => {
    const key = chatQuestions[step].key;
    setAnswers(prev => ({ ...prev, [key]: value }));
    setStep(prev => prev + 1);
  };

  // チャット形式UI
  if (step < chatQuestions.length) {
    const q = chatQuestions[step];
    return (
      <Box sx={{ maxWidth: 480, mx: 'auto', mt: 4, p: 2 }}>
        <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>{q.label}</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {q.options.map(opt => (
            <Button
              key={opt}
              variant="outlined"
              onClick={() => handleSelect(opt)}
              sx={{ fontSize: '1rem', py: 1.5, borderRadius: 2, fontWeight: 600 }}
            >
              {opt}
            </Button>
          ))}
        </Box>
      </Box>
    );
  }

  // 全設問回答後の処理（例：onRecommendにanswersを渡すなど）
  return (
    <Box sx={{ maxWidth: 480, mx: 'auto', mt: 4, p: 2 }}>
      <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>ご回答ありがとうございました！</Typography>
      <pre style={{ background: '#f5f5f5', padding: 16, borderRadius: 8 }}>{JSON.stringify(answers, null, 2)}</pre>
      {/* 必要に応じてonRecommend(answers)など呼び出し */}
    </Box>
  );
};

export default RecommendationForm; 