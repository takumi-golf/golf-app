const ENV = process.env.REACT_APP_ENV || 'development';

const config = {
  development: {
    apiUrl: 'http://localhost:8000',
    gaMeasurementId: 'G-DEV-XXXXXXXX', // 開発環境用のGA測定ID
    debug: true,
  },
  staging: {
    apiUrl: 'https://staging-api.swingfit-pro.com',
    gaMeasurementId: 'G-STAGING-XXXXXXXX', // ステージング環境用のGA測定ID
    debug: true,
  },
  production: {
    apiUrl: 'https://api.swingfit-pro.com',
    gaMeasurementId: 'G-PROD-XXXXXXXX', // 本番環境用のGA測定ID
    debug: false,
  }
};

export const getConfig = () => {
  return config[ENV] || config.development;
};

export const isDevelopment = () => ENV === 'development';
export const isStaging = () => ENV === 'staging';
export const isProduction = () => ENV === 'production'; 