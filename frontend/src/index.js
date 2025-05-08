import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// パフォーマンス最適化のための設定
const container = document.getElementById('root');
const root = createRoot(container);

// StrictModeを有効化して開発時の問題を早期発見
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// パフォーマンス計測の設定
reportWebVitals(console.log); 