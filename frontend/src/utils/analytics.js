import ReactGA from 'react-ga4';
import { getConfig, isDevelopment } from '../config/environment';

const config = getConfig();

// Google Analyticsの初期化
export const initGA = () => {
  if (isDevelopment()) {
    console.log('GA initialized in development mode');
  }
  ReactGA.initialize(config.gaMeasurementId);
};

// ページビューのトラッキング
export const trackPageView = (path) => {
  if (isDevelopment()) {
    console.log('Page view tracked:', path);
  }
  ReactGA.send({ hitType: "pageview", page: path });
};

// イベントのトラッキング
export const trackEvent = (category, action, label) => {
  if (isDevelopment()) {
    console.log('Event tracked:', { category, action, label });
  }
  ReactGA.event({
    category: category,
    action: action,
    label: label,
  });
};

// ユーザー属性のトラッキング
export const trackUserProperties = (properties) => {
  if (isDevelopment()) {
    console.log('User properties tracked:', properties);
  }
  ReactGA.set(properties);
};

// カスタムイベントのトラッキング
export const trackCustomEvent = (eventName, eventParams) => {
  if (isDevelopment()) {
    console.log('Custom event tracked:', { eventName, eventParams });
  }
  ReactGA.event(eventName, eventParams);
}; 