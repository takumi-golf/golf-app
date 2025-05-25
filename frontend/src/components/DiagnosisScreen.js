import React, { useState, useRef, useEffect } from 'react';
import { Box, Typography, Button, Paper, Chip, IconButton } from '@mui/material';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { keyframes } from '@mui/system';
import { AnimatedIconButton } from './AnimatedIconButton';
import ClubRecommendations from './ClubRecommendations';

// アニメーション定義
const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

// チャットフロー設計
const chatFlow = [
  {
    question: "ゴルフ歴はどれくらいですか？",
    options: ["半年未満", "1～3年", "3年以上", "覚えていない"]
  },
  {
    question: "スコアを確認したい範囲を選んでください",
    options: [
      "120以上",
      "110～119",
      "100～109",
      "90～99",
      "80～89",
      "70～79",
      "69以下",
      "分からない"
    ]
  },
  {
    question: "今、ゴルフで一番悩んでいることは何ですか？",
    options: ["方向性", "飛距離", "安定性", "アプローチ", "パター", "特にない"]
  },
  {
    question: "コースや練習で\"自信がある\"または\"よく当たる\"クラブはどれですか？",
    options: ["ドライバー", "アイアン", "ウェッジ", "パター", "特にない"]
  },
  {
    question: "最近、一番\"ミスが多い\"と感じるのはどのクラブですか？",
    options: ["ドライバー", "アイアン", "ウェッジ", "パター", "特にない"]
  },
  {
    question: "どんなゴルフを目指したいですか？",
    options: ["スコアアップ", "楽しくラウンド", "飛距離アップ", "仲間と上達", "特にない"]
  },
  {
    question: "クラブ購入に考えている予算帯は？",
    options: ["1万円未満", "1～3万円", "3～5万円", "5～10万円", "10万円以上", "まだ決めていない"]
  }
];

function DiagnosisScreen({ onReset }) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [showLoadingAnimation, setShowLoadingAnimation] = useState(false);
  const messagesEndRef = useRef(null);
  const optionsBarRef = useRef(null);
  const recommendRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [answers]);

  // 選択肢を選んだ時の処理
  const handleOptionSelect = (option) => {
    const newAnswers = [...answers, option];
    setAnswers(newAnswers);
    if (step < chatFlow.length - 1) {
      setStep(step + 1);
      // 回答後に自動スクロール
      setTimeout(() => {
        if (messagesEndRef.current) {
          messagesEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
          const chatArea = messagesEndRef.current.parentElement;
          if (chatArea && optionsBarRef.current) {
            chatArea.scrollTop += optionsBarRef.current.offsetHeight + 68;
          }
        }
      }, 100);
    } else {
      // すべての質問が終わったらローディングアニメーションを表示
      setShowLoadingAnimation(true);
      // 3秒後にAPI呼び出し
      setTimeout(() => {
        setShowLoadingAnimation(false);
      }, 3000);
    }
  };

  // 一つ前に戻るボタン
  const handleBack = () => {
    if (answers.length > 0) {
      const newAnswers = answers.slice(0, -1);
      setAnswers(newAnswers);
      setStep(newAnswers.length);
    }
  };

  return (
    <>
      {/* チャット画面内ヘッダー */}
      <Box sx={{
        width: '100%',
        height: 56,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 3,
        borderBottom: '1px solid #e0e0e2',
        bgcolor: '#f7f7f8',
        position: 'relative',
        zIndex: 30,
        flexShrink: 0,
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography sx={{ fontWeight: 700, fontSize: 18, color: '#222' }}>
            AIゴルフクラブ診断
          </Typography>
          <Chip label="β版" size="small" sx={{ fontWeight: 700, fontSize: 12, letterSpacing: 1, bgcolor: '#69f0ae', color: '#222', height: 22, ml: 1 }} />
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.35 }}>
          <AnimatedIconButton
            onClick={handleBack}
            disabled={step === 0 || answers.length === 0}
            sx={{
              color: (step === 0 || answers.length === 0) ? '#bbb' : '#666',
              opacity: (step === 0 || answers.length === 0) ? 0.4 : 1,
              cursor: (step === 0 || answers.length === 0) ? 'default' : 'pointer',
              mr: 1,
            }}
          >
            <ChevronLeftIcon sx={{ fontSize: 22, fontWeight: 700 }} />
            <span className="btn-label">1つ戻る</span>
          </AnimatedIconButton>
          <AnimatedIconButton
            onClick={onReset}
            sx={{
              color: '#666',
              opacity: 1,
              cursor: 'pointer',
            }}
          >
            <RestartAltIcon sx={{ fontSize: 22, fontWeight: 700 }} />
            <span className="btn-label">最初からやり直す</span>
          </AnimatedIconButton>
        </Box>
      </Box>

      {/* チャット履歴エリア */}
      <Box sx={{
        flex: 1,
        width: '100%',
        overflowY: 'auto',
        p: 0,
        fontFamily: `'Inter', 'Noto Sans JP', 'system-ui', sans-serif`,
        background: '#f7f7f8',
        display: 'flex',
        flexDirection: 'column',
      }}>
        <Box sx={{ flex: 1, px: { xs: 0.75, md: 1.5 }, py: 2 }}>
          {chatFlow.slice(0, step + 1).map((q, idx) => (
            <Box key={idx} sx={{ mb: 2.5, px: { xs: 0.75, md: 1.5 }, display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
              {/* AIの発言 */}
              <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', mb: 1 }}>
                <Box sx={{
                  display: 'inline-block',
                  width: 'fit-content',
                  maxWidth: '70%',
                  py: 1.5,
                  px: 2.5,
                  color: '#222',
                  fontWeight: 500,
                  fontSize: 16,
                  lineHeight: 1.6,
                  letterSpacing: 0.2,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  fontFamily: `'Inter', 'Noto Sans JP', 'system-ui', sans-serif`,
                }}>
                  {q.question}
                </Box>
              </Box>
              {/* ユーザー側の回答 */}
              <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'flex-end', alignItems: 'flex-end', minHeight: 36, mt: 0.5 }}>
                {answers[idx] && (
                  <Paper sx={{
                    display: 'inline-block',
                    maxWidth: '70%',
                    width: 'fit-content',
                    py: 0.8,
                    px: 2,
                    borderRadius: '999px',
                    bgcolor: '#e7e7e9',
                    color: '#222',
                    border: '1.5px solid #e0e0e2',
                    boxShadow: '0 1px 4px rgba(0,0,0,0.04)',
                    fontWeight: 500,
                    fontSize: 16,
                    animation: `${fadeIn} 0.5s`,
                    lineHeight: 1.6,
                    letterSpacing: 0.2,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    fontFamily: `'Inter', 'Noto Sans JP', 'system-ui', sans-serif`,
                  }}>
                    {answers[idx]}
                  </Paper>
                )}
              </Box>
            </Box>
          ))}
          <div ref={messagesEndRef} style={{ float: 'left', clear: 'both' }} />
        </Box>
      </Box>

      {/* 選択肢エリア or 診断完了メッセージ */}
      {answers.length < chatFlow.length && step === answers.length ? (
        <Box
          ref={optionsBarRef}
          sx={{
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            height: 120,
            minHeight: 120,
            maxHeight: 120,
            px: 2,
            py: 0,
            zIndex: 10,
            background: '#f7f7f8',
            borderTop: '1.5px solid #e0e0e2',
            boxShadow: '0 -2px 16px rgba(0,0,0,0.04)',
            flexShrink: 0,
          }}
        >
          {/* 選択肢ボタン */}
          <Box sx={{
            flex: 8,
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gridTemplateRows: 'repeat(2, 1fr)',
            gap: 1.2,
            width: '100%',
            minHeight: 0,
            pb: 1.2,
            pt: 2.2,
            px: 2,
            background: 'transparent',
            boxSizing: 'border-box',
            justifyItems: 'center',
            alignItems: 'center',
          }}>
            {chatFlow[step].options.slice(0, 6).map((opt) => (
              <Button
                key={opt}
                onClick={() => handleOptionSelect(opt)}
                variant="outlined"
                sx={{
                  borderRadius: '16px',
                  px: 1.2,
                  py: 0.7,
                  fontWeight: 500,
                  fontSize: 13.5,
                  width: '100%',
                  background: '#fff',
                  color: '#222',
                  border: '1.5px solid #e0e0e2',
                  boxShadow: 'none',
                  transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                  letterSpacing: 0.5,
                  outline: 'none',
                  whiteSpace: 'normal',
                  textAlign: 'center',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  m: 0,
                  '&:hover': {
                    background: '#f3f3f4',
                    borderColor: '#bdbdbf',
                    color: '#222',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
                    transform: 'translateY(-1px) scale(1.03)',
                  },
                  '&:active': {
                    background: '#ededee',
                    borderColor: '#bdbdbf',
                    color: '#222',
                    boxShadow: 'none',
                    transform: 'translateY(1px) scale(0.98)'
                  },
                  '&:focus': {
                    outline: '2px solid #1976D2',
                    outlineOffset: 2
                  }
                }}
              >
                {opt}
              </Button>
            ))}
          </Box>
        </Box>
      ) : (
        <Box
          sx={{
            width: '100%',
            height: 120,
            minHeight: 120,
            maxHeight: 120,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#f7f7f8',
            borderTop: '1px solid #e0e0e2',
            textAlign: 'center',
            gap: 0.5,
            flexShrink: 0,
            overflow: 'hidden',
            p: 0,
          }}
        >
          <span style={{fontSize: 28, lineHeight: 1, marginBottom: 2}}>🎉✨</span>
          <Typography sx={{ fontWeight: 700, fontSize: 18, color: '#1976D2', mb: 0.5 }}>
            診断が完了しました！
          </Typography>
          <Typography
            onClick={onReset}
            sx={{
              mt: 0.5,
              color: '#888',
              fontWeight: 400,
              fontSize: 13,
              opacity: 0.7,
              textDecoration: 'underline',
              cursor: 'pointer',
              transition: 'color 0.2s, opacity 0.2s',
              '&:hover': {
                color: '#1976D2',
                opacity: 1,
                textDecoration: 'underline'
              }
            }}
          >
            最初からはじめる
          </Typography>
        </Box>
      )}

      {/* 診断完了時のみレコメンドエリア */}
      {answers.length === chatFlow.length && !showLoadingAnimation && (
        <div ref={recommendRef}>
          <ClubRecommendations />
        </div>
      )}
    </>
  );
}

export default DiagnosisScreen; 