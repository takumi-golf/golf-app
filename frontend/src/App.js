import React, { useState, useRef, useEffect } from 'react';
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
import Button from '@mui/material/Button';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import Rating from '@mui/material/Rating';
import ShareIcon from '@mui/icons-material/Share';
import CloseIcon from '@mui/icons-material/Close';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import ClubRecommendations from './components/ClubRecommendations';
import { Tabs, Tab, LinearProgress } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import TwitterIcon from '@mui/icons-material/Twitter';
import { styled } from '@mui/material/styles';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Terms from './components/Terms';
import Privacy from './components/Privacy';
import MenuIcon from '@mui/icons-material/Menu';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import DescriptionIcon from '@mui/icons-material/Description';
import PolicyIcon from '@mui/icons-material/Policy';
import Link from '@mui/material/Link';
import DiagnosisScreen from './components/DiagnosisScreen';

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
    primary: {
      main: '#222', // Apple風ニュートラル
      light: '#E3E6EA',
      dark: '#888',
      contrastText: '#fff',
    },
    background: {
      default: '#F7F9FB',
      paper: '#fff',
    },
    text: {
      primary: '#222',
      secondary: '#555',
      disabled: '#B0B0B0',
    },
    divider: '#E3E6EA',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
fontWeight: 600,
          textTransform: 'none',
          '&:hover': {
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }
        },
        containedPrimary: {
          background: 'linear-gradient(45deg, #1976D2 0%, #2196F3 100%)',
          '&:hover': {
            background: 'linear-gradient(45deg, #1565C0 0%, #1976D2 100%)'
          }
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          border: '1px solid #E0E0E0',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }
      }
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(45deg, #1976D2 0%, #2196F3 100%)',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
        }
      }
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          backgroundColor: '#E3F2FD'
        },
        bar: {
          backgroundColor: '#1976D2'
        }
      }
    },
    MuiRadio: {
      styleOverrides: {
        root: {
          color: '#90CAF9',
          '&.Mui-checked': {
            color: '#1976D2'
          }
        }
      }
    }
  },
  typography: {
    fontFamily: [
      'SF Pro Display',
      'Noto Sans JP',
      'system-ui',
      'Arial',
      'sans-serif'
    ].join(','),
    h6: {
      fontWeight: 700,
      color: '#222',
    },
    body1: {
      lineHeight: 1.6
    }
  }
});

const initialRecommendation = {
  driver: '初心者向けドライバー',
  iron: 'ゲーム改善用アイアン',
  putter: 'ストローク安定型パター'
};

// デフォルトのカスタムセット4つ（14本クラブ情報付き）
const defaultClubSets = [
  {
    set_name: 'カスタムセットA',
    match: 90,
    clubs: [
      { type: 'ドライバー', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '3W', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '5W', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '4U', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '5I', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '6I', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '7I', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '8I', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: '9I', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: 'PW', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: 'AW', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: 'SW', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: 'LW', brand: 'NIKE', model: 'VR Pro', flex: 'S' },
      { type: 'パター', brand: 'NIKE', model: 'Method', flex: '' }
    ]
  },
  {
    set_name: 'カスタムセットB',
    match: 85,
    clubs: [
      { type: 'ドライバー', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '3W', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '5W', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '4U', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '5I', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '6I', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '7I', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '8I', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: '9I', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: 'PW', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: 'AW', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: 'SW', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: 'LW', brand: 'adidas', model: 'Tour360', flex: 'S' },
      { type: 'パター', brand: 'adidas', model: 'PureRoll', flex: '' }
    ]
  },
  {
    set_name: 'カスタムセットC',
    match: 80,
    clubs: [
      { type: 'ドライバー', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '3W', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '5W', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '4U', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '5I', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '6I', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '7I', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '8I', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: '9I', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: 'PW', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: 'AW', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: 'SW', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: 'LW', brand: 'PUMA', model: 'KING', flex: 'S' },
      { type: 'パター', brand: 'PUMA', model: 'KING', flex: '' }
    ]
  },
  {
    set_name: 'カスタムセットD',
    match: 75,
    clubs: [
      { type: 'ドライバー', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '3W', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '5W', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '4U', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '5I', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '6I', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '7I', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '8I', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: '9I', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: 'PW', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: 'AW', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: 'SW', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: 'LW', brand: 'Titleist', model: 'TSi3', flex: 'S' },
      { type: 'パター', brand: 'Titleist', model: 'Scotty', flex: '' }
    ]
  }
];

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

// サンプルのクラブセット4つ（マッチ度順でソートして表示）
const sampleClubSets = [
  {
    set_name: 'カスタムセットA',
    match: 92,
    driver: 'NIKE VR Pro ドライバー',
    review: '「飛距離が伸びてスコアも安定しました！」',
    stars: 5,
    reviews: 128
  },
  {
    set_name: 'カスタムセットB',
    match: 88,
    driver: 'adidas Tour360 ドライバー',
    review: '「方向性が良くなりました！」',
    stars: 4,
    reviews: 102
  },
  {
    set_name: 'カスタムセットC',
    match: 84,
    driver: 'PUMA KING ドライバー',
    review: '「打感が最高です！」',
    stars: 4,
    reviews: 76
  },
  {
    set_name: 'カスタムセットD',
    match: 80,
    driver: 'Titleist TSi3 ドライバー',
    review: '「初心者でも扱いやすい！」',
    stars: 3,
    reviews: 54
  }
].sort((a, b) => b.match - a.match);

// アニメーション付きアイコンボタン
const AnimatedIconButton = styled(IconButton)(({ theme }) => ({
  width: 'auto',
  minWidth: 32,
  height: 38,
  borderRadius: 18,
  border: '1.2px solid #e0e0e2',
  background: '#fff',
  boxShadow: '0 1px 4px rgba(60,60,60,0.06)',
  fontSize: 18,
  transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
  overflow: 'hidden',
  paddingLeft: theme.spacing(1),
  paddingRight: `calc(${theme.spacing(1)} + 3px)`,
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(0.7),
  color: '#666',
  position: 'relative',
  '& .btn-label': {
    opacity: 0,
    maxWidth: 0,
    marginLeft: 0,
    transition: 'max-width 1.5s cubic-bezier(.4,2,.6,1), opacity 0.22s, margin-left 0.22s, color 0.22s',
    whiteSpace: 'nowrap',
    display: 'inline-block',
    color: '#666',
    fontWeight: 500,
    fontSize: 13,
    letterSpacing: 0.2,
    overflow: 'hidden',
  },
  '&:hover': {
    background: '#f3f3f4',
    boxShadow: '0 2px 8px rgba(60,60,60,0.10)',
    color: '#222',
    borderColor: '#bdbdbf',
  },
  '&:hover .btn-label': {
    opacity: 1,
    maxWidth: 200,
    marginLeft: theme.spacing(0.7),
    color: '#222',
  },
  '&:active': {
    background: '#ededee',
    boxShadow: 'none',
  },
  '&.Mui-disabled': {
    color: '#bbb',
    background: '#f5f5f7',
    boxShadow: 'none',
    opacity: 0.5,
    borderColor: '#e0e0e2',
  }
}));

function App() {
  const theme = useTheme();
  const navigate = useNavigate();
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
  const optionsRef = useRef(null);
  const optionsBarRef = useRef(null);
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  const [selectedNav, setSelectedNav] = useState('ai');
  const [clubSets, setClubSets] = useState([]);
  const [clubSetsLoading, setClubSetsLoading] = useState(false);
  const [clubSetsError, setClubSetsError] = useState(null);
  const [showOverlay, setShowOverlay] = useState(false);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [carouselTab, setCarouselTab] = useState(0);
  const carouselTabs = ['ドライバー', 'ウッド', 'アイアン', 'ウェッジ', 'パター'];
  const [anchorEl, setAnchorEl] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const isMobile = useMediaQuery(theme.breakpoints.down('lg'));
  const [showLoadingAnimation, setShowLoadingAnimation] = useState(false);
  const recommendRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // isTypingがfalseになったらフォーカスを当てる
  useEffect(() => {
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
    setStep(0);
    setAnswers([]);
    setClubSets([]);
    setClubSetsError(null);
    setClubSetsLoading(false);
    setShowChat(false); // スタート画面に戻す
  };

  // 初期表示時にAPIを呼び出し
  useEffect(() => {
    const fetchClubSets = async () => {
      setClubSetsLoading(true);
      setClubSetsError(null);
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
        setClubSetsLoading(false);
      }
    };
    fetchClubSets();
  }, []);

  // clubSetsLoadingの状態に応じてオーバーレイを表示
  useEffect(() => {
    if (clubSetsLoading) {
      setShowOverlay(true);
    } else {
      const timer = setTimeout(() => setShowOverlay(false), 800);
      return () => clearTimeout(timer);
    }
  }, [clubSetsLoading]);

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
          if (chatArea && optionsRef.current) {
            chatArea.scrollTop += optionsRef.current.offsetHeight + 68;
          }
        }
      }, 100);
    } else {
      // すべての質問が終わったらローディングアニメーションを表示
      setShowLoadingAnimation(true);
      // 3秒後にAPI呼び出し
      setTimeout(() => {
        setShowLoadingAnimation(false);
        fetchClubSetsByAnswers(newAnswers);
      }, 3000);
    }
  };

  // 選択肢ベースでAPI呼び出し
  const fetchClubSetsByAnswers = async (answersArr) => {
    setClubSetsLoading(true);
    setClubSetsError(null);
    try {
      const userData = {
        golf_history: answersArr[0],
        score: answersArr[1],
        main_club: answersArr[2],
        improvement_point: answersArr[3]
      };
      const sets = await getClubSetRecommendations(userData);
      sets.sort((a, b) => b.match - a.match);
      setClubSets(sets);
    } catch (err) {
      setClubSetsError('クラブセットの検索に失敗しました');
    } finally {
      setClubSetsLoading(false);
    }
  };

  // --- 追加: ユーザーアバター用 ---
  const userAvatar = <Avatar sx={{ bgcolor: '#222', color: '#fff', width: 32, height: 32, fontSize: 18 }}>U</Avatar>;

  const handleMenuOpen = (event) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);
  const handleMenuReset = () => {
    handleMenuClose();
    handleResetChat();
  };

  // 一つ前に戻るボタン
  const handleBack = () => {
    if (answers.length > 0) {
      const newAnswers = answers.slice(0, -1);
      setAnswers(newAnswers);
      setStep(newAnswers.length); // answersの長さにstepを合わせる
    }
  };

  const handleDrawerOpen = () => setDrawerOpen(true);
  const handleDrawerClose = () => setDrawerOpen(false);

  // チャット完了時にレコメンドエリアへ自動スクロール（isMobileのみ）
  useEffect(() => {
    if (isMobile && answers.length === chatFlow.length && recommendRef.current) {
      setTimeout(() => {
        recommendRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 400); // レコメンド描画タイミングに合わせて少し遅延
    }
  }, [isMobile, answers.length]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <style>{`
        body {
          background: #f7f7f8 !important;
        }
        ::-webkit-scrollbar {
          width: 8px;
          background: #f7f7f8;
        }
        ::-webkit-scrollbar-thumb {
          background: #e0e0e2;
          border-radius: 4px;
        }
      `}</style>
      <Routes>
        <Route path="/terms" element={<Terms />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/diagnosis" element={<DiagnosisScreen onReset={() => navigate('/')} />} />
        <Route path="/" element={
          <>
            {isMobile ? (
              <Box sx={{ width: '100vw', minHeight: '100vh', bgcolor: '#fff', pb: 8 }}>
                {/* ヘッダー */}
                <Box sx={{ 
                  position: 'fixed', 
                  top: 0, 
                  left: 0, 
                  width: '100vw', 
                  height: 56, 
                  zIndex: 1200, 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  boxShadow: 4, 
                  background: '#fff', 
                  color: '#222' 
                }}>
                  <Typography sx={{ 
                    fontWeight: 700,
                    position: 'absolute',
                    left: '50%',
                    transform: 'translateX(-50%)'
                  }}>
                    Swing Fit Pro
                  </Typography>
                  <IconButton 
                    edge="end" 
                    onClick={handleDrawerOpen} 
                    sx={{ 
                      position: 'absolute',
                      right: 8,
                      color: '#222'
                    }}
                  >
                    <MenuIcon />
                  </IconButton>
                </Box>
                {/* Drawer */}
                <Drawer anchor="left" open={drawerOpen} onClose={handleDrawerClose}>
                  <List sx={{ width: 240 }}>
                    <ListItem button component={Link} href="/" onClick={handleDrawerClose}>
                      <ListItemIcon><HomeIcon /></ListItemIcon>
                      <ListItemText primary="AI診断" />
                    </ListItem>
                    <ListItem button component={Link} href="/terms" onClick={handleDrawerClose}>
                      <ListItemIcon><DescriptionIcon /></ListItemIcon>
                      <ListItemText primary="利用規約" />
                    </ListItem>
                    <ListItem button component={Link} href="/privacy" onClick={handleDrawerClose}>
                      <ListItemIcon><PolicyIcon /></ListItemIcon>
                      <ListItemText primary="プライバシーポリシー" />
                    </ListItem>
                    <ListItem button component={Link} href="https://x.com/golf_ai_t" target="_blank" rel="noopener noreferrer" onClick={handleDrawerClose}>
                      <ListItemIcon><TwitterIcon /></ListItemIcon>
                      <ListItemText primary="X (旧Twitter)" />
                    </ListItem>
                  </List>
                </Drawer>
                {/* メイン */}
                <Box sx={{ pt: 7, pb: 10 }}>
                  <Box sx={{
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
                    gap: 3,
                  }}>
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
                      }}
                      onClick={() => navigate('/diagnosis')}
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
                </Box>
                {/* フッター */}
                <Box sx={{ position: 'fixed', bottom: 0, left: 0, width: '100%', bgcolor: '#fff', borderTop: '1px solid #eee', py: 1, px: 2, display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', zIndex: 1200 }}>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <IconButton href="/" size="small"><HomeIcon fontSize="small" /></IconButton>
                    <IconButton href="/terms" size="small"><DescriptionIcon fontSize="small" /></IconButton>
                    <IconButton href="/privacy" size="small"><PolicyIcon fontSize="small" /></IconButton>
                    <IconButton href="https://x.com/golf_ai_t" target="_blank" rel="noopener noreferrer" size="small"><TwitterIcon fontSize="small" /></IconButton>
                  </Box>
                </Box>
              </Box>
            ) : (
              <>
                {/* ヘッダー */}
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
                    boxShadow: 4,
                    background: '#fff',
                    color: '#222',
                    backdropFilter: 'blur(10px)',
                  }}
                >
                  {/* ロゴ・タイトル部分 */}
                  <Box sx={{
                    width: { xs: 0, md: 74 },
                    height: '100%',
                    bgcolor: { md: '#111', xs: 'transparent' },
                    flexShrink: 0,
                    display: { xs: 'none', md: 'flex' },
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <img src="/service-logos/logo-vertical.png" alt="AI Golf" style={{ height: 46, maxWidth: 74, objectFit: 'contain', background: 'transparent', display: 'block', margin: 0, padding: 0 }} />
                  </Box>
                </Box>
                {/* 3カラムレイアウト */}
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    width: '100vw',
                    height: '100vh',
                    background: 'linear-gradient(135deg, #F7F9FB 0%, #E3E6EA 100%)',
                    alignItems: 'stretch',
                    pt: '56px',
                    overflow: 'hidden',
                    position: 'fixed',
                    top: 0,
                    left: 0,
                  }}
                >
                  {/* サイドバー */}
                  <Box
                    sx={{
                      width: { xs: 0, md: 74 },
                      minWidth: { md: 74 },
                      bgcolor: { xs: 'transparent', md: '#fff' },
                      color: '#222',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'stretch',
                      justifyContent: 'flex-start',
                      pt: 2,
                      borderRight: { md: '1px solid', xs: 'none' },
                      borderColor: { md: '#E3E6EA', xs: 'transparent' },
                      flexShrink: 0,
                      height: '100%',
                      overflow: 'auto',
                      borderRadius: 0,
                      boxShadow: { md: 2, xs: 0 },
                      transition: 'all 0.25s',
                      p: 0,
                      m: 0,
                      boxSizing: 'border-box',
                    }}
                  >
                    {/* アイコンとテキストをinfo系に統一 */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'center', mt: 1 }}>
                      <Box
                        sx={{
                          display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5, width: '100%', py: 1,
                          cursor: 'pointer',
                          transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                          bgcolor: selectedNav === 'ai' ? '#F7F9FB' : 'transparent',
                          color: selectedNav === 'ai' ? '#111' : '#222',
                          fontWeight: selectedNav === 'ai' ? 700 : 400,
                          boxShadow: selectedNav === 'ai' ? 2 : 0,
                          '& svg': { color: selectedNav === 'ai' ? '#111' : '#222' }
                        }}
                        tabIndex={0}
                        role="button"
                        onClick={() => {
                          setSelectedNav('ai');
                          setShowChat(false);
                          setStep(0);
                          setAnswers([]);
                        }}
                      >
                        <SmartToyIcon sx={{ fontSize: 23, mb: 0.5, transition: 'color 0.18s' }} />
                        <span style={{ fontWeight: 700, fontSize: 12, letterSpacing: 1 }}>AI診断</span>
                      </Box>
                    </Box>
                    {/* サイドバー下部：お問い合わせSNSリンク */}
                    <Box sx={{
                      mt: 'auto',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      py: 2,
                      gap: 0.5,
                    }}>
                      <Tooltip
                        title={<span>お問い合わせは<br />DMまで</span>}
                        arrow
                        placement="top"
                        PopperProps={{
                          modifiers: [
                            {
                              name: 'offset',
                              options: {
                                offset: [12, 8], // 左に12px、上に8pxずらす
                              },
                            },
                          ],
                        }}
                        componentsProps={{
                          tooltip: {
                            sx: {
                              fontSize: 13,
                              fontWeight: 500,
                              bgcolor: '#222',
                              color: '#fff',
                              borderRadius: 2,
                              px: 1.5,
                              py: 0.7,
                              boxShadow: '0 2px 8px rgba(0,0,0,0.10)'
                            }
                          }
                        }}
                      >
                        <IconButton
                          component="a"
                          href="https://x.com/golf_ai_t"
                          target="_blank"
                          sx={{
                            color: '#222',
                            p: 0.5,
                            '&:hover': {
                              color: '#1976D2',
                              opacity: 1,
                            }
                          }}
                        >
                          <img src="/sns-logos/logo-black.png" alt="Xロゴ" width="17" height="17" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </Box>
                  {/* 中央カラム */}
                  <Box sx={{
                    width: { lg: 486 },
                    flexShrink: 0,
                    display: 'flex',
                    flexDirection: 'column',
                    height: { md: 'calc(100vh - 56px - 32px)', xs: 'calc(100vh - 56px)' },
                    overflow: 'hidden',
                    borderRight: '1px solid #e0e0e2',
                    position: 'relative',
                    bgcolor: '#f7f7f8',
                    m: { md: 2, xs: 0 },
                    boxShadow: { md: 2, xs: 0 },
                    borderRadius: { md: '18px', xs: 0 },
                    transition: 'all 0.25s',
                    boxSizing: 'border-box',
                  }}>
                    {!showChat ? (
                      <Box sx={{
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
                        gap: 3,
                      }}>
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
                          }}
                          onClick={() => navigate('/diagnosis')}
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
                    ) : (
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
                              onClick={handleResetChat}
                              disabled={!showChat}
                              sx={{
                                color: (!showChat) ? '#bbb' : '#666',
                                opacity: (!showChat) ? 0.4 : 1,
                                cursor: (!showChat) ? 'default' : 'pointer',
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
                                {/* AIの発言（バブル・アイコンなし、ChatGPT風） */}
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
                                {/* ユーザー側（右側）領域＋アバター */}
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
                            {/* 上層：選択肢ボタン */}
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
                              onClick={handleResetChat}
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
                      </>
                    )}
                  </Box>
                  {/* 右カラム */}
                  <Box
                    sx={{
                      flex: 1,
                      minWidth: 0,
                      display: 'flex',
                      flexDirection: 'column',
                      height: 'calc(100vh - 56px)',
                      overflow: 'hidden',
                      bgcolor: '#F7F9FB',
                      borderLeft: '1px solid #E3E6EA'
                    }}
                  >
                    <Box
                      sx={{
                        height: '100%',
                        overflowY: 'auto',
                        boxSizing: 'border-box',
                        '&::-webkit-scrollbar': {
                          width: '8px',
                          background: '#E3E6EA'
                        },
                        '&::-webkit-scrollbar-thumb': {
                          backgroundColor: '#B0C4DE',
                          borderRadius: '4px'
                        }
                      }}
                    >
                      {!showChat || answers.length < chatFlow.length ? (
                        <Box
                          sx={{
                            height: '100%',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            textAlign: 'center',
                            px: 4,
                            py: 6,
                            gap: 2
                          }}
                        >
                          <Typography
                            sx={{
                              fontSize: 24,
                              fontWeight: 700,
                              color: '#1976D2',
                              mb: 2,
                              letterSpacing: 0.5
                            }}
                          >
                            {!showChat ? 
                              'あなたに最適なクラブセットを提案します' :
                              '診断を完了させてください'
                            }
                          </Typography>
                          {showChat && (
                            <Box sx={{ width: '100%', maxWidth: 400, mb: 3 }}>
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography sx={{ fontSize: 14, color: '#666' }}>
                                  質問 {answers.length + 1} / {chatFlow.length}
                                </Typography>
                                <Typography sx={{ fontSize: 14, color: '#666' }}>
                                  {Math.round((answers.length / chatFlow.length) * 100)}%
                                </Typography>
                              </Box>
                              <LinearProgress 
                                variant="determinate" 
                                value={(answers.length / chatFlow.length) * 100}
                                sx={{
                                  height: 8,
                                  borderRadius: 4,
                                  backgroundColor: '#E3E6EA',
                                  '& .MuiLinearProgress-bar': {
                                    borderRadius: 4,
                                    background: 'linear-gradient(45deg, #1976D2 0%, #2196F3 100%)'
                                  }
                                }}
                              />
                            </Box>
                          )}
                          <Typography
                            sx={{
                              fontSize: 16,
                              color: '#666',
                              lineHeight: 1.8,
                              maxWidth: '80%',
                              mb: 3
                            }}
                          >
                            {!showChat ? 
                              'いくつかの質問に答えるだけで、あなたのスイングやプレースタイルに最適な14本のクラブセットをAIが自動で選定します。' :
                              'すべての質問に回答すると、あなたに最適なクラブセットを提案します。'
                            }
                          </Typography>
                          {!showChat && (
                            <Box
                              sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                gap: 2,
                                mt: 2
                              }}
                            >
                              <Box
                                sx={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 1,
                                  color: '#666',
                                  fontSize: 14
                                }}
                              >
                                <SmartToyIcon sx={{ fontSize: 20 }} />
                                <span>AIによる最適なクラブ選定</span>
                              </Box>
                              <Box
                                sx={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 1,
                                  color: '#666',
                                  fontSize: 14
                                }}
                              >
                                <HistoryIcon sx={{ fontSize: 20 }} />
                                <span>プロ・アマチュアのデータベース</span>
                              </Box>
                              <Box
                                sx={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 1,
                                  color: '#666',
                                  fontSize: 14
                                }}
                              >
                                <SettingsIcon sx={{ fontSize: 20 }} />
                                <span>詳細なスペック情報</span>
                              </Box>
                            </Box>
                          )}
                        </Box>
                      ) : showLoadingAnimation ? (
                        <Box
                          sx={{
                            height: '100%',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            textAlign: 'center',
                            px: 4,
                            py: 6,
                            gap: 3
                          }}
                        >
                          <CircularProgress
                            size={60}
                            thickness={4}
                            sx={{
                              color: '#1976D2',
                              animation: 'spin 1.5s linear infinite',
                              '@keyframes spin': {
                                '0%': {
                                  transform: 'rotate(0deg)',
                                },
                                '100%': {
                                  transform: 'rotate(360deg)',
                                },
                              },
                            }}
                          />
                          <Typography
                            sx={{
                              fontSize: 20,
                              fontWeight: 700,
                              color: '#1976D2',
                              mb: 1
                            }}
                          >
                            AIが最適なクラブセットを選定中...
                          </Typography>
                          <Typography
                            sx={{
                              fontSize: 14,
                              color: '#666',
                              maxWidth: '80%',
                              lineHeight: 1.6
                            }}
                          >
                            あなたの回答を分析し、最適なクラブセットを提案します。
                            <br />
                            お待ちください。
                          </Typography>
                        </Box>
                      ) : (
                        <ClubRecommendations />
                      )}
                    </Box>
                  </Box>
                </Box>
              </>
            )}
          </>
        } />
      </Routes>
    </ThemeProvider>
  );
}

export default App;