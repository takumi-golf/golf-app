describe('レコメンデーション機能', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
  });

  it('フォーム入力とレコメンデーション生成', () => {
    // フォーム入力
    cy.get('input[name="height"]').type('175');
    cy.get('input[name="weight"]').type('70');
    cy.get('input[name="age"]').type('35');
    cy.get('input[name="handicap"]').type('15');
    cy.get('input[name="headSpeed"]').type('45');
    cy.get('input[name="budget"]').type('200000');

    // 送信ボタンクリック
    cy.get('button[type="submit"]').click();

    // ローディング表示の確認
    cy.get('.MuiCircularProgress-root').should('be.visible');

    // 結果表示の確認
    cy.get('.MuiPaper-root').should('contain', 'レコメンデーション結果');
    cy.get('.MuiPaper-root').should('contain', 'マッチ度');
  });

  it('エラー表示の確認', () => {
    // 空のフォームで送信
    cy.get('button[type="submit"]').click();

    // エラーメッセージの確認
    cy.get('.MuiAlert-root').should('be.visible');
  });

  it('APIエラーハンドリング', () => {
    // 不正なデータで送信
    cy.get('input[name="height"]').type('999');
    cy.get('input[name="weight"]').type('999');
    cy.get('input[name="age"]').type('999');
    cy.get('input[name="handicap"]').type('999');
    cy.get('input[name="headSpeed"]').type('999');
    cy.get('input[name="budget"]').type('999999999');

    cy.get('button[type="submit"]').click();

    // エラーメッセージの確認
    cy.get('.MuiAlert-root').should('be.visible');
  });

  it('レスポンシブデザインの確認', () => {
    // モバイルビュー
    cy.viewport('iphone-6');
    cy.get('.MuiBox-root').should('have.css', 'max-width', '600px');

    // デスクトップビュー
    cy.viewport('macbook-13');
    cy.get('.MuiBox-root').should('have.css', 'max-width', '600px');
  });
}); 