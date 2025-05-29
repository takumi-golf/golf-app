import React, { useState } from 'react';
import { Box, Paper, Typography, Button, Avatar, Tabs, Tab, Chip, Rating, IconButton } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import SearchIcon from '@mui/icons-material/Search';
import StorefrontIcon from '@mui/icons-material/Storefront';
import { motion } from 'framer-motion';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import SwipeableViews from 'react-swipeable-views';
import GolfCourseIcon from '@mui/icons-material/GolfCourse';
import Fab from '@mui/material/Fab';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import MatchBadge from './MatchBadge';
import RateReviewIcon from '@mui/icons-material/RateReview';
import TextField from '@mui/material/TextField';
import ReplayIcon from '@mui/icons-material/Replay';
import { useNavigate } from 'react-router-dom';
import ReactGA from "react-ga4";

// カテゴリごとのクラブデータ（β版用・TaylorMade/Titleistのみ）
const clubData = {
  driver: [
    {
      id: 'TM_ST2_DRV',
      brand: 'TaylorMade',
      name: 'Stealth 2',
      maker: 'TaylorMade',
      model: 'Stealth 2',
      category: 'ドライバー',
      year: 2023,
      loft: '9°/10.5°/12°',
      shaft_flex: 'R/S/X',
      length: '45.75"',
      head_volume: '460cc',
      price: 45000,
      price_label: '約45,000円～',
      used_price: 21800,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 95,
      matchReason: '60X Carbon Twist Face搭載、FARGIVENESS（飛距離+寛容性）を追求',
      specs: 'ロフト: 9°/10.5°/12° / シャフト: R/S/X / 長さ: 45.75" / 460cc',
      releaseDate: '2023-01-15',
      image: '/images/clubs/driver-taylormade-stealth2.jpg',
      rating: 4.8,
      reviews: 128,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/%E3%82%B9%E3%83%86%E3%83%AB%E3%82%B92+%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/%E3%82%B9%E3%83%86%E3%83%AB%E3%82%B92%20%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/668271'
    },
    {
      id: 'TM_SIM2M_DRV',
      brand: 'TaylorMade',
      name: 'SIM2 Max',
      maker: 'TaylorMade',
      model: 'SIM2 Max',
      category: 'ドライバー',
      year: 2021,
      loft: '9°/10.5°/12°',
      shaft_flex: 'R/S/X',
      length: '45.5"',
      head_volume: '460cc',
      price: 38000,
      price_label: '約38,000円～',
      used_price: 24200,
      stock_status: '在庫あり',
      recommended_for: '初心者・中級者',
      match: 85,
      matchReason: '高弾道・寛容性重視の設計',
      specs: 'ロフト: 9°/10.5°/12° / シャフト: R/S/X / 長さ: 45.5" / 460cc',
      releaseDate: '2021-02-01',
      image: '/images/clubs/driver-taylormade-sim2max.jpg',
      rating: 4.7,
      reviews: 95,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/sim2+max+%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/%E3%82%B7%E3%83%A0%20max%20%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/680893'
    },
    {
      id: 'TT_TSR2_DRV',
      brand: 'Titleist',
      name: 'TSR2',
      maker: 'Titleist',
      model: 'TSR2',
      category: 'ドライバー',
      year: 2022,
      loft: '8°/9°/10°/11°',
      shaft_flex: 'R/S/X',
      length: '45.5"',
      head_volume: '460cc',
      price: 48000,
      price_label: '約48,000円～',
      used_price: 22980,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 75,
      matchReason: '高初速・高弾道設計、寛容性も両立',
      specs: 'ロフト: 8°/9°/10°/11° / シャフト: R/S/X / 長さ: 45.5" / 460cc',
      releaseDate: '2022-09-01',
      image: '/images/clubs/driver-titleist-tsr2.jpg',
      rating: 4.9,
      reviews: 156,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/TSR2+%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/TSR2%20%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://www.golfpartner.jp/shop/usedgoods/h010001_m15_b153709/?search=x&model_code=422691'
    },
    {
      id: 'TT_TSI3_DRV',
      brand: 'Titleist',
      name: 'TSi3',
      maker: 'Titleist',
      model: 'TSi3',
      category: 'ドライバー',
      year: 2020,
      loft: '8°/9°/10°',
      shaft_flex: 'R/S/X',
      length: '45.5"',
      head_volume: '460cc',
      price: 36000,
      price_label: '約36,000円～',
      used_price: 25980,
      stock_status: '在庫あり',
      recommended_for: '上級者',
      match: 65,
      matchReason: '操作性重視の上級者向けモデル',
      specs: 'ロフト: 8°/9°/10° / シャフト: R/S/X / 長さ: 45.5" / 460cc',
      releaseDate: '2020-10-01',
      image: '/images/clubs/driver-titleist-tsi3.jpg',
      rating: 4.8,
      reviews: 110,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/TSi3+%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/TSi3%20%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://www.golfkids.co.jp/search/model/item/?class%5B0%5D=1001&model=19691&current_class_code='
    }
  ],
  wood: [
    {
      id: 'TM_ST2_FW',
      brand: 'TaylorMade',
      name: 'Stealth 2',
      maker: 'TaylorMade',
      model: 'Stealth 2',
      category: 'フェアウェイウッド',
      year: 2023,
      loft: '3W:15°/5W:18°',
      shaft_flex: 'R/S/X',
      length: '43.25"/42.25"',
      head_volume: '185cc/170cc',
      price: 31800,
      price_label: '約31,800円～',
      used_price: 19980,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 92,
      matchReason: '高初速・寛容性の両立',
      specs: 'ロフト: 3W:15°/5W:18° / シャフト: R/S/X / 長さ: 43.25"/42.25" / 185cc/170cc',
      releaseDate: '2023-02-01',
      image: '/images/clubs/wood-taylormade-stealth2.jpg',
      rating: 4.8,
      reviews: 88,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/%E3%82%B9%E3%83%86%E3%83%AB%E3%82%B32+%E3%83%95%E3%82%A7%E3%82%A2%E3%82%A6%E3%82%A7%E3%82%A4%E3%82%A6%E3%83%83%E3%83%89+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/%E3%82%B9%E3%83%86%E3%83%AB%E3%82%B32%20%E3%83%95%E3%82%A7%E3%82%A2%E3%82%A6%E3%82%A7%E3%82%A4%E3%82%A6%E3%83%83%E3%83%89%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://www.golfkids.co.jp/search/model/item/?maker%5B%5D=16&class%5B%5D=1002&model=21871'
    },
    {
      id: 'TT_TSI3_FW',
      brand: 'Titleist',
      name: 'TSi3',
      maker: 'Titleist',
      model: 'TSi3',
      category: 'フェアウェイウッド',
      year: 2020,
      loft: '3W:15°/5W:18°',
      shaft_flex: 'R/S/X',
      length: '43.25"/42.25"',
      head_volume: '175cc',
      price: 38000,
      price_label: '約38,000円～',
      used_price: 18980,
      stock_status: '在庫あり',
      recommended_for: '上級者',
      match: 85,
      matchReason: '操作性・打感重視の上級者向け',
      specs: 'ロフト: 3W:15°/5W:18° / シャフト: R/S/X / 長さ: 43.25"/42.25" / 175cc',
      releaseDate: '2020-10-01',
      image: '/images/clubs/wood-titleist-tsi3.jpg',
      rating: 4.7,
      reviews: 76,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/TSi3+%E3%83%95%E3%82%A7%E3%82%A2%E3%82%A6%E3%82%A7%E3%82%A4%E3%82%A6%E3%83%83%E3%83%89+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/TSi3%20%E3%83%95%E3%82%A7%E3%82%A2%E3%82%A6%E3%82%A7%E3%82%A4%E3%82%A6%E3%83%83%E3%83%89%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://www.aftergolf.net/gekiyasu/club/1/1/12/TL/'
    }
  ],
  iron: [
    {
      id: 'TM_SIM2M_IRN',
      brand: 'TaylorMade',
      name: 'SIM2 Max',
      maker: 'TaylorMade',
      model: 'SIM2 Max',
      category: 'アイアン',
      year: 2021,
      loft: '7I:34°',
      shaft_flex: 'R/S',
      length: '37.00"',
      club_weight: '-',
      price: 45000,
      price_label: '約45,000円～',
      used_price: 35980,
      stock_status: '在庫あり',
      recommended_for: '初心者・中級者',
      match: 90,
      matchReason: '高弾道・寛容性重視の設計',
      specs: '7I:34° / シャフト: R/S / 長さ: 37.00"',
      releaseDate: '2021-03-01',
      image: '/images/clubs/iron-taylormade-sim2max.jpg',
      rating: 4.8,
      reviews: 142,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/SIM2+MAX+%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/SIM2%20MAX%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/680893'
    },
    {
      id: 'TM_P790_IRN',
      brand: 'TaylorMade',
      name: 'P790',
      maker: 'TaylorMade',
      model: 'P790',
      category: 'アイアン',
      year: 2023,
      loft: '7I:30.5°',
      shaft_flex: 'R/S/X',
      length: '37.00"',
      club_weight: '-',
      price: 150000,
      price_label: '約150,000円～',
      used_price: 44427,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 95,
      matchReason: '飛距離・打感・寛容性のバランス',
      specs: '7I:30.5° / シャフト: R/S/X / 長さ: 37.00" / 5本セット',
      releaseDate: '2023-07-01',
      image: '/images/clubs/iron-taylormade-p790.jpg',
      rating: 4.9,
      reviews: 168,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/P790+%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/P790%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/P790%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3'
    },
    {
      id: 'TT_T100_IRN',
      brand: 'Titleist',
      name: 'T100',
      maker: 'Titleist',
      model: 'T100',
      category: 'アイアン',
      year: 2023,
      loft: '7I:34°',
      shaft_flex: 'R/S/X',
      length: '37.00"',
      club_weight: '-',
      price: 125000,
      price_label: '約125,000円～',
      used_price: 47980,
      stock_status: '在庫あり',
      recommended_for: '上級者',
      match: 92,
      matchReason: 'ツアープロも愛用する操作性',
      specs: '7I:34° / シャフト: R/S/X / 長さ: 37.00" / 6本セット',
      releaseDate: '2023-08-01',
      image: '/images/clubs/iron-titleist-t100.jpg',
      rating: 4.9,
      reviews: 156,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/T100+%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/T100%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/T100%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3'
    },
    {
      id: 'TT_T200_IRN',
      brand: 'Titleist',
      name: 'T200',
      maker: 'Titleist',
      model: 'T200',
      category: 'アイアン',
      year: 2023,
      loft: '7I:30.5°',
      shaft_flex: 'R/S/X',
      length: '37.00"',
      club_weight: '-',
      price: 125000,
      price_label: '約125,000円～',
      used_price: 97980,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 90,
      matchReason: '飛距離・寛容性のバランス',
      specs: '7I:30.5° / シャフト: R/S/X / 長さ: 37.00" / 6本セット',
      releaseDate: '2023-08-01',
      image: '/images/clubs/iron-titleist-t200..jpg',
      rating: 4.8,
      reviews: 126,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/T200+%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/T200%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/T200%20%E3%82%A2%E3%82%A4%E3%82%A2%E3%83%B3'
    }
  ],
  wedge: [
    {
      id: 'TM_HITOE_WDG',
      brand: 'TaylorMade',
      name: 'Hi-Toe RAW',
      maker: 'TaylorMade',
      model: 'Hi-Toe RAW',
      category: 'ウェッジ',
      year: 2023,
      loft: '56°/58°/60°',
      shaft_flex: 'Wedge',
      length: '35.25"',
      club_weight: '-',
      price: 16000,
      price_label: '約16,000円～',
      used_price: 6490,
      stock_status: '在庫あり',
      recommended_for: '中級者・上級者',
      match: 88,
      matchReason: '多彩なロフト展開とスピン性能',
      specs: 'ロフト: 56°/58°/60° / シャフト: Wedge / 長さ: 35.25"',
      releaseDate: '2023-04-01',
      image: '/images/clubs/wedge-taylormade-hitoe.jpg',
      rating: 4.8,
      reviews: 102,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/Hi-Toe+RAW+%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/Hi-Toe%20RAW%20%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/Hi-Toe%20RAW%20%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8'
    },
    {
      id: 'TT_SM9_WDG',
      brand: 'Titleist',
      name: 'Vokey SM9',
      maker: 'Titleist',
      model: 'Vokey SM9',
      category: 'ウェッジ',
      year: 2021,
      loft: '50°/52°/54°/56°/58°/60°',
      shaft_flex: 'Wedge',
      length: '35.50"/35.25"/35.00"',
      club_weight: '-',
      price: 18000,
      price_label: '約18,000円～',
      used_price: 6600,
      stock_status: '在庫あり',
      recommended_for: '全レベル',
      match: 90,
      matchReason: '世界中のツアープロが信頼するスピン性能',
      specs: 'ロフト: 50°/52°/54°/56°/58°/60° / シャフト: Wedge / 長さ: 35.50"/35.25"/35.00"',
      releaseDate: '2021-03-01',
      image: '/images/clubs/wedge-titleist-sm9.jpg',
      rating: 4.9,
      reviews: 120,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/Vokey+SM9+%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/Vokey%20SM9%20%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/Vokey%20SM9%20%E3%82%A6%E3%82%A7%E3%83%83%E3%82%B8'
    }
  ],
  putter: [
    {
      id: 'TM_SPDRX_PTR',
      brand: 'TaylorMade',
      name: 'Spider Tour X',
      maker: 'TaylorMade',
      model: 'Spider Tour X',
      category: 'パター',
      year: 2023,
      loft: '3°',
      shaft_flex: '-',
      length: '33"/34"/35"',
      club_weight: '-',
      price: 38000,
      price_label: '約38,000円～',
      used_price: 32980,
      stock_status: '在庫あり',
      recommended_for: '全レベル',
      match: 90,
      matchReason: '安定したストロークと高い直進性',
      specs: 'ロフト: 3° / 長さ: 33"/34"/35"',
      releaseDate: '2023-06-01',
      image: '/images/clubs/putter-taylormade-spider.jpg',
      rating: 4.8,
      reviews: 89,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/Spider+Tour+X+%E3%83%91%E3%82%BF%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/Spider%20Tour%20X%20%E3%83%91%E3%82%BF%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/Spider%20Tour%20X%20%E3%83%91%E3%82%BF%E3%83%BC'
    },
    {
      id: 'TT_PHX5_PTR',
      brand: 'Titleist',
      name: 'Phantom X 5',
      maker: 'Titleist',
      model: 'Phantom X 5',
      category: 'パター',
      year: 2023,
      loft: '3.5°',
      shaft_flex: '-',
      length: '33"/34"/35"',
      club_weight: '-',
      price: 42000,
      price_label: '約42,000円～',
      used_price: 41750,
      stock_status: '在庫あり',
      recommended_for: '全レベル',
      match: 92,
      matchReason: '高い安定性と直進性、ツアープロも愛用',
      specs: 'ロフト: 3.5° / 長さ: 33"/34"/35"',
      releaseDate: '2023-07-01',
      image: '/images/clubs/putter-titleist-phantom.jpg',
      rating: 4.9,
      reviews: 102,
      rakutenUrl: 'https://search.rakuten.co.jp/search/mall/Phantom+X+5+%E3%83%91%E3%82%BF%E3%83%BC+%E6%96%B0%E5%93%81/',
      yahooUrl: 'https://shopping.yahoo.co.jp/search/Phantom%20X%205%20%E3%83%91%E3%82%BF%E3%83%BC%20%E6%96%B0%E5%93%81/0/',
      usedUrl: 'https://jp.mercari.com/s/Phantom%20X%205%20%E3%83%91%E3%82%BF%E3%83%BC'
    }
  ]
};

// グラスモーフィズム・ニューモーフィズム用スタイル
const glassmorphismStyle = {
  background: 'rgba(255, 255, 255, 0.25)',
  backdropFilter: 'blur(10px)',
  borderRadius: '20px',
  border: '1px solid rgba(255, 255, 255, 0.18)',
  boxShadow: '0 8px 32px 0 rgba(0,0,0,0.06), 0 1.5px 8px 0 rgba(0,0,0,0.02)'
};

// Apple風カードスタイル
const appleCardStyle = {
  background: 'linear-gradient(135deg, #fafdff 60%, #e9eef3 100%)',
  border: '1.5px solid #e3e6ea',
  boxShadow: '0 4px 24px 0 rgba(25,118,210,0.07), 0 1.5px 8px 0 rgba(0,0,0,0.03)',
  borderRadius: { xs: 16, md: 8 },
};

// マッチ度ランクを返す関数
const getMatchRank = (match) => {
  if (match >= 90) return { rank: 'S', color: '#FFD700', emoji: '🥇' };
  if (match >= 80) return { rank: 'A', color: '#00E5FF', emoji: '🥈' };
  if (match >= 70) return { rank: 'B', color: '#7C4DFF', emoji: '🥉' };
  return { rank: 'C', color: '#B0BEC5', emoji: '🏅' };
};

// --- 割引率計算関数 ---
function getDiscountRate(newPrice, usedPrice) {
  if (!newPrice || !usedPrice) return null;
  const rate = Math.round((1 - usedPrice / newPrice) * 100);
  return rate > 0 ? rate : null;
}

export default function ClubRecommendations() {
  const [category, setCategory] = useState('driver');
  const [bounceOffset, setBounceOffset] = useState(0);
  const [swipeIndex, setSwipeIndex] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalClub, setModalClub] = useState(null);
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [feedbackRating, setFeedbackRating] = useState(0);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackSent, setFeedbackSent] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('lg'));
  const navigate = useNavigate();

  const categories = [
    { value: 'driver', label: 'ドライバー' },
    { value: 'wood', label: 'ウッド' },
    { value: 'iron', label: 'アイアン' },
    { value: 'wedge', label: 'ウェッジ' },
    { value: 'putter', label: 'パター' }
  ];

  // categoryIndexとswipeIndexを同期
  const categoryIndex = categories.findIndex(cat => cat.value === category);
  React.useEffect(() => {
    setSwipeIndex(categoryIndex);
  }, [categoryIndex]);

  const handleSwipeIndexChange = (index) => {
    setCategory(categories[index].value);
    setBounceOffset(0); // スワイプ完了時はバウンド解除
  };

  // 端で逆方向にスワイプした時だけバウンド、indexは固定
  const handleSwitching = (index, type) => {
    if (type === 'move') {
      if (categoryIndex === 0 && index < 0) {
        return; // ドライバータブで左スワイプを無効化
      } else if (categoryIndex === categories.length - 1 && index > categories.length - 1) {
        return; // パタータブで右スワイプを無効化
      } else {
        setBounceOffset(0);
        setSwipeIndex(index);
      }
    }
  };

  // スワイプ終了時にバウンド解除
  const handleTransitionEnd = () => {
    setBounceOffset(0);
  };

  // ブランドロゴ取得（なければGolfCourseIcon）
  const getBrandLogo = (maker) => {
    try {
      const base = `/brand-logos/${maker.toLowerCase()}`;
      const exts = ['.svg', '.png', '.jpg', '.webp'];
      for (const ext of exts) {
        const img = new window.Image();
        img.src = base + ext;
        if (img.complete) return (
          <Avatar src={img.src} alt={maker} sx={{ width: 88, height: 88, bgcolor: '#fff', border: '3.5px solid #fff', p: 1 }} imgProps={{ style: { objectFit: 'contain', width: '80%', height: '80%' } }} />
        );
      }
    } catch (e) {}
    return (
      <Avatar sx={{ width: 88, height: 88, bgcolor: '#fff', border: '3.5px solid #fff', p: 1 }}>
        <GolfCourseIcon sx={{ color: '#1976D2', fontSize: 56 }} />
      </Avatar>
    );
  };

  const handleOpenFeedback = () => {
    ReactGA.event({ 
      category: 'Feedback', 
      action: 'Open', 
      label: 'open-feedback-modal',
      value: 1
    });
    setFeedbackOpen(true);
    setFeedbackSent(false);
    setFeedbackRating(0);
    setFeedbackComment('');
  };
  const handleCloseFeedback = () => setFeedbackOpen(false);
  const handleSendFeedback = () => {
    // GoogleフォームにPOST
    const GOOGLE_FORM_ACTION_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdUmfkWKusTkvz4qUGexP04HAl8mRSCD0dUYQ_B9ZW8JvWaMg/formResponse";
    const ENTRY_RATING = "entry.945144138";   // 評価
    const ENTRY_COMMENT = "entry.259237576";  // コメント
    fetch(GOOGLE_FORM_ACTION_URL, {
      method: "POST",
      mode: "no-cors",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        [ENTRY_RATING]: feedbackRating,
        [ENTRY_COMMENT]: feedbackComment,
      }),
    });
    // Googleアナリティクスイベント送信
    ReactGA.event({ 
      category: 'Feedback', 
      action: 'Send', 
      label: 'recommend-feedback',
      value: feedbackRating
    });
    setFeedbackSent(true);
    setTimeout(() => {
      setFeedbackOpen(false);
    }, 1800);
  };

  const handleViewRecommend = () => {
    ReactGA.event({ 
      category: 'Recommend', 
      action: 'View', 
      label: 'view-recommend',
      value: 1
    });
  };

  // カテゴリ切り替え
  const handleCategoryChange = (newCategory) => {
    ReactGA.event({ 
      category: 'Recommend', 
      action: 'Category', 
      label: newCategory,
      value: 1
    });
    setCategory(newCategory);
  };

  // 商品詳細表示
  const handleViewDetail = (club) => {
    ReactGA.event({ 
      category: 'Recommend', 
      action: 'ViewDetail', 
      label: `${club.brand}-${club.name}`,
      value: 1
    });
    setModalClub(club);
    setModalOpen(true);
  };

  // 外部リンククリック
  const handleExternalLink = (type, club) => {
    ReactGA.event({ 
      category: 'Recommend', 
      action: 'ExternalLink', 
      label: `${type}-${club.brand}-${club.name}`,
      value: 1
    });
  };

  return (
    <>
      <Box sx={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', pt: { xs: '56px', md: 0 }, overflowX: 'hidden' }}>
        {/* カテゴリタブ */}
        <Box sx={{ 
          borderBottom: 1, 
          borderColor: 'divider', 
          mb: 0,
          position: { xs: 'sticky', md: 'absolute' },
          top: 0,
          left: 0,
          right: 0,
          zIndex: 1200,
          background: 'white',
          width: '100%',
          overflowX: 'hidden',
          touchAction: 'none'
        }}>
          <Tabs
            value={category}
            onChange={(e, v) => setCategory(v)}
            variant={isMobile ? "fullWidth" : "scrollable"}
            scrollButtons="auto"
            sx={{
              minHeight: 50,
              height: 50,
              display: 'flex',
              justifyContent: isMobile ? 'space-between' : 'flex-start',
              '& .MuiTabs-flexContainer': {
                display: 'flex',
                justifyContent: isMobile ? 'space-between' : 'flex-start',
              },
              '& .MuiTab-root': {
                fontWeight: 700,
                fontSize: { xs: 14, sm: 16, md: 18 },
                minWidth: isMobile ? 0 : 120,
                maxWidth: isMobile ? 'none' : 160,
                height: 50,
                minHeight: 50,
                px: { xs: 0, sm: 2, md: 4 },
                color: '#444',
                letterSpacing: 1,
                whiteSpace: 'nowrap',
                flex: isMobile ? 1 : 'none',
                '&.Mui-selected': { color: '#111' }
              },
              '& .MuiTabs-indicator': {
                backgroundColor: '#007AFF',
                borderRadius: 4,
                height: 3,
                marginTop: '2px',
              }
            }}
          >
            {categories.map((cat) => (
              <Tab 
                key={cat.value} 
                label={cat.label} 
                value={cat.value}
                sx={{
                  flex: isMobile ? 1 : 'none',
                  maxWidth: isMobile ? 'none' : 160,
                  minWidth: isMobile ? 0 : 120,
                  whiteSpace: 'nowrap',
                  px: { xs: 0, sm: 2, md: 4 },
                }}
              />
            ))}
          </Tabs>
        </Box>

        {/* 商品一覧＋モーダル・FABなども分岐内に移動 */}
        {isMobile ? (
          <>
            <SwipeableViews
              index={swipeIndex}
              onChangeIndex={handleSwipeIndexChange}
              onSwitching={handleSwitching}
              resistance
              style={{ flex: 1 }}
              containerStyle={{ height: '100%' }}
              slideStyle={{ minHeight: '100%', transform: bounceOffset !== 0 ? `translateX(${bounceOffset}px)` : undefined, transition: bounceOffset !== 0 ? 'transform 0.38s cubic-bezier(0.23, 1, 0.32, 1)' : undefined }}
              onTransitionEnd={handleTransitionEnd}
              springConfig={{ duration: '0.55s', easeFunction: 'cubic-bezier(0.23, 1, 0.32, 1)', delay: '0s' }}
            >
              {categories.map((cat) => (
                <Box key={cat.value} sx={{ flex: 1, overflowY: 'auto', px: 2, pb: 2, pt: 1 }}>
                  {clubData[cat.value].sort((a, b) => b.match - a.match).map((club) => (
                    <motion.div
                      key={club.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Paper
                        elevation={0}
                        sx={{
                          ...appleCardStyle,
                          p: { xs: 2, md: 3 },
                          mb: { xs: 2, md: 3 },
                          borderRadius: { xs: 4, md: 6 },
                          boxShadow: {
                            xs: '0 4px 24px 0 rgba(25,118,210,0.10), 0 1.5px 8px 0 rgba(0,0,0,0.04)',
                            md: '0 8px 32px 0 rgba(25,118,210,0.13), 0 2px 12px 0 rgba(0,0,0,0.06)'
                          },
                          maxWidth: { xs: '98vw', md: 720 },
                          mx: 'auto',
                          position: 'relative',
                          transition: 'box-shadow 0.18s, transform 0.18s',
                          '&:hover': {
                            boxShadow: '0 16px 48px 0 rgba(25,118,210,0.18), 0 4px 24px 0 rgba(0,0,0,0.10)',
                            transform: { md: 'translateY(-2px) scale(1.012)' }
                          },
                          background: 'linear-gradient(135deg, #fafdff 70%, #e9eef3 100%)',
                          border: '1.5px solid #e3e6ea',
                        }}
                      >
                        {/* マッチ度バッジ */}
                        <Box sx={{ position: 'absolute', top: 16, right: 16, zIndex: 3 }}>
                          <MatchBadge value={club.match} />
                        </Box>
                        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, alignItems: { xs: 'center', md: 'flex-start' }, gap: { xs: 2, md: 3 } }}>
                          {/* 画像＋ブランドロゴ */}
                          <Box sx={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: { md: 120 }, mb: { xs: 1, md: 0 } }}>
                            <Avatar src={club.image} alt={club.name} sx={{ width: { xs: 90, md: 110 }, height: { xs: 90, md: 110 }, borderRadius: 3, boxShadow: 2, bgcolor: '#fff' }} />
                            {/* ブランドロゴ（仮） */}
                            <Box sx={{ position: 'absolute', bottom: -12, left: '50%', transform: 'translateX(-50%)', bgcolor: '#fff', borderRadius: 2, boxShadow: 1, px: 1, py: 0.5, display: { xs: 'none', md: 'block' } }}>
                              <Typography sx={{ fontSize: 13, fontWeight: 700, color: '#1976D2' }}>{club.maker}</Typography>
                            </Box>
                          </Box>
                          {/* メイン情報 */}
                          <Box sx={{ flex: 1, width: '100%' }}>
                            <Typography variant="h6" sx={{ fontWeight: 800, fontSize: { xs: '1.1rem', md: '1.25rem' }, mb: 0.5, color: '#111', textAlign: { xs: 'center', md: 'left' } }}>{club.name}</Typography>
                            <Typography variant="subtitle2" color="text.secondary" sx={{ fontSize: { xs: '0.92rem', md: '1rem' }, mb: 1, textAlign: { xs: 'center', md: 'left' } }}>
                              {club.maker} | {club.specs}
                            </Typography>
                            {/* 詳細ボタン（スマホは中央、PCは右下） */}
                            <Box sx={{ display: { xs: 'flex', md: 'none' }, justifyContent: 'center', mb: 1 }}>
                              <Button
                                variant="contained"
                                startIcon={<InfoOutlinedIcon />}
                                sx={{
                                  bgcolor: '#222',
                                  color: '#fff',
                                  fontWeight: 700,
                                  borderRadius: 3,
                                  px: 2,
                                  minWidth: 180,
                                  maxWidth: 260,
                                  height: 36,
                                  fontSize: '0.92rem',
                                  alignSelf: 'center',
                                  boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
                                  letterSpacing: 0.5,
                                  textAlign: 'center',
                                  '&:hover': { bgcolor: '#444' }
                                }}
                                onClick={() => { handleViewDetail(club); }}
                              >
                                詳細
                              </Button>
                            </Box>
                            {/* レコメンド理由 */}
                            <Typography 
                              variant="body2" 
                              color="text.secondary" 
                              sx={{ 
                                mb: 1,
                                backgroundColor: 'rgba(0, 0, 0, 0.04)',
                                p: 1,
                                borderRadius: 2,
                                fontSize: { xs: '0.90rem', md: '0.98rem' },
                                textAlign: { xs: 'center', md: 'left' },
                                maxWidth: '100%',
                                wordBreak: 'break-word',
                                overflowWrap: 'break-word',
                                mx: 'auto',
                                display: 'block',
                                fontWeight: 500
                              }}
                            >
                              {club.matchReason}
                            </Typography>
                            {/* 価格表示 */}
                            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', justifyContent: { xs: 'center', md: 'flex-start' }, mb: 1 }}>
                              <Box>
                                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.80rem' }}>
                                  新品
                                </Typography>
                                <Typography variant="h6" color="primary" sx={{ fontWeight: 700, fontSize: { xs: '1.05rem', md: '1.12rem' } }}>
                                  {club.price_label}
                                </Typography>
                              </Box>
                              <Box>
                                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.80rem' }}>
                                  中古
                                </Typography>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <Typography variant="h6" color="success.main" sx={{ fontWeight: 700, fontSize: { xs: '1.05rem', md: '1.12rem' } }}>
                                    ¥{club.used_price.toLocaleString()}～
                                  </Typography>
                                  {getDiscountRate(club.price, club.used_price) && (
                                    <Chip
                                      label={`${getDiscountRate(club.price, club.used_price)}%OFF`}
                                      size="small"
                                      color="success"
                                      sx={{ height: 18, fontSize: '0.7rem', px: 0.5 }}
                                    />
                                  )}
                                </Box>
                              </Box>
                            </Box>
                            {/* アクションボタン */}
                            <Box sx={{
                              display: 'flex',
                              flexDirection: 'row',
                              gap: 1.5,
                              mt: 1,
                              width: '100%',
                              justifyContent: { xs: 'space-between', md: 'flex-end' },
                            }}>
                              <Button
                                variant="outlined"
                                startIcon={<StorefrontIcon />}
                                href={club.rakutenUrl}
                                target="_blank"
                                onClick={() => handleExternalLink('rakuten', club)}
                                sx={{
                                  flex: 1,
                                  minWidth: 0,
                                  maxWidth: { xs: 'none', md: 120 },
                                  borderColor: '#007AFF',
                                  color: '#007AFF',
                                  height: 36,
                                  fontSize: '0.85rem',
                                  fontWeight: 700,
                                  borderRadius: 2,
                                  px: 1,
                                  '&:hover': {
                                    borderColor: '#0066CC',
                                    bgcolor: '#F1F3F4',
                                    color: '#0066CC',
                                    transform: 'translateY(-1px)'
                                  }
                                }}
                              >
                                楽天
                              </Button>
                              <Button
                                variant="outlined"
                                startIcon={<StorefrontIcon />}
                                href={club.yahooUrl}
                                target="_blank"
                                onClick={() => handleExternalLink('yahoo', club)}
                                sx={{
                                  flex: 1,
                                  minWidth: 0,
                                  maxWidth: { xs: 'none', md: 120 },
                                  borderColor: '#007AFF',
                                  color: '#007AFF',
                                  height: 36,
                                  fontSize: '0.85rem',
                                  fontWeight: 700,
                                  borderRadius: 2,
                                  px: 1,
                                  '&:hover': {
                                    borderColor: '#0066CC',
                                    bgcolor: '#F1F3F4',
                                    color: '#0066CC',
                                    transform: 'translateY(-1px)'
                                  }
                                }}
                              >
                                Yahoo!
                              </Button>
                              <Button
                                variant="outlined"
                                startIcon={<SearchIcon />}
                                href={club.usedUrl}
                                target="_blank"
                                onClick={() => handleExternalLink('used', club)}
                                sx={{
                                  flex: 1,
                                  minWidth: 0,
                                  maxWidth: { xs: 'none', md: 120 },
                                  borderColor: '#4CAF50',
                                  color: '#4CAF50',
                                  height: 36,
                                  fontSize: '0.85rem',
                                  fontWeight: 700,
                                  borderRadius: 2,
                                  px: 1,
                                  '&:hover': {
                                    borderColor: '#388E3C',
                                    bgcolor: '#E8F5E9',
                                    transform: 'translateY(-1px)'
                                  }
                                }}
                              >
                                中古
                              </Button>
                              {/* PCのみ詳細ボタンを右下に */}
                              <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', ml: 2 }}>
                                <Button
                                  variant="contained"
                                  startIcon={<InfoOutlinedIcon />}
                                  sx={{
                                    bgcolor: '#222',
                                    color: '#fff',
                                    fontWeight: 700,
                                    borderRadius: 3,
                                    px: 2,
                                    minWidth: 120,
                                    maxWidth: 180,
                                    height: 36,
                                    fontSize: '0.92rem',
                                    alignSelf: 'center',
                                    boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
                                    letterSpacing: 0.5,
                                    textAlign: 'center',
                                    '&:hover': { bgcolor: '#444' }
                                  }}
                                  onClick={() => { handleViewDetail(club); }}
                                >
                                  詳細
                                </Button>
                              </Box>
                            </Box>
                          </Box>
                        </Box>
                      </Paper>
                    </motion.div>
                  ))}
                </Box>
              ))}
            </SwipeableViews>
            {/* モバイル用のモーダルとFAB */}
            <Dialog open={modalOpen} onClose={() => setModalOpen(false)} fullWidth maxWidth="xs">
              <DialogTitle sx={{ fontWeight: 800, color: '#1976D2', fontSize: 20 }}>{modalClub?.name}</DialogTitle>
              <DialogContent>
                <Box sx={{ mb: 2 }}>
                  <Typography sx={{ fontWeight: 700, fontSize: 16, mb: 1 }}>スペック</Typography>
                  <Typography sx={{ fontSize: 15, color: '#444', mb: 1 }}>{modalClub?.specs}</Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: 16, mb: 1 }}>レビュー</Typography>
                  <Typography sx={{ fontSize: 15, color: '#444', mb: 1 }}>{modalClub?.matchReason}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    <Rating value={modalClub?.rating} precision={0.1} readOnly size="small" />
                    <Typography sx={{ fontSize: 14, color: '#888', fontWeight: 600 }}>({modalClub?.reviews})</Typography>
                  </Box>
                </Box>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setModalOpen(false)} color="primary" variant="contained">閉じる</Button>
              </DialogActions>
            </Dialog>
            <Fab color="primary" variant="circular" size="medium" onClick={() => {
              navigate('/diagnosis', { state: { step: 0, answers: [] } });
            }} sx={{ position: 'fixed', bottom: 84, right: 20, zIndex: 1200, boxShadow: 2, bgcolor: '#007AFF', color: '#fff', '&:hover': { bgcolor: '#0066CC' } }}>
              <ReplayIcon />
            </Fab>
            <Box sx={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1200 }}>
              <Fab color="info" variant="extended" onClick={handleOpenFeedback} sx={{ fontWeight: 700, px: 2, boxShadow: 3, bgcolor: '#007AFF', color: '#fff', '&:hover': { bgcolor: '#0066CC' } }}>
                <RateReviewIcon sx={{ mr: 1 }} />
                フィードバック
              </Fab>
            </Box>
            <Dialog open={feedbackOpen} onClose={handleCloseFeedback} maxWidth="xs" fullWidth>
              <DialogTitle sx={{ fontWeight: 700, color: '#1976D2', fontSize: 20, textAlign: 'center' }}>
                このレコメンドはいかがでしたか？
              </DialogTitle>
              <DialogContent>
                {feedbackSent ? (
                  <Box sx={{ py: 4, textAlign: 'center', fontWeight: 700, fontSize: 18, color: '#1976D2' }}>
                    ありがとうございました！
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, py: 1 }}>
                    <Rating
                      name="feedback-rating"
                      value={feedbackRating}
                      onChange={(_, newValue) => setFeedbackRating(newValue)}
                      size="large"
                    />
                    <TextField
                      label="ご意見・ご感想（任意）"
                      multiline
                      rows={3}
                      value={feedbackComment}
                      onChange={e => setFeedbackComment(e.target.value)}
                      fullWidth
                    />
                  </Box>
                )}
              </DialogContent>
              <DialogActions sx={{ justifyContent: 'center', pb: 2 }}>
                {!feedbackSent && (
                  <Button
                    variant="contained"
                    onClick={handleSendFeedback}
                    sx={{ borderRadius: 4, width: 160, fontWeight: 700 }}
                    disabled={!feedbackRating}
                  >
                    送信
                  </Button>
                )}
                <Button onClick={handleCloseFeedback} color="inherit" sx={{ ml: 1 }}>
                  閉じる
                </Button>
              </DialogActions>
            </Dialog>
          </>
        ) : (
          <>
            <Box sx={{ flex: 1, overflowY: 'auto', px: 2, pb: 2, pt: 1, paddingTop: '56px' }}>
              {clubData[category].sort((a, b) => b.match - a.match).map((club) => (
                <motion.div
                  key={club.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Paper
                    elevation={0}
                    sx={{
                      ...appleCardStyle,
                      p: { xs: 2, md: 3 },
                      mb: { xs: 2, md: 3 },
                      borderRadius: { xs: 4, md: 6 },
                      boxShadow: {
                        xs: '0 4px 24px 0 rgba(25,118,210,0.10), 0 1.5px 8px 0 rgba(0,0,0,0.04)',
                        md: '0 8px 32px 0 rgba(25,118,210,0.13), 0 2px 12px 0 rgba(0,0,0,0.06)'
                      },
                      maxWidth: { xs: '98vw', md: 720 },
                      mx: 'auto',
                      position: 'relative',
                      transition: 'box-shadow 0.18s, transform 0.18s',
                      '&:hover': {
                        boxShadow: '0 16px 48px 0 rgba(25,118,210,0.18), 0 4px 24px 0 rgba(0,0,0,0.10)',
                        transform: { md: 'translateY(-2px) scale(1.012)' }
                      },
                      background: 'linear-gradient(135deg, #fafdff 70%, #e9eef3 100%)',
                      border: '1.5px solid #e3e6ea',
                    }}
                  >
                    {/* マッチ度バッジ */}
                    <Box sx={{ position: 'absolute', top: 16, right: 16, zIndex: 3 }}>
                      <MatchBadge value={club.match} />
                    </Box>
                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, alignItems: { xs: 'center', md: 'flex-start' }, gap: { xs: 2, md: 3 } }}>
                      {/* 画像＋ブランドロゴ */}
                      <Box sx={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: { md: 120 }, mb: { xs: 1, md: 0 } }}>
                        <Avatar src={club.image} alt={club.name} sx={{ width: { xs: 90, md: 110 }, height: { xs: 90, md: 110 }, borderRadius: 3, boxShadow: 2, bgcolor: '#fff' }} />
                        {/* ブランドロゴ（仮） */}
                        <Box sx={{ position: 'absolute', bottom: -12, left: '50%', transform: 'translateX(-50%)', bgcolor: '#fff', borderRadius: 2, boxShadow: 1, px: 1, py: 0.5, display: { xs: 'none', md: 'block' } }}>
                          <Typography sx={{ fontSize: 13, fontWeight: 700, color: '#1976D2' }}>{club.maker}</Typography>
                        </Box>
                      </Box>
                      {/* メイン情報 */}
                      <Box sx={{ flex: 1, width: '100%' }}>
                        <Typography variant="h6" sx={{ fontWeight: 800, fontSize: { xs: '1.1rem', md: '1.25rem' }, mb: 0.5, color: '#111', textAlign: { xs: 'center', md: 'left' } }}>{club.name}</Typography>
                        <Typography variant="subtitle2" color="text.secondary" sx={{ fontSize: { xs: '0.92rem', md: '1rem' }, mb: 1, textAlign: { xs: 'center', md: 'left' } }}>
                          {club.maker} | {club.specs}
                        </Typography>
                        {/* 詳細ボタン（スマホは中央、PCは右下） */}
                        <Box sx={{ display: { xs: 'flex', md: 'none' }, justifyContent: 'center', mb: 1 }}>
                          <Button
                            variant="contained"
                            startIcon={<InfoOutlinedIcon />}
                            sx={{
                              bgcolor: '#222',
                              color: '#fff',
                              fontWeight: 700,
                              borderRadius: 3,
                              px: 2,
                              minWidth: 180,
                              maxWidth: 260,
                              height: 36,
                              fontSize: '0.92rem',
                              alignSelf: 'center',
                              boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
                              letterSpacing: 0.5,
                              textAlign: 'center',
                              '&:hover': { bgcolor: '#444' }
                            }}
                            onClick={() => { handleViewDetail(club); }}
                          >
                            詳細
                          </Button>
                        </Box>
                        {/* レコメンド理由 */}
                        <Typography 
                          variant="body2" 
                          color="text.secondary" 
                          sx={{ 
                            mb: 1,
                            backgroundColor: 'rgba(0, 0, 0, 0.04)',
                            p: 1,
                            borderRadius: 2,
                            fontSize: { xs: '0.90rem', md: '0.98rem' },
                            textAlign: { xs: 'center', md: 'left' },
                            maxWidth: '100%',
                            wordBreak: 'break-word',
                            overflowWrap: 'break-word',
                            mx: 'auto',
                            display: 'block',
                            fontWeight: 500
                          }}
                        >
                          {club.matchReason}
                        </Typography>
                        {/* 価格表示 */}
                        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', justifyContent: { xs: 'center', md: 'flex-start' }, mb: 1 }}>
                          <Box>
                            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.80rem' }}>
                              新品
                            </Typography>
                            <Typography variant="h6" color="primary" sx={{ fontWeight: 700, fontSize: { xs: '1.05rem', md: '1.12rem' } }}>
                              {club.price_label}
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.80rem' }}>
                              中古
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                              <Typography variant="h6" color="success.main" sx={{ fontWeight: 700, fontSize: { xs: '1.05rem', md: '1.12rem' } }}>
                                ¥{club.used_price.toLocaleString()}～
                              </Typography>
                              {getDiscountRate(club.price, club.used_price) && (
                                <Chip
                                  label={`${getDiscountRate(club.price, club.used_price)}%OFF`}
                                  size="small"
                                  color="success"
                                  sx={{ height: 18, fontSize: '0.7rem', px: 0.5 }}
                                />
                              )}
                            </Box>
                          </Box>
                        </Box>
                        {/* アクションボタン */}
                        <Box sx={{
                          display: 'flex',
                          flexDirection: 'row',
                          gap: 1.5,
                          mt: 1,
                          width: '100%',
                          justifyContent: { xs: 'space-between', md: 'flex-end' },
                        }}>
                          <Button
                            variant="outlined"
                            startIcon={<StorefrontIcon />}
                            href={club.rakutenUrl}
                            target="_blank"
                            onClick={() => handleExternalLink('rakuten', club)}
                            sx={{
                              flex: 1,
                              minWidth: 0,
                              maxWidth: { xs: 'none', md: 120 },
                              borderColor: '#007AFF',
                              color: '#007AFF',
                              height: 36,
                              fontSize: '0.85rem',
                              fontWeight: 700,
                              borderRadius: 2,
                              px: 1,
                              '&:hover': {
                                borderColor: '#0066CC',
                                bgcolor: '#F1F3F4',
                                color: '#0066CC',
                                transform: 'translateY(-1px)'
                              }
                            }}
                          >
                            楽天
                          </Button>
                          <Button
                            variant="outlined"
                            startIcon={<StorefrontIcon />}
                            href={club.yahooUrl}
                            target="_blank"
                            onClick={() => handleExternalLink('yahoo', club)}
                            sx={{
                              flex: 1,
                              minWidth: 0,
                              maxWidth: { xs: 'none', md: 120 },
                              borderColor: '#007AFF',
                              color: '#007AFF',
                              height: 36,
                              fontSize: '0.85rem',
                              fontWeight: 700,
                              borderRadius: 2,
                              px: 1,
                              '&:hover': {
                                borderColor: '#0066CC',
                                bgcolor: '#F1F3F4',
                                color: '#0066CC',
                                transform: 'translateY(-1px)'
                              }
                            }}
                          >
                            Yahoo!
                          </Button>
                          <Button
                            variant="outlined"
                            startIcon={<SearchIcon />}
                            href={club.usedUrl}
                            target="_blank"
                            onClick={() => handleExternalLink('used', club)}
                            sx={{
                              flex: 1,
                              minWidth: 0,
                              maxWidth: { xs: 'none', md: 120 },
                              borderColor: '#4CAF50',
                              color: '#4CAF50',
                              height: 36,
                              fontSize: '0.85rem',
                              fontWeight: 700,
                              borderRadius: 2,
                              px: 1,
                              '&:hover': {
                                borderColor: '#388E3C',
                                bgcolor: '#E8F5E9',
                                transform: 'translateY(-1px)'
                              }
                            }}
                          >
                            中古
                          </Button>
                          {/* PCのみ詳細ボタンを右下に */}
                          <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', ml: 2 }}>
                            <Button
                              variant="contained"
                              startIcon={<InfoOutlinedIcon />}
                              sx={{
                                bgcolor: '#222',
                                color: '#fff',
                                fontWeight: 700,
                                borderRadius: 3,
                                px: 2,
                                minWidth: 120,
                                maxWidth: 180,
                                height: 36,
                                fontSize: '0.92rem',
                                alignSelf: 'center',
                                boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
                                letterSpacing: 0.5,
                                textAlign: 'center',
                                '&:hover': { bgcolor: '#444' }
                              }}
                              onClick={() => { handleViewDetail(club); }}
                            >
                              詳細
                            </Button>
                          </Box>
                        </Box>
                      </Box>
                    </Box>
                  </Paper>
                </motion.div>
              ))}
            </Box>
            {/* PC用のモーダル */}
            <Dialog open={modalOpen} onClose={() => setModalOpen(false)} fullWidth maxWidth="xs">
              <DialogTitle sx={{ fontWeight: 800, color: '#1976D2', fontSize: 20 }}>{modalClub?.name}</DialogTitle>
              <DialogContent>
                <Box sx={{ mb: 2 }}>
                  <Typography sx={{ fontWeight: 700, fontSize: 16, mb: 1 }}>スペック</Typography>
                  <Typography sx={{ fontSize: 15, color: '#444', mb: 1 }}>{modalClub?.specs}</Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: 16, mb: 1 }}>レビュー</Typography>
                  <Typography sx={{ fontSize: 15, color: '#444', mb: 1 }}>{modalClub?.matchReason}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    <Rating value={modalClub?.rating} precision={0.1} readOnly size="small" />
                    <Typography sx={{ fontSize: 14, color: '#888', fontWeight: 600 }}>({modalClub?.reviews})</Typography>
                  </Box>
                </Box>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setModalOpen(false)} color="primary" variant="contained">閉じる</Button>
              </DialogActions>
            </Dialog>
            <Box sx={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1200 }}>
              <Fab color="info" variant="extended" onClick={handleOpenFeedback} sx={{ fontWeight: 700, px: 2, boxShadow: 3, bgcolor: '#007AFF', color: '#fff', '&:hover': { bgcolor: '#0066CC' } }}>
                <RateReviewIcon sx={{ mr: 1 }} />
                フィードバック
              </Fab>
            </Box>
            <Dialog open={feedbackOpen} onClose={handleCloseFeedback} maxWidth="xs" fullWidth>
              <DialogTitle sx={{ fontWeight: 700, color: '#1976D2', fontSize: 20, textAlign: 'center' }}>
                このレコメンドはいかがでしたか？
              </DialogTitle>
              <DialogContent>
                {feedbackSent ? (
                  <Box sx={{ py: 4, textAlign: 'center', fontWeight: 700, fontSize: 18, color: '#1976D2' }}>
                    ありがとうございました！
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, py: 1 }}>
                    <Rating
                      name="feedback-rating"
                      value={feedbackRating}
                      onChange={(_, newValue) => setFeedbackRating(newValue)}
                      size="large"
                    />
                    <TextField
                      label="ご意見・ご感想（任意）"
                      multiline
                      rows={3}
                      value={feedbackComment}
                      onChange={e => setFeedbackComment(e.target.value)}
                      fullWidth
                    />
                  </Box>
                )}
              </DialogContent>
              <DialogActions sx={{ justifyContent: 'center', pb: 2 }}>
                {!feedbackSent && (
                  <Button
                    variant="contained"
                    onClick={handleSendFeedback}
                    sx={{ borderRadius: 4, width: 160, fontWeight: 700 }}
                    disabled={!feedbackRating}
                  >
                    送信
                  </Button>
                )}
                <Button onClick={handleCloseFeedback} color="inherit" sx={{ ml: 1 }}>
                  閉じる
                </Button>
              </DialogActions>
            </Dialog>
          </>
        )}
      </Box>
    </>
  );
} 