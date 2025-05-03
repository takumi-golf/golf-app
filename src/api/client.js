// APIのベースURLを設定
const API_BASE_URL = process.env.REACT_APP_API_URL;

// レコメンデーションリクエストの関数
export const getRecommendations = async (data) => {
  try {
    console.log('Sending recommendation request with data:', data);
    console.log('Sending request to:', `${API_BASE_URL}/recommendations/`);
    const response = await axios.post(`${API_BASE_URL}/recommendations/`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('レコメンデーション生成エラー:', error);
    throw error;
  }
};