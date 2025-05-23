import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false
});

// リクエストインターセプター
client.interceptors.request.use(
  config => {
    // リクエスト送信前の処理
    console.log('Sending request to:', config.url);
    return config;
  },
  error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// レスポンスインターセプター
client.interceptors.response.use(
  response => {
    // レスポンス受信時の処理
    console.log('Received response from:', response.config.url);
    return response;
  },
  error => {
    // エラーハンドリング
    if (error.response) {
      // サーバーからのレスポンスがある場合
      console.error('API Error:', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      });
    } else if (error.request) {
      // リクエストは送信されたがレスポンスがない場合
      console.error('No response received:', error.request);
    } else {
      // リクエストの設定中にエラーが発生した場合
      console.error('Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

// レコメンデーション生成
export const getRecommendations = async (userData) => {
  try {
    console.log('Sending recommendation request with data:', userData);
    const response = await client.post('/api/recommendations/', userData);
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
export const createRecommendation = async (recommendationData) => {
  try {
    console.log('Creating recommendation with data:', recommendationData);
    const response = await client.post('/api/recommendations/create/', recommendationData);
    console.log('Received create recommendation response:', response.data);
    return response;
  } catch (error) {
    console.error('レコメンデーション作成エラー:', error);
    throw error;
  }
};

// レコメンデーション履歴取得
export const getRecommendationHistory = async () => {
  try {
    const response = await client.get('/api/recommendations/history/');
    return response.data;
  } catch (error) {
    console.error('履歴取得エラー:', error);
    throw error;
  }
};

// フィードバック送信
export const submitFeedback = async (recommendationId, feedback) => {
  try {
    const response = await client.post(`/api/recommendations/${recommendationId}/feedback/`, { feedback });
    return response.data;
  } catch (error) {
    console.error('フィードバック送信エラー:', error);
    throw error;
  }
};

export const api = {
  getRecommendations,
  createRecommendation,
  getRecommendationHistory,
  submitFeedback
};

export default client; 