import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

const Privacy = () => {
  const navigate = useNavigate();
  return (
    <>
      {/* ヘッダー（ロゴのみ） */}
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
      {/* サイドバー＋本文レイアウト */}
      <Box sx={{ width: '100%', height: 'calc(100vh - 56px)', background: 'linear-gradient(135deg, #F7F9FB 0%, #E3E6EA 100%)', position: 'relative' }}>
        {/* サイドバー（トップページと同じデザイン, Xリンク常時表示） */}
        <Box
          sx={{
            width: 74,
            minWidth: 74,
            bgcolor: '#fff',
            color: '#222',
            display: { xs: 'none', md: 'flex' },
            flexDirection: 'column',
            alignItems: 'stretch',
            justifyContent: 'space-between',
            height: 'calc(100vh - 56px)',
            boxShadow: 2,
            borderRight: '1px solid #E3E6EA',
            position: 'fixed',
            top: 56,
            left: 0,
            zIndex: 100,
            p: 0,
            m: 0,
            boxSizing: 'border-box',
          }}
        >
          {/* 上部：AI診断 */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'center', mt: 1 }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 0.5,
                width: '100%',
                py: 1,
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(.4,2,.6,1)',
                bgcolor: 'transparent',
                color: '#222',
                fontWeight: 400,
                '& svg': { color: '#222' },
                '&:hover': {
                  background: '#f3f3f4',
                  color: '#1976D2',
                  fontWeight: 700,
                  '& svg': { color: '#1976D2' }
                }
              }}
              tabIndex={0}
              role="button"
              onClick={() => navigate('/')}
            >
              <SmartToyIcon sx={{ fontSize: 23, mb: 0.5, transition: 'color 0.18s' }} />
              <span style={{ fontWeight: 700, fontSize: 12, letterSpacing: 1 }}>AI診断</span>
            </Box>
          </Box>
          {/* 下部：Xリンク */}
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'center' }}>
            <Tooltip
              title={<span>お問い合わせは<br />DMまで</span>}
              arrow
              placement="top"
              PopperProps={{
                modifiers: [
                  { name: 'offset', options: { offset: [12, 8] } },
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
                sx={{ color: '#222', p: 0.5, '&:hover': { color: '#1976D2', opacity: 1 } }}
              >
                <img src="/sns-logos/logo-black.png" alt="Xロゴ" width="17" height="17" />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        {/* 本文（エリア全体を広く使い、背景を白に） */}
        <Box sx={{
          ml: { md: '74px', xs: 0 },
          width: { md: 'calc(100% - 74px)', xs: '100%' },
          minHeight: 'calc(100vh - 56px)',
          height: 'auto',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          bgcolor: '#fff',
          px: { xs: 2, md: 8 },
          pt: '72px',
          pb: 0,
        }}>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 3, textAlign: 'center', mt: 2 }}>
            プライバシーポリシー
          </Typography>
          <Box sx={{ maxWidth: 800, mx: 'auto', textAlign: 'left', color: '#222', fontSize: 15, lineHeight: 2 }}>
            <p>Swing Fit Pro（以下「当サービス」といいます）は、ユーザーの個人情報の保護を重要な責務と認識し、以下の方針に基づき、個人情報の適切な取り扱い・管理・保護に努めます。</p>
            <br />
            <strong>1. 個人情報の定義</strong><br />
            当サービスが取得・管理する「個人情報」とは、氏名、メールアドレス、その他特定の個人を識別できる情報を指します。<br /><br />
            <strong>2. 取得する情報</strong><br />
            当サービスは、以下の情報を取得する場合があります。<br />
            ・ユーザーが入力したプロフィール情報（例：ゴルフ歴、スコア、悩み等）<br />
            ・メールアドレス、ニックネーム等の登録情報<br />
            ・サービス利用履歴、アクセスログ、Cookie等の技術情報<br />
            ・その他、サービス運営・改善に必要な情報<br /><br />
            <strong>3. 利用目的</strong><br />
            取得した個人情報は、以下の目的で利用します。<br />
            ・AI診断・レコメンド等、サービス提供のため<br />
            ・サービス改善・新機能開発のための分析<br />
            ・ユーザーへの連絡、メンテナンス・重要なお知らせのため<br />
            ・利用規約違反等への対応<br />
            ・広告配信・マーケティング（同意を得た場合のみ）<br /><br />
            <strong>4. 第三者提供</strong><br />
            当サービスは、法令に基づく場合を除き、ユーザーの同意なく個人情報を第三者に提供しません。<br /><br />
            <strong>5. 委託・共同利用</strong><br />
            個人情報の取り扱いを外部に委託する場合、委託先を適切に管理・監督します。<br />
            共同利用を行う場合は、その範囲・目的・管理責任者を別途明示します。<br /><br />
            <strong>6. 開示・訂正・削除等の請求</strong><br />
            ユーザーは、自己の個人情報について、開示・訂正・利用停止・削除等を請求できます。ご希望の場合は、下記の窓口までご連絡ください。<br /><br />
            <strong>7. Cookie等の利用</strong><br />
            当サービスは、ユーザー体験向上やアクセス解析のため、Cookie等の技術を利用する場合があります。<br />
            Googleアナリティクス等の外部サービスを利用する場合は、その旨およびデータ利用方法についても明記します。<br /><br />
            <strong>8. 法令遵守と見直し</strong><br />
            当サービスは、個人情報保護法その他関連法令を遵守し、必要に応じて本ポリシーの内容を見直し・改善します。<br /><br />
            <strong>9. お問い合わせ窓口</strong><br />
            個人情報の取り扱いに関するお問い合わせは、下記フォームよりご連絡ください。<br />
            <a href="https://forms.gle/8TEkdbwUhc3WpN829" target="_blank" rel="noopener noreferrer">お問い合わせフォーム</a><br />
            <br />
          </Box>
          <Box sx={{ textAlign: 'center', mt: 4, mb: 6 }}>
            <Button variant="outlined" color="primary" onClick={() => navigate('/')} sx={{ borderRadius: 999, px: 4, py: 1, fontWeight: 700 }}>
              診断に戻る
            </Button>
          </Box>
        </Box>
      </Box>
    </>
  );
};

export default Privacy; 