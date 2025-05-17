import React, { useState, useRef } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import useMediaQuery from '@mui/material/useMediaQuery';
import GolfCourseIcon from '@mui/icons-material/GolfCourse';
import Avatar from '@mui/material/Avatar';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';
import LoginIcon from '@mui/icons-material/Login';
import Divider from '@mui/material/Divider';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import Tooltip from '@mui/material/Tooltip';
import Fade from '@mui/material/Fade';
import { getClubSetRecommendations } from './api/client';
import { keyframes } from '@mui/system';
import CircularProgress from '@mui/material/CircularProgress';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/Send';
import Typography from '@mui/material/Typography';

// 繧｢繝九Γ繝ｼ繧ｷ繝ｧ繝ｳ縺ｮ螳夂ｾｩ
const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const fadeOut = keyframes`
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
`;

// 繝峨ャ繝医い繝九Γ繝ｼ繧ｷ繝ｧ繝ｳ縺ｮ螳夂ｾｩ
const dotFlashing = keyframes`
  0% { opacity: 0.2; }
  20% { opacity: 1; }
  100% { opacity: 0.2; }
`;

const theme = createTheme({
  palette: {
    primary: { main: '#2E7D32' },
    secondary: { main: '#FF9100' },
    background: { default: '#F8FBF8', paper: '#FFFFFF' },
    text: { primary: '#2D2D2D', secondary: '#5A5A5A' }
  },
  typography: {
    fontFamily: "'Noto Sans JP', sans-serif",
    body1: { fontSize: '0.95rem' }
  },
  breakpoints: {
    values: { xs: 0, sm: 600, md: 960 }
  }
});

const initialRecommendation = {
  driver: '初心者向けドライバー',
  iron: 'ゲーム改善用アイアン',
  putter: 'ストローク安定型パター'
};

function App() {
  const initialMessages = [
    {
      message: "ようこそ！あなたに最適なゴルフクラブを提案します。\nまずは以下の質問にお答えください。\n1. ゴルフ歴を教えてください",
      sender: "bot",
      direction: "incoming",
      timestamp: new Date().toISOString()
    }
  ];
  const [messages, setMessages] = useState(initialMessages);
  const [isTyping, setIsTyping] = useState(false);
  const [recommendation, setRecommendation] = useState(initialRecommendation);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  const [selectedNav, setSelectedNav] = useState('ai');
  const [clubSets, setClubSets] = React.useState([]);
  const [clubSetsLoading, setClubSetsLoading] = React.useState(false);
  const [clubSetsError, setClubSetsError] = React.useState(null);
  const [showOverlay, setShowOverlay] = React.useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // isTyping縺掲alse縺ｫ縺ｪ縺｣縺溘ち繧､繝溘Φ繧ｰ縺ｧ蜈･蜉帶ｬ�↓繝輔か繝ｼ繧ｫ繧ｹ
  React.useEffect(() => {
    if (!isTyping && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isTyping]);

  const handleSend = () => {
    let sendText = inputMessage.trim();
    if (!sendText) return;
    
    const newMessage = {
      message: sendText,
      direction: 'outgoing',
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsTyping(true);
    setClubSetsLoading(true);
    setClubSetsError(null);
    const fetchClubSets = async () => {
      try {
        const userData = {
          golf_history: '3年',
          score: 100,
          main_club: '7番アイアン',
          improvement_point: 'スコア改善'
        };
        const sets = await getClubSetRecommendations(userData);
        sets.sort((a, b) => b.match - a.match);
        setClubSets(sets);
      } catch (err) {
        setClubSetsError('クラブセットの検索に失敗しました');
      } finally {
        setTimeout(() => {
          const botResponse = {
            message: getNextQuestion(sendText),
            sender: "bot",
            direction: "incoming",
            timestamp: new Date().toISOString()
          };
          setMessages(prev => [...prev, botResponse]);
          updateRecommendation(sendText);
          setIsTyping(false);
          setClubSetsLoading(false);
          inputRef.current?.focus();
        }, 800);
      }
    };
    fetchClubSets();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const generateBotResponse = (userMessage) => ({
    message: getNextQuestion(userMessage),
    sender: "bot",
    direction: "incoming"
  });

  const getNextQuestion = (answer) => {
    const questionFlow = [
      "2. 平均スコアを教えてください",
      "3. メインクラブは？",
      "4. 改善したいポイントは？",
      "最適なクラブを提案します"
    ];
    return questionFlow[messages.filter(m => m.sender === 'user').length % questionFlow.length];
  };

  const updateRecommendation = (answer) => {
    let newRec = {};

    // ゴルフ歴の判定
    const yearMatch = answer.match(/([0-9０-９]+)\s*年目?/);
    const halfMatch = answer.match(/半年目?/);
    if (yearMatch) {
      const years = parseInt(yearMatch[1].replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 65248)));
      if (years <= 1) newRec.driver = '初心者向けドライバー';
      else if (years <= 3) newRec.driver = '中級者向けドライバー';
      else newRec.driver = '上級者向けドライバー';
    } else if (halfMatch) {
      newRec.driver = '初心者向けドライバー';
    }

    // メインクラブ
    if (/アイアン|7番|8番|9番/.test(answer)) {
      newRec.iron = '中級者向けアイアン';
    }
    if (/ウッド|5番ウッド|6番ウッド|ハイブリッド/.test(answer)) {
      newRec.driver = 'フォルギブネス向けドライバー';
    }
    if (/パター/.test(answer)) {
      newRec.putter = 'ストローク安定型パター';
    }

    setRecommendation(prev => ({
      ...prev,
      ...newRec
    }));
  };

  const handleResetChat = () => {
    setMessages(initialMessages);
    setRecommendation(initialRecommendation);
    setInputMessage('');
    if (inputRef.current) inputRef.current.focus();
  };

  // 蛻晏屓繝槭え繝ｳ繝域凾縺ｫAPI繝ｪ繧ｯ繧ｨ繧ｹ繝茨ｼ井ｻｮ縺ｧ蟷ｳ蝮�噪縺ｪ繝ｦ繝ｼ繧ｶ繝ｼ諠��ｱ繧帝∽ｿ｡��
  React.useEffect(() => {
    const fetchClubSets = async () => {
      setClubSetsLoading(true);
      setClubSetsError(null);
      try {
        const userData = {
          golf_history: '3蟷ｴ',
          score: 100,
          main_club: '7逡ｪ繧｢繧､繧｢繝ｳ',
          improvement_point: '鬟幄ｷ晞屬繧｢繝'
        };
        const sets = await getClubSetRecommendations(userData);
        // 繝槭ャ繝∝ｺｦ鬆↓繧ｽ繝ｼ繝
        sets.sort((a, b) => b.match - a.match);
        setClubSets(sets);
      } catch (err) {
        setClubSetsError('繧ｯ繝ｩ繝悶そ繝ヨ縺ｮ蜿門ｾ励↓螟ｱ謨励＠縺ｾ縺励◆');
      } finally {
        setClubSetsLoading(false);
      }
    };
    fetchClubSets();
  }, []);

  // clubSetsLoading縺ｮ螟牙喧繧堤屮隕悶＠縲√Μ繝ｼ繝峨ち繧､繝�繧定ｿｽ蜉�
  React.useEffect(() => {
    if (clubSetsLoading) {
      setShowOverlay(true);
    } else {
      // 繝ｭ繝ｼ繝�ぅ繝ｳ繧ｰ邨ゆｺ�ｾ後�0.8遘貞ｾ�▲縺ｦ縺九ｉ繧ｪ繝ｼ繝舌�繝ｬ繧､繧呈ｶ医☆
      const timer = setTimeout(() => setShowOverlay(false), 800);
      return () => clearTimeout(timer);
    }
  }, [clubSetsLoading]);

return (
<ThemeProvider theme={theme}>
<CssBaseline />
      {/* 繝倥ャ繝繝ｼ */}
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: 56,
          zIndex: 1200,
          display: 'flex',
          alignItems: 'center',
          boxShadow: 3,
          background: 'linear-gradient(135deg, #9B1ECD 0%, #9910FA 100%)',
          color: '#fff',
          backdropFilter: 'blur(10px)',
        }}
      >
        {/* 蟾ｦ繧ｫ繝ｩ繝�縺ｨ驥阪↑繧矩Κ蛻�□縺題牡莉倥″�九い繧､繧ｳ繝ｳ */}
        <Box sx={{
          width: { xs: 0, md: 86 },
          height: '100%',
          bgcolor: { md: 'primary.main', xs: 'transparent' },
          flexShrink: 0,
          display: { xs: 'none', md: 'flex' },
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <img src="/service-logos/logo-vertical.png" alt="AI Golf" style={{ height: 46, maxWidth: 46, objectFit: 'contain', background: 'transparent', display: 'block' }} />
        </Box>
        {/* 繝倥ャ繝繝ｼ譛ｬ菴� */}
        <Box sx={{
          flex: 1,
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          pl: { xs: 3, md: 2 },
          color: '#fff',
          fontWeight: 700,
          fontSize: '1.2rem',
          letterSpacing: '0.05em',
        }}>
          AIゴルフクラブレコメンダー
        </Box>
      </Box>
      {/* 3繧ｫ繝ｩ繝�繝ｬ繧､繧｢繧ｦ繝� */}
<Box
sx={{
display: 'flex',
flexDirection: { xs: 'column', md: 'row' },
          width: '100vw',
          height: '100vh',
          background: '#DCCCBE',
          alignItems: 'stretch',
          pt: '56px',
overflow: 'hidden',
          position: 'fixed',
          top: 0,
          left: 0,
}}
>
        {/* 蟾ｦ繧ｫ繝ｩ繝� */}
<Box
sx={{
            width: { xs: '100%', md: 86 },
            minWidth: { md: 86 },
            bgcolor: { xs: 'transparent', md: 'primary.main' },
            color: { xs: 'primary.contrastText', md: '#fff' },
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'stretch',
            justifyContent: 'flex-start',
            pt: 2,
            borderRight: { md: '1px solid', xs: 'none' },
            borderColor: { md: 'divider', xs: 'transparent' },
flexShrink: 0,
            height: '100%',
            overflow: 'auto',
          }}
        >
          {/* 繝翫ン繧ｲ繝ｼ繧ｷ繝ｧ繝ｳ�医い繧､繧ｳ繝ｳ荳九↓繝�く繧ｹ繝茨ｼ� */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'center', mt: 1 }}>
            <Box
              sx={{
                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5, width: '100%', py: 1,
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                ...(selectedNav === 'ai'
                  ? {
                      bgcolor: '#fff',
                      color: 'primary.main',
                      fontWeight: 700,
                      boxShadow: 2,
                      '& svg': { color: 'primary.main' }
                    }
                  : {
                      bgcolor: { md: 'primary.main' },
                      color: '#fff',
                      '&:hover': {
                        bgcolor: { md: 'rgba(255,255,255,0.28)' },
                        color: 'primary.main',
                        boxShadow: 2,
                        transform: 'scale(1.08)',
                        '& svg': { color: 'primary.main' }
                      }
                    }),
              }}
              tabIndex={0}
              role="button"
              onClick={() => setSelectedNav('ai')}
            >
              <SmartToyIcon sx={{ fontSize: 23, mb: 0.5, transition: 'color 0.18s' }} />
              <span style={{ fontWeight: 700, fontSize: 12, letterSpacing: 1 }}>AI</span>
            </Box>
            <Box sx={{ width: '80%', my: 2, mx: 'auto' }}>
              <Box sx={{
                width: '70%',
                height: '1.5px',
                bgcolor: '#fff',
                mb: 1,
                mx: 'auto',
              }} />
              <Box sx={{ textAlign: 'center', color: '#fff', fontSize: 13, fontWeight: 500, lineHeight: 1.3, letterSpacing: 1 }}>
                
              </Box>
            </Box>
<Box
sx={{
                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5, width: '100%', py: 1,
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                ...(selectedNav === 'history'
                  ? {
                      bgcolor: '#fff',
                      color: 'primary.main',
                      fontWeight: 700,
                      boxShadow: 2,
                      '& svg': { color: 'primary.main' }
                    }
                  : {
                      bgcolor: { md: 'primary.main' },
                      color: '#fff',
                      '&:hover': {
                        bgcolor: { md: 'rgba(255,255,255,0.28)' },
                        color: 'primary.main',
                        boxShadow: 2,
                        transform: 'scale(1.08)',
                        '& svg': { color: 'primary.main' }
                      }
                    }),
              }}
              tabIndex={0}
              role="button"
              onClick={() => setSelectedNav('history')}
            >
              <HistoryIcon sx={{ fontSize: 19, mb: 0.5, transition: 'color 0.18s' }} />
              <span style={{ fontWeight: 500, fontSize: 11 }}>履歴</span>
            </Box>
            <Box
              sx={{
                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5, width: '100%', py: 1,
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                ...(selectedNav === 'settings'
                  ? {
                      bgcolor: '#fff',
                      color: 'primary.main',
                      fontWeight: 700,
                      boxShadow: 2,
                      '& svg': { color: 'primary.main' }
                    }
                  : {
                      bgcolor: { md: 'primary.main' },
                      color: '#fff',
                      '&:hover': {
                        bgcolor: { md: 'rgba(255,255,255,0.28)' },
                        color: 'primary.main',
                        boxShadow: 2,
                        transform: 'scale(1.08)',
                        '& svg': { color: 'primary.main' }
                      }
                    }),
              }}
              tabIndex={0}
              role="button"
              onClick={() => setSelectedNav('settings')}
            >
              <SettingsIcon sx={{ fontSize: 19, mb: 0.5, transition: 'color 0.18s' }} />
              <span style={{ fontWeight: 500, fontSize: 11 }}>設定</span>
</Box>
<Box
sx={{
                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5, width: '100%', py: 1,
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                ...(selectedNav === 'login'
                  ? {
                      bgcolor: '#fff',
                      color: 'primary.main',
                      fontWeight: 700,
                      boxShadow: 2,
                      '& svg': { color: 'primary.main' }
                    }
                  : {
                      bgcolor: { md: 'primary.main' },
                      color: '#fff',
                      '&:hover': {
                        bgcolor: { md: 'rgba(255,255,255,0.28)' },
                        color: 'primary.main',
                        boxShadow: 2,
                        transform: 'scale(1.08)',
                        '& svg': { color: 'primary.main' }
                      }
                    }),
              }}
              tabIndex={0}
              role="button"
              onClick={() => setSelectedNav('login')}
            >
              <LoginIcon sx={{ fontSize: 19, mb: 0.5, transition: 'color 0.18s' }} />
              <span style={{ fontWeight: 500, fontSize: 11 }}>ログイン</span>
            </Box>
</Box>
</Box>
        {/* 荳ｭ螟ｮ繧ｫ繝ｩ繝��医メ繝｣繝�ヨ�� */}
<Box
sx={{
            width: { xs: '100%', md: 540 },
            minWidth: { md: 540 },
            bgcolor: 'background.paper',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'stretch',
            justifyContent: 'flex-start',
            borderRight: { md: '1px solid', xs: 'none' },
            borderColor: { md: 'divider', xs: 'transparent' },
flexShrink: 0,
            p: { xs: 2, md: 4 },
            boxSizing: 'border-box',
            pl: { md: 4 },
            height: '100%',
            overflow: 'auto',
}}
>
          <Paper 
            elevation={0}
            sx={{
              width: '100%',
              maxWidth: '100%',
              minHeight: 480,
              height: '100%',
              p: { xs: 2, md: 3 },
              border: '1.2px solid #3D371C',
              borderRadius: 4,
              display: 'flex',
              flexDirection: 'column',
              flex: 1,
              alignItems: 'stretch',
              justifyContent: 'flex-start',
              overflow: 'hidden',
              boxShadow: '0 4px 20px rgba(46, 125, 50, 0.08)',
              background: '#FFFFFF',
              backdropFilter: 'blur(10px)',
            }}
          >
            {/* チャットヘッダー */}
            <Box sx={{
              mb: 1,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              color: '#1A3A4A',
              fontWeight: 700,
              borderBottom: '2px solid #9910FA',
              pb: 0.5,
              pt: 1.2,
              px: 1.5,
              position: 'sticky',
              top: 0,
              zIndex: 2,
              background: '#fff',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
            }}>
              <SmartToyIcon sx={{ fontSize: 24, color: '#9910FA', p: 0.5 }} />
              <span style={{ fontWeight: 700, fontSize: 16, letterSpacing: 1, color: '#9910FA' }}>AI</span>
              <span style={{ marginLeft: 8 }}>チャット</span>
            </Box>

            {/* メッセージエリア */}
            <Box sx={{
              flex: 1,
              overflowY: 'auto',
              p: 2,
              '&::-webkit-scrollbar': {
                width: '8px',
                background: 'rgba(0,0,0,0.05)'
              },
              '&::-webkit-scrollbar-thumb': {
                backgroundColor: '#9910FA',
                borderRadius: '4px'
              }
            }}>
              {messages.map((msg, i) => (
                <Box
                  key={i}
                  sx={{
                    display: 'flex',
                    justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2,
                    gap: 1.5,
                    alignItems: 'flex-end'
                  }}
                >
                  {msg.sender === 'bot' && (
                    <Avatar sx={{ 
                      bgcolor: 'primary.main', 
                      width: 32, 
                      height: 32,
                      fontSize: 14
                    }}>
                      AI
                    </Avatar>
                  )}
                  
                  <Paper
                    sx={{
                      maxWidth: '75%',
                      p: 2,
                      borderRadius: '18px',
                      bgcolor: msg.sender === 'user' ? '#FFFFF4' : '#9910FA',
                      color: msg.sender === 'user' ? '#2D2D2D' : '#fff',
                      boxShadow: msg.sender === 'user'
                        ? '0 2px 8px rgba(61,195,150,0.15)'
                        : '0 4px 20px rgba(153,16,250,0.15)',
                      position: 'relative',
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      '&:hover': {
                        boxShadow: msg.sender === 'user'
                          ? '0 4px 12px rgba(61,195,150,0.25)'
                          : '0 6px 24px rgba(153,16,250,0.25)',
                      }
                    }}
                  >
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {msg.message}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{
                        display: 'block',
                        textAlign: 'right',
                        mt: 1,
                        color: msg.sender === 'user' ? 'rgba(0,0,0,0.5)' : 'rgba(255,255,255,0.7)'
                      }}
                    >
                      {new Date(msg.timestamp).toLocaleTimeString('ja-JP', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </Typography>
                  </Paper>
                </Box>
              ))}
              
              {isTyping && (
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 0.5,
                  mb: 2,
                  pl: 1
                }}>
                  <CircularProgress size={18} sx={{ mr: 1 }} />
                  <Typography variant="body2" color="textSecondary">
                    入力中...
                  </Typography>
                </Box>
              )}
              <div ref={messagesEndRef} />
            </Box>

            {/* 入力エリア */}
            <Box sx={{
              position: 'sticky',
              bottom: 0,
              bgcolor: 'background.paper',
              p: 2,
              borderTop: '1px solid rgba(0,0,0,0.12)',
              boxShadow: '0 -4px 12px rgba(0,0,0,0.05)'
            }}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="メッセージを入力..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                  multiline
                  maxRows={4}
                  disabled={isTyping}
                  inputRef={inputRef}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: '24px',
                      backgroundColor: 'background.default'
                    }
                  }}
                />
                <Tooltip title="送信">
                  <IconButton
                    color="primary"
                    onClick={handleSend}
                    disabled={!inputMessage.trim() || isTyping}
                    sx={{
                      bgcolor: 'primary.main',
                      color: '#fff',
                      '&:hover': { bgcolor: 'primary.dark' }
                    }}
                  >
                    <SendIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="リセット">
                  <IconButton
                    onClick={handleResetChat}
                    disabled={isTyping}
                    sx={{ color: 'primary.main' }}
                  >
                    <RestartAltIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>
          </Paper>
        </Box>
        {/* 蜿ｳ繧ｫ繝ｩ繝��医Ξ繧ｳ繝｡繝ｳ繝臥ｵ先棡�� */}
        <Box
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'stretch',
            justifyContent: 'flex-start',
            bgcolor: 'background.paper',
            boxSizing: 'border-box',
            p: { xs: 2, md: 4 },
            height: '100%',
            overflow: 'auto',
            position: 'relative',
          }}
        >
          <Box sx={{
            width: '100%',
            maxWidth: { md: 'calc(100vw - 96px - 64px)', xs: '100%' },
            minWidth: 0,
            minHeight: 480,
            height: '100%',
            paddingTop: '24px',
            paddingRight: '24px',
            paddingBottom: '24px',
            paddingLeft: '24px',
            borderRadius: 4,
            border: '1.2px solid #3D371C',
            display: 'flex',
            flexDirection: 'column',
            flex: 1,
            alignItems: 'stretch',
            justifyContent: 'flex-start',
            background: '#FFFFFF',
            overflow: 'auto',
            margin: '0 auto',
            boxSizing: 'border-box',
            position: 'relative',
          }}>
            {/* 繧ｪ繝ｼ繝舌�繝ｬ繧､�九せ繝斐リ繝ｼ */}
            {showOverlay && (
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  bgcolor: 'rgba(255,255,255,0.75)',
                  zIndex: 10,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  animation: `${fadeIn} 0.3s`,
                }}
              >
                <CircularProgress color="primary" size={48} thickness={4} />
                <Box sx={{ mt: 2, color: 'primary.main', fontWeight: 700, fontSize: 18, letterSpacing: 1 }}>
                  クラブセット検索中
                </Box>
              </Box>
            )}
            {/* 繧ｯ繝ｩ繝悶そ繝ヨ繧ｫ繝ｼ繝芽｡ｨ遉ｺ */}
            {!clubSetsLoading && clubSetsError ? (
              <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'error.main', fontSize: 18 }}>
                {clubSetsError}
              </Box>
            ) : !clubSetsLoading && (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, overflowY: 'auto', maxHeight: '100%' }}>
                {clubSets.map((set, idx) => (
                  <Box
                    key={idx}
                    sx={{
                      animation: `${fadeIn} 0.6s ease-out ${idx * 0.15}s both`,
                      border: '1px solid rgba(153,16,250,0.2)',
                      borderRadius: 4,
                      p: 2,
                      boxShadow: '0 4px 20px rgba(153,16,250,0.08)',
                      background: 'rgba(255, 255, 255, 0.9)',
                      backdropFilter: 'blur(10px)',
                      transition: 'all 0.3s ease',
                      position: 'relative',
                      '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: '0 8px 24px rgba(153,16,250,0.12)',
                      }
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ fontWeight: 700, fontSize: 18, color: '#1A3A4A', flex: 1 }}>{set.set_name}</Box>
                      <Box sx={{ fontWeight: 500, fontSize: 15, color: 'primary.main' }}>マッチング度: {set.match}%</Box>
                    </Box>
                    <Box sx={{ color: '#7A869A', fontSize: 14, mb: 1 }}>{set.description}</Box>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {set.clubs.map((club, cidx) => (
                        <Box
                          key={cidx}
                          sx={{
                            border: '1px solid #DDD',
                            borderRadius: 2,
                            px: 1.5,
                            py: 0.5,
                            fontSize: 13,
                            bgcolor: '#fff',
                            animation: `${fadeIn} 0.4s ease-out ${idx * 0.15 + 0.2}s both`,
                            position: 'relative',
                          }}
                        >
                          {club.type}: {club.brand} {club.model} {club.flex && `(${club.flex})`}
                        </Box>
                      ))}
                    </Box>
                  </Box>
                ))}
              </Box>
            )}
          </Box>
        </Box>
</Box>
</ThemeProvider>
);
}

function RecommendationResult({ recommendation }) {
  return (
    <Box sx={{ p: 0, height: '100%' }}>
      <Box sx={{ fontWeight: 700, fontSize: 16, mb: 2, color: '#1A3A4A' }}>
        クラブセット提案
      </Box>
      <Box sx={{ fontSize: 16, color: '#222' }}>
        <div>ドライバー: {recommendation.driver}</div>
        <div>アイアン: {recommendation.iron}</div>
        <div>パター: {recommendation.putter}</div>
        {recommendation.wedge && <div>ウェッジ: {recommendation.wedge}</div>}
      </Box>
    </Box>
);
}

export default App;