import React, { useState } from 'react';
import { Box, Paper, Typography, Button, Avatar, Tabs, Tab, Chip, Rating, IconButton } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import SearchIcon from '@mui/icons-material/Search';
import StorefrontIcon from '@mui/icons-material/Storefront';
import { motion } from 'framer-motion';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';

// カテゴリごとのダミーデータ
const clubData = {
  driver: [
    {
      id: 1,
      name: 'TaylorMade Stealth 2',
      maker: 'TaylorMade',
      price: 59800,
      match: 92,
      matchReason: 'スライス修正に最適な設計',
      specs: 'ロフト: 9度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-01-15',
      image: '/sample/driver.png',
      rating: 4.8,
      reviews: 128,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 2,
      name: 'Callaway Paradym',
      maker: 'Callaway',
      price: 62800,
      match: 90,
      matchReason: '高弾道で飛距離が伸びる',
      specs: 'ロフト: 10.5度 / シャフト: グラファイト / フレックス: S',
      releaseDate: '2023-02-01',
      image: '/sample/driver.png',
      rating: 4.7,
      reviews: 95,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 3,
      name: 'Titleist TSR3',
      maker: 'Titleist',
      price: 64800,
      match: 88,
      matchReason: '方向性と飛距離のバランスが良い',
      specs: 'ロフト: 9度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-03-15',
      image: '/sample/driver.png',
      rating: 4.9,
      reviews: 156,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 4,
      name: 'PING G430',
      maker: 'PING',
      price: 57800,
      match: 87,
      matchReason: '安定した弾道でスコアが伸びる',
      specs: 'ロフト: 10.5度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-04-01',
      image: '/sample/driver.png',
      rating: 4.6,
      reviews: 82,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 5,
      name: 'Mizuno ST-X',
      maker: 'Mizuno',
      price: 54800,
      match: 86,
      matchReason: '打感が良く、コントロール性が高い',
      specs: 'ロフト: 9度 / シャフト: グラファイト / フレックス: S',
      releaseDate: '2023-05-15',
      image: '/sample/driver.png',
      rating: 4.8,
      reviews: 112,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 6,
      name: 'Srixon ZX7',
      maker: 'Srixon',
      price: 52800,
      match: 85,
      matchReason: '低スピンで飛距離が伸びる',
      specs: 'ロフト: 9度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-06-01',
      image: '/sample/driver.png',
      rating: 4.7,
      reviews: 78,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    }
  ],
  wood: [
    {
      id: 1,
      name: 'Callaway Paradym 3W',
      maker: 'Callaway',
      price: 39800,
      match: 90,
      matchReason: '高弾道で着地が柔らかい',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: S',
      releaseDate: '2023-02-01',
      image: '/sample/wood.png',
      rating: 4.7,
      reviews: 95,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 2,
      name: 'TaylorMade Stealth 2 3W',
      maker: 'TaylorMade',
      price: 42800,
      match: 89,
      matchReason: '方向性が良く、飛距離も出る',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-03-01',
      image: '/sample/wood.png',
      rating: 4.8,
      reviews: 88,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 3,
      name: 'Titleist TSR2 3W',
      maker: 'Titleist',
      price: 41800,
      match: 88,
      matchReason: '打感が良く、コントロール性が高い',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: S',
      releaseDate: '2023-04-01',
      image: '/sample/wood.png',
      rating: 4.9,
      reviews: 92,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 4,
      name: 'PING G430 3W',
      maker: 'PING',
      price: 39800,
      match: 87,
      matchReason: '安定した弾道でスコアが伸びる',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-05-01',
      image: '/sample/wood.png',
      rating: 4.7,
      reviews: 76,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 5,
      name: 'Mizuno ST-X 3W',
      maker: 'Mizuno',
      price: 37800,
      match: 86,
      matchReason: '打感が良く、方向性が安定',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: S',
      releaseDate: '2023-06-01',
      image: '/sample/wood.png',
      rating: 4.8,
      reviews: 82,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 6,
      name: 'Srixon ZX 3W',
      maker: 'Srixon',
      price: 36800,
      match: 85,
      matchReason: '低スピンで飛距離が伸びる',
      specs: 'ロフト: 15度 / シャフト: グラファイト / フレックス: R',
      releaseDate: '2023-07-01',
      image: '/sample/wood.png',
      rating: 4.6,
      reviews: 68,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    }
  ],
  iron: [
    {
      id: 1,
      name: 'Titleist T200',
      maker: 'Titleist',
      price: 128000,
      match: 88,
      matchReason: '方向性と飛距離のバランスが良い',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: R',
      releaseDate: '2023-03-15',
      image: '/sample/iron.png',
      rating: 4.9,
      reviews: 156,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 2,
      name: 'Callaway Apex Pro',
      maker: 'Callaway',
      price: 138000,
      match: 87,
      matchReason: '打感が良く、コントロール性が高い',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: S',
      releaseDate: '2023-04-01',
      image: '/sample/iron.png',
      rating: 4.8,
      reviews: 142,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 3,
      name: 'TaylorMade P790',
      maker: 'TaylorMade',
      price: 148000,
      match: 86,
      matchReason: '高弾道で飛距離が伸びる',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: R',
      releaseDate: '2023-05-01',
      image: '/sample/iron.png',
      rating: 4.9,
      reviews: 168,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 4,
      name: 'PING i525',
      maker: 'PING',
      price: 118000,
      match: 85,
      matchReason: '安定した弾道でスコアが伸びる',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: S',
      releaseDate: '2023-06-01',
      image: '/sample/iron.png',
      rating: 4.7,
      reviews: 132,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 5,
      name: 'Mizuno JPX923',
      maker: 'Mizuno',
      price: 128000,
      match: 84,
      matchReason: '打感が最高で、方向性も安定',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: R',
      releaseDate: '2023-07-01',
      image: '/sample/iron.png',
      rating: 4.8,
      reviews: 148,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 6,
      name: 'Srixon ZX7',
      maker: 'Srixon',
      price: 118000,
      match: 83,
      matchReason: '低スピンで飛距離が伸びる',
      specs: 'セット構成: 4-PW / シャフト: スチール / フレックス: S',
      releaseDate: '2023-08-01',
      image: '/sample/iron.png',
      rating: 4.7,
      reviews: 126,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    }
  ],
  wedge: [
    {
      id: 1,
      name: 'Vokey SM9',
      maker: 'Titleist',
      price: 29800,
      match: 85,
      matchReason: 'スピン量が多く、コントロール性が高い',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-04-01',
      image: '/sample/wedge.png',
      rating: 4.8,
      reviews: 112,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 2,
      name: 'Callaway Jaws Raw',
      maker: 'Callaway',
      price: 28800,
      match: 84,
      matchReason: 'スピン量が多く、方向性も安定',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-05-01',
      image: '/sample/wedge.png',
      rating: 4.7,
      reviews: 98,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 3,
      name: 'TaylorMade MG3',
      maker: 'TaylorMade',
      price: 27800,
      match: 83,
      matchReason: '打感が良く、コントロール性が高い',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-06-01',
      image: '/sample/wedge.png',
      rating: 4.8,
      reviews: 108,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 4,
      name: 'PING Glide 4.0',
      maker: 'PING',
      price: 26800,
      match: 82,
      matchReason: '安定した弾道でスコアが伸びる',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-07-01',
      image: '/sample/wedge.png',
      rating: 4.7,
      reviews: 92,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 5,
      name: 'Mizuno T22',
      maker: 'Mizuno',
      price: 25800,
      match: 81,
      matchReason: '打感が最高で、方向性も安定',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-08-01',
      image: '/sample/wedge.png',
      rating: 4.8,
      reviews: 102,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 6,
      name: 'Srixon ZX',
      maker: 'Srixon',
      price: 24800,
      match: 80,
      matchReason: '低スピンで飛距離が伸びる',
      specs: 'ロフト: 56度 / バウンス: 10度 / シャフト: スチール',
      releaseDate: '2023-09-01',
      image: '/sample/wedge.png',
      rating: 4.6,
      reviews: 88,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    }
  ],
  putter: [
    {
      id: 1,
      name: 'Scotty Cameron Super Select',
      maker: 'Titleist',
      price: 49800,
      match: 87,
      matchReason: '安定したストロークが可能',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-05-15',
      image: '/sample/putter.png',
      rating: 4.9,
      reviews: 89,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 2,
      name: 'Odyssey White Hot OG',
      maker: 'Callaway',
      price: 45800,
      match: 86,
      matchReason: '打感が良く、方向性も安定',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-06-01',
      image: '/sample/putter.png',
      rating: 4.8,
      reviews: 82,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 3,
      name: 'TaylorMade Spider GT',
      maker: 'TaylorMade',
      price: 47800,
      match: 85,
      matchReason: '安定したストロークが可能',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-07-01',
      image: '/sample/putter.png',
      rating: 4.9,
      reviews: 92,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 4,
      name: 'PING PLD',
      maker: 'PING',
      price: 46800,
      match: 84,
      matchReason: '打感が良く、コントロール性が高い',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-08-01',
      image: '/sample/putter.png',
      rating: 4.7,
      reviews: 78,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 5,
      name: 'Mizuno M-Craft',
      maker: 'Mizuno',
      price: 45800,
      match: 83,
      matchReason: '打感が最高で、方向性も安定',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-09-01',
      image: '/sample/putter.png',
      rating: 4.8,
      reviews: 88,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
    },
    {
      id: 6,
      name: 'Srixon Z-Star',
      maker: 'Srixon',
      price: 44800,
      match: 82,
      matchReason: '安定したストロークが可能',
      specs: 'ヘッドタイプ: マレット / 長さ: 34インチ / 重量: 350g',
      releaseDate: '2023-10-01',
      image: '/sample/putter.png',
      rating: 4.7,
      reviews: 76,
      rakutenUrl: '#',
      yahooUrl: '#',
      usedUrl: '#'
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

export default function ClubRecommendations() {
  const [category, setCategory] = useState('driver');
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('lg'));

  const handleCategoryChange = (event, newValue) => {
    setCategory(newValue);
  };

  return (
    <Box sx={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* カテゴリタブ */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs
          value={category}
          onChange={handleCategoryChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            '& .MuiTab-root': {
              fontWeight: 600,
              fontSize: 15,
              minWidth: 100,
              color: '#666',
              '&.Mui-selected': { color: '#111' }
            },
            '& .MuiTabs-indicator': {
              height: 3,
              background: '#111'
            }
          }}
        >
          <Tab label="ドライバー" value="driver" />
          <Tab label="ウッド" value="wood" />
          <Tab label="アイアン" value="iron" />
          <Tab label="ウェッジ" value="wedge" />
          <Tab label="パター" value="putter" />
        </Tabs>
      </Box>

      {/* 商品一覧 */}
      <Box sx={{ flex: 1, overflowY: 'auto', px: 2, pb: 2 }}>
        {clubData[category].map((club) => (
          <motion.div
            key={club.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Paper
              elevation={0}
              sx={{
                ...glassmorphismStyle,
                p: 2,
                mb: 3,
                transition: 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)',
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.35)',
                  transform: 'translateY(-5px)',
                  boxShadow: '0 16px 40px 0 rgba(0,0,0,0.09), 0 2px 12px 0 rgba(0,0,0,0.04)',
                  transition: 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)'
                }
              }}
            >
              {isMobile ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                  {/* 画像上 */}
                  <Avatar
                    src={club.image}
                    alt={club.name}
                    sx={{ width: 120, height: 120, borderRadius: 2, mb: 1 }}
                  />
                  {/* 情報下 */}
                  <Box sx={{ width: '100%' }}>
                    {/* ヘッダー部分 */}
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1.5 }}>
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.5 }}>{club.name}</Typography>
                        <Typography variant="subtitle2" color="text.secondary">
                          {club.maker} | {club.specs}
                        </Typography>
                      </Box>
                      <Chip
                        label={`マッチ度 ${club.match}%`}
                        color="primary"
                        size="small"
                        sx={{ fontWeight: 600 }}
                      />
                    </Box>
                    {/* マッチ理由 */}
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ 
                        mb: 1.5,
                        backgroundColor: 'rgba(0, 0, 0, 0.03)',
                        p: 1,
                        borderRadius: 1,
                        fontSize: '0.875rem'
                      }}
                    >
                      {club.matchReason}
                    </Typography>
                    {/* 価格表示＋詳細ボタン */}
                    <Box sx={{ 
                      mb: 2,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'flex-start',
                      gap: 1.5
                    }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                            新品価格
                          </Typography>
                          <Typography variant="h6" color="primary" sx={{ fontWeight: 700 }}>
                            ¥{club.price.toLocaleString()}
                          </Typography>
                        </Box>
                        <Box>
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                            中古価格
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="h6" color="success.main" sx={{ fontWeight: 700 }}>
                              ¥{(club.price * 0.6).toLocaleString()}
                            </Typography>
                            <Chip
                              label="40%OFF"
                              size="small"
                              color="success"
                              sx={{ height: 20, fontSize: '0.75rem' }}
                            />
                          </Box>
                        </Box>
                      </Box>
                      <Button
                        variant="contained"
                        startIcon={<InfoOutlinedIcon />}
                        sx={{
                          bgcolor: '#111',
                          color: '#fff',
                          fontWeight: 600,
                          borderRadius: 2,
                          px: 3,
                          height: 38,
                          fontSize: '0.92rem',
                          mt: 1,
                          alignSelf: 'stretch',
                          '&:hover': { bgcolor: '#222' }
                        }}
                      >
                        詳細を確認
                      </Button>
                    </Box>
                    {/* アクションボタン */}
                    <Box sx={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 1,
                      mt: 1,
                      '& .MuiButton-root': {
                        height: 38,
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        borderRadius: 2,
                        minWidth: 0,
                        maxWidth: '100%',
                        px: 1.5,
                        whiteSpace: 'nowrap',
                      }
                    }}>
                      <Button
                        variant="outlined"
                        startIcon={<StorefrontIcon />}
                        href={club.rakutenUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#E91E63',
                          color: '#E91E63',
                          '&:hover': {
                            borderColor: '#C2185B',
                            bgcolor: '#FCE4EC',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        楽天で購入
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<StorefrontIcon />}
                        href={club.yahooUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#FF9800',
                          color: '#FF9800',
                          '&:hover': {
                            borderColor: '#F57C00',
                            bgcolor: '#FFF3E0',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        Yahoo!で購入
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<SearchIcon />}
                        href={club.usedUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#4CAF50',
                          color: '#4CAF50',
                          '&:hover': {
                            borderColor: '#388E3C',
                            bgcolor: '#E8F5E9',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        中古を探す
                      </Button>
                    </Box>
                  </Box>
                </Box>
              ) : (
                <Box sx={{ display: 'flex', gap: 2 }}>
                  {/* 商品画像 */}
                  <Avatar
                    src={club.image}
                    alt={club.name}
                    sx={{ width: 100, height: 100, borderRadius: 2 }}
                  />

                  {/* 商品情報 */}
                  <Box sx={{ flex: 1 }}>
                    {/* ヘッダー部分 */}
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1.5 }}>
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.5 }}>{club.name}</Typography>
                        <Typography variant="subtitle2" color="text.secondary">
                          {club.maker} | {club.specs}
                        </Typography>
                      </Box>
                      <Chip
                        label={`マッチ度 ${club.match}%`}
                        color="primary"
                        size="small"
                        sx={{ fontWeight: 600 }}
                      />
                    </Box>
                    {/* マッチ理由 */}
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ 
                        mb: 1.5,
                        backgroundColor: 'rgba(0, 0, 0, 0.03)',
                        p: 1,
                        borderRadius: 1,
                        fontSize: '0.875rem'
                      }}
                    >
                      {club.matchReason}
                    </Typography>
                    {/* 価格表示＋詳細ボタン */}
                    <Box sx={{ 
                      mb: 2,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: 2
                    }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                            新品価格
                    </Typography>
                          <Typography variant="h6" color="primary" sx={{ fontWeight: 700 }}>
                            ¥{club.price.toLocaleString()}
                    </Typography>
                  </Box>
                        <Box>
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                            中古価格
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="h6" color="success.main" sx={{ fontWeight: 700 }}>
                              ¥{(club.price * 0.6).toLocaleString()}
                    </Typography>
                            <Chip
                              label="40%OFF"
                              size="small"
                              color="success"
                              sx={{ height: 20, fontSize: '0.75rem' }}
                            />
                          </Box>
                        </Box>
                      </Box>
                      <Button
                        variant="contained"
                        startIcon={<InfoOutlinedIcon />}
                        sx={{
                          bgcolor: '#111',
                          color: '#fff',
                          fontWeight: 600,
                          borderRadius: 2,
                          px: 3,
                          height: 38,
                          fontSize: '0.92rem',
                          '&:hover': { bgcolor: '#222' }
                        }}
                      >
                        詳細を確認
                      </Button>
                    </Box>
                    {/* アクションボタン */}
                    <Box sx={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(3, minmax(130px, 1fr))',
                      gap: 1,
                      '& .MuiButton-root': {
                        height: 38,
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        borderRadius: 2,
                        minWidth: 0,
                        maxWidth: '100%',
                        px: 1.5,
                        whiteSpace: 'nowrap',
                      }
                    }}>
                      <Button
                        variant="outlined"
                        startIcon={<StorefrontIcon />}
                        href={club.rakutenUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#E91E63',
                          color: '#E91E63',
                          '&:hover': {
                            borderColor: '#C2185B',
                            bgcolor: '#FCE4EC',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        楽天で購入
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<StorefrontIcon />}
                        href={club.yahooUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#FF9800',
                          color: '#FF9800',
                          '&:hover': {
                            borderColor: '#F57C00',
                            bgcolor: '#FFF3E0',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        Yahoo!で購入
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<SearchIcon />}
                        href={club.usedUrl}
                        target="_blank"
                        sx={{
                          borderColor: '#4CAF50',
                          color: '#4CAF50',
                          '&:hover': {
                            borderColor: '#388E3C',
                            bgcolor: '#E8F5E9',
                            transform: 'translateY(-1px)'
                          }
                        }}
                      >
                        中古を探す
                      </Button>
                    </Box>
                  </Box>
                </Box>
              )}
            </Paper>
          </motion.div>
        ))}
      </Box>
    </Box>
  );
} 