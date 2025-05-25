import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// リクエストインターセプター
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// レスポンスインターセプター
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // 認証エラーの場合、ログインページにリダイレクト
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// レコメンデーション生成
export const getRecommendations = async (userData) => {
  try {
    console.log('Sending recommendation request with data:', userData);
    const response = await apiClient.post('/api/recommendations/', userData);
    console.log('Received recommendation response:', response.data);
    if (!response.data || !Array.isArray(response.data)) {
      throw new Error('Invalid response format from server');
    }
    return response.data;
  } catch (error) {
    console.error('レコメンデーション生成エラー:', error);
    throw error;
  }
};

// レコメンデーション作成
export const createRecommendation = async (data) => {
  try {
    console.log('Creating recommendation with data:', data);
    const response = await apiClient.post('/api/v1/recommendations/', data);
    console.log('Received create recommendation response:', response.data);
    return response.data;
  } catch (error) {
    console.error('レコメンデーション作成エラー:', error);
    
    if (error.response) {
      const { status, data } = error.response;
      console.error('エラーの詳細:', data);
      
      // バックエンドからのエラーメッセージを処理
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          // バリデーションエラーの場合
          const errorMessages = data.detail.map(err => {
            const field = err.loc[err.loc.length - 1];
            return `${field}: ${err.msg}`;
          });
          throw new Error(errorMessages.join('\n'));
        } else {
          // その他のエラーの場合
          throw new Error(data.detail);
        }
      }
      
      // ステータスコードに基づくエラーメッセージ
      switch (status) {
        case 422:
          throw new Error('入力データが不正です。入力内容を確認してください。');
        case 500:
          throw new Error('サーバーエラーが発生しました。しばらく経ってから再度お試しください。');
        default:
          throw new Error(`エラーが発生しました（ステータスコード: ${status}）`);
      }
    }
    
    throw new Error('ネットワークエラーが発生しました。インターネット接続を確認してください。');
  }
};

// レコメンデーション履歴取得
export const getRecommendationHistory = async () => {
  try {
    const response = await apiClient.get('/api/recommendations/history/');
    return response.data;
  } catch (error) {
    console.error('履歴取得エラー:', error);
    throw error;
  }
};

// フィードバック送信
export const submitFeedback = async (recommendationId, feedback) => {
  try {
    const response = await apiClient.post(`/api/recommendations/${recommendationId}/feedback/`, { feedback });
    return response.data;
  } catch (error) {
    console.error('フィードバック送信エラー:', error);
    throw error;
  }
};

// 14本クラブセットのレコメンド（複数セット・マッチ度順）
export const getClubSetRecommendations = async (userData) => {
  try {
    const response = await apiClient.post('/api/v1/recommendations/sets', userData);
    return response.data;
  } catch (error) {
    console.error('クラブセットレコメンド取得エラー:', error);
    throw error;
  }
};

export default apiClient; 