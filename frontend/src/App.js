import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import AppsIcon from '@mui/icons-material/Apps';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import RecommendationForm from './components/RecommendationForm';
import RecommendationResult from './components/RecommendationResult';
import useMediaQuery from '@mui/material/useMediaQuery';
import Typography from '@mui/material/Typography';
import { motion, AnimatePresence } from 'framer-motion';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';

const theme = createTheme({
palette: {
primary: { main: '#1B5E20' },
secondary: { main: '#F57C00' },
background: { default: '#F5F5F5', paper: '#FFFFFF' },
},
typography: {
fontFamily: 'Noto Sans JP, sans-serif',
allVariants: {
lineHeight: 1.2,
marginBlockStart: 0,
marginBlockEnd: 0,
WebkitFontSmoothing: 'antialiased',
MozOsxFontSmoothing: 'grayscale',
},
h3: {
fontWeight: 700,
letterSpacing: '0.05em',
fontSize: '2rem',
},
h4: {
fontWeight: 700,
letterSpacing: '0.05em',
fontSize: '1.75rem',
},
h5: {
fontWeight: 600,
letterSpacing: '0.02em',
fontSize: '1.5rem',
},
h6: {
fontWeight: 600,
letterSpacing: '0.02em',
fontSize: '1.25rem',
},
body1: {
letterSpacing: '0.02em',
fontSize: '1rem',
},
body2: {
letterSpacing: '0.02em',
fontSize: '0.875rem',
},
},
breakpoints: {
values: { xs: 0, sm: 600, md: 960, lg: 1280, xl: 1920 },
},
});

function App() {
const [recommendation, setRecommendation] = useState(null);
const [isExpanded, setIsExpanded] = useState(false);
const isDesktop = useMediaQuery(theme.breakpoints.up('md'));

const handleRecommend = (data) => {
setRecommendation(data);
setIsExpanded(true);
};

const handleBack = () => {
setIsExpanded(false);
setRecommendation(null); // 結果データもリセット
};

return (
<ThemeProvider theme={theme}>
<CssBaseline />
<Box
sx={{
display: 'flex',
minHeight: '100vh',
flexDirection: { xs: 'column', md: 'row' },
gap: { xs: 2, md: 4 },
p: { xs: 2, md: 4 },
backgroundColor: 'background.default',
position: 'relative',
overflow: 'hidden',
alignItems: { md: 'center' },
justifyContent: { xs: 'center', md: 'flex-start' }
}}
>
{/* 左カラム - ナビゲーション */}
<Box
sx={{
width: { md: 112 },
flexShrink: 0,
display: 'flex',
flexDirection: { xs: 'row', md: 'column' },
justifyContent: { xs: 'space-between', md: 'flex-start' },
alignItems: 'center',
gap: 2,
order: { xs: 2, md: 0 },
mb: { xs: 2, md: 0 },
height: { md: 'auto' }
}}
>
<Box
sx={{
backgroundColor: 'primary.main',
p: 1,
borderRadius: 1,
display: 'flex',
justifyContent: 'center',
alignItems: 'center',
}}
>
<img
src={isDesktop ? '/service-logos/logo-vertical.png.png' : '/service-logos/logo-horizontal.png.png'}
alt="SwingFitProロゴ"
style={{
width: isDesktop ? 64 : 80,
height: 'auto',
}}
/>
</Box>
<Box
sx={{
display: 'flex',
flexDirection: { xs: 'row', md: 'column' },
gap: 1,
}}
>
<IconButton color="primary">
<HelpOutlineIcon />
</IconButton>
<IconButton color="primary">
<AppsIcon />
</IconButton>
<IconButton color="primary">
<AccountCircleIcon />
</IconButton>
</Box>
</Box>

{/* 中央カラム - メインコンテンツ */}
<Box
component={motion.div}
animate={{
width: isExpanded
? 'calc(60% - 56px)'
: 'calc(100% - 116px)',
transition: {
type: 'spring',
stiffness: 300,
damping: 30,
restDelta: 0.001
}
}}
sx={{
flexShrink: 0,
minWidth: 0,
position: 'relative',
zIndex: 2,
maxWidth: '100%',
overflow: 'hidden',
display: 'flex',
alignItems: 'center',
justifyContent: 'center'
}}
>
<Box
sx={{
width: '100%',
maxWidth: 800,
margin: '0 auto',
paddingRight: { md: 2 },
display: 'flex',
flexDirection: 'column',
justifyContent: 'center'
}}
>
<RecommendationForm onRecommend={handleRecommend} />
</Box>
</Box>

{/* 右カラム - サイドバー */}
<AnimatePresence mode="wait">
{isExpanded && (
<motion.div
initial={{ x: '100%', opacity: 0 }}
animate={{ x: 0, opacity: 1 }}
exit={{ x: '100%', opacity: 0 }}
transition={{ type: 'spring', stiffness: 300, damping: 30 }}
style={{
position: 'absolute',
top: 0,
right: 0,
width: '40%',
height: '100%',
zIndex: 3
}}
>
<Box
sx={{
height: '100%',
backgroundColor: 'background.paper',
boxShadow: 3,
p: 4,
position: 'relative',
}}
>
<IconButton
onClick={handleBack}
sx={{
position: 'absolute',
left: 16,
top: 16,
zIndex: 4
}}
>
<ArrowBackIosIcon />
</IconButton>
<RecommendationResult recommendation={recommendation} />
</Box>
</motion.div>
)}
</AnimatePresence>
</Box>
</ThemeProvider>
);
}

export default App;