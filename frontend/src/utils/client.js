import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// エラーメッセージのマッピング
const ERROR_MESSAGES = {
  400: 'リクエストが不正です',
  401: '認証が必要です',
  403: 'アクセスが拒否されました',
  404: 'リソースが見つかりません',
  422: '入力データが不正です',
  500: 'サーバーエラーが発生しました',
};

// エラーレスポンスの解析
const parseErrorResponse = (error) => {
  if (error.response) {
    const { status, data } = error.response;
    const baseMessage = ERROR_MESSAGES[status] || '予期せぬエラーが発生しました';
    
    // バリデーションエラーの場合
    if (status === 422 && data.detail) {
      if (Array.isArray(data.detail)) {
        return data.detail.map(err => `${err.loc[1]}: ${err.msg}`).join('\n');
      }
      return `${baseMessage}: ${data.detail}`;
    }
    
    // その他のエラーの場合
    return data.message || baseMessage;
  }
  
  if (error.request) {
    return 'サーバーに接続できません';
  }
  
  return 'リクエストの作成中にエラーが発生しました';
};

// APIクライアントの設定
const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター
client.interceptors.request.use(
  (config) => {
    console.log('Sending request to:', config.url);
    console.log('Request data:', config.data);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// レスポンスインターセプター
client.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.data);
    return response;
  },
  (error) => {
    const errorMessage = parseErrorResponse(error);
    console.error('API Error:', errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

// APIメソッド
export const api = {
  // クラブ関連
  getClubs: () => client.get('/clubs'),
  getClubById: (id) => client.get(`/clubs/${id}`),
  getClubsByType: (type) => client.get(`/clubs/${type}`),
  getClubsByBrand: (brand) => client.get(`/clubs/brand/${brand}`),
  
  // レコメンデーション関連
  createRecommendation: (data) => client.post('/recommendations/', data),
  getRecommendations: () => client.get('/recommendations/'),
  getRecommendationById: (id) => client.get(`/recommendations/${id}`),
  updateRecommendation: (id, data) => client.put(`/recommendations/${id}`, data),
  deleteRecommendation: (id) => client.delete(`/recommendations/${id}`),
};

export default api; 
