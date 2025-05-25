import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

const Terms = () => {
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
            利用規約
          </Typography>
          <Typography sx={{ fontSize: 15, color: '#444', mb: 4, textAlign: 'center' }}>
            この利用規約（以下「本規約」といいます）は、Swing Fit Pro（以下「当サービス」といいます）が提供するAIゴルフクラブ診断・レコメンドサービス（以下「本サービス」）の利用条件を定めるものです。本サービスをご利用いただく前に、必ず本規約をお読みの上、同意いただく必要があります。
          </Typography>
          <Box sx={{ maxWidth: 800, mx: 'auto', textAlign: 'left', color: '#222', fontSize: 15, lineHeight: 2 }}>
            <strong>第1条（適用範囲）</strong><br />
            本規約は、当サービスのWebサイト・アプリ・関連サービスの全ての利用に適用されます。<br /><br />
            <strong>第2条（サービス内容）</strong><br />
            1. 本サービスは、ユーザーが入力したゴルフ歴・スコア・悩み等の情報に基づき、AIが最適なゴルフクラブや練習法、レッスン等をレコメンドするものです。<br />
            2. 本サービスは、各種ゴルフクラブのスペック・レビュー・価格情報等を第三者サービスや提携先から取得し、参考情報として表示します。<br />
            3. 本サービスは、ユーザーのゴルフ上達や最適なクラブ選びをサポートするものであり、購入・契約等の最終判断はユーザーご自身の責任で行っていただきます。<br /><br />
            <strong>第3条（利用登録・アカウント）</strong><br />
            1. 一部機能のご利用には、ユーザー登録が必要な場合があります。<br />
            2. 登録情報に虚偽があった場合、当サービスはアカウントの停止・削除等の措置をとることができます。<br /><br />
            <strong>第4条（知的財産権）</strong><br />
            1. 本サービスに掲載される文章・画像・プログラム等の著作権その他の知的財産権は、当サービスまたは正当な権利者に帰属します。<br />
            2. ユーザーは、当サービスの内容を私的利用の範囲を超えて利用することはできません。<br /><br />
            <strong>第5条（禁止事項）</strong><br />
            ユーザーは、以下の行為を行ってはなりません。<br />
            ・本サービスの運営を妨げる行為<br />
            ・他のユーザーまたは第三者の権利・利益を侵害する行為<br />
            ・虚偽情報の入力、なりすまし<br />
            ・法令または公序良俗に反する行為<br /><br />
            <strong>第6条（免責事項）</strong><br />
            1. 本サービスは、AIによる診断・レコメンドや各種情報の正確性・完全性・有用性を保証するものではありません。<br />
            2. 本サービスを利用したことによる損害・トラブル等について、当サービスは一切の責任を負いません。<br />
            3. 本サービスに掲載されている価格・在庫・レビュー等は、提携先や第三者サービスの情報をもとに表示しており、最新・正確であることを保証するものではありません。<br /><br />
            <strong>第7条（サービスの変更・停止・終了）</strong><br />
            当サービスは、事前の通知なく本サービスの内容を変更・停止・終了することができます。<br /><br />
            <strong>第8条（個人情報の取扱い）</strong><br />
            本サービスにおける個人情報の取扱いについては、別途定める「プライバシーポリシー」に従います。<br /><br />
            <strong>第9条（規約の変更）</strong><br />
            当サービスは、必要に応じて本規約を改定することができます。改定後の規約は、Webサイト上で掲示した時点から効力を生じます。<br /><br />
            <strong>第10条（準拠法・裁判管轄）</strong><br />
            本規約は日本法に準拠し、本サービスに関する紛争は東京都を管轄する裁判所を第一審の専属的合意管轄裁判所とします。<br /><br />
            <div style={{ marginTop: 32, color: '#888', fontSize: 14 }}>
              Swing Fit Pro 運営事務局<br />
              制定日：2025年6月1日
            </div>
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

export default Terms; 