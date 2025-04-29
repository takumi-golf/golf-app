-- 既存のテーブル
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT,
    website TEXT,
    established_year INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    release_year INTEGER,
    target_handicap_range TEXT,
    technology_description TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    UNIQUE(manufacturer_id, name)
);

CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    club_type TEXT NOT NULL,
    loft_range TEXT,
    length_range TEXT,
    weight_range TEXT,
    stock_options TEXT,
    msrp REAL,
    release_year INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(id),
    UNIQUE(series_id, name)
);

-- 新しいテーブル: シャフト情報
CREATE TABLE IF NOT EXISTS shaft_manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    website TEXT,
    established_year INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shaft_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    release_year INTEGER,
    technology_description TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES shaft_manufacturers(id)
);

CREATE TABLE IF NOT EXISTS shafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    flex TEXT,
    weight_range TEXT,
    material TEXT,
    torque_range TEXT,
    launch_characteristics TEXT,
    spin_characteristics TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    UNIQUE(manufacturer_id, name)
);

-- 新しいテーブル: クラブの進化履歴
CREATE TABLE IF NOT EXISTS club_histories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    release_date DATE,
    discontinuation_date DATE,
    technology_changes TEXT,
    design_changes TEXT,
    performance_changes TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- 新しいテーブル: プロの使用実績
CREATE TABLE IF NOT EXISTS pro_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    tour TEXT,
    world_ranking INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pro_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pro_player_id INTEGER NOT NULL,
    model_id INTEGER,
    shaft_id INTEGER,
    start_date DATE,
    end_date DATE,
    tournament_results TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pro_player_id) REFERENCES pro_players(id),
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (shaft_id) REFERENCES shafts(id)
);

-- 新しいテーブル: レコメンデーション情報
CREATE TABLE IF NOT EXISTS swing_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    characteristics TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    shaft_id INTEGER,
    handicap_range TEXT,
    swing_type_id INTEGER,
    recommended_settings TEXT,
    performance_characteristics TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (shaft_id) REFERENCES shafts(id),
    FOREIGN KEY (swing_type_id) REFERENCES swing_types(id)
);

-- 新しいテーブル: データ収集履歴
CREATE TABLE IF NOT EXISTS data_collection_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER,
    collection_type TEXT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT,
    error_message TEXT,
    records_processed INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
);

-- パフォーマンスデータテーブル
CREATE TABLE IF NOT EXISTS performance_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    carry_distance REAL,
    total_distance REAL,
    launch_angle REAL,
    spin_rate REAL,
    ball_speed REAL,
    club_speed REAL,
    smash_factor REAL,
    dispersion REAL,
    peak_height REAL,
    descent_angle REAL,
    date TIMESTAMP,
    conditions TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- グリップテーブル
CREATE TABLE IF NOT EXISTS grips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    material TEXT,
    size_range TEXT,
    texture TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    UNIQUE(manufacturer_id, name)
);

-- モデルとシャフトの関連テーブル
CREATE TABLE IF NOT EXISTS model_shafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    shaft_id INTEGER NOT NULL,
    is_stock BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (shaft_id) REFERENCES shafts(id),
    UNIQUE(model_id, shaft_id)
);

-- モデルとグリップの関連テーブル
CREATE TABLE IF NOT EXISTS model_grips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    grip_id INTEGER NOT NULL,
    is_stock BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (grip_id) REFERENCES grips(id),
    UNIQUE(model_id, grip_id)
);

-- スペックテーブル
CREATE TABLE IF NOT EXISTS specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    loft REAL,
    lie REAL,
    length REAL,
    swing_weight TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id),
    UNIQUE(model_id, loft, lie, length)
);

-- レビューテーブル
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    source TEXT,
    rating REAL,
    review_text TEXT,
    pros TEXT,
    cons TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- 価格履歴テーブル
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    price REAL NOT NULL,
    currency TEXT DEFAULT 'JPY',
    date DATE NOT NULL,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- インデックスの作成
CREATE INDEX IF NOT EXISTS idx_manufacturers_name ON manufacturers(name);
CREATE INDEX IF NOT EXISTS idx_series_manufacturer_id ON series(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_models_series_id ON models(series_id);
CREATE INDEX IF NOT EXISTS idx_models_club_type ON models(club_type);
CREATE INDEX IF NOT EXISTS idx_shafts_manufacturer_id ON shafts(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_grips_manufacturer_id ON grips(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_performance_data_model_id ON performance_data(model_id);
CREATE INDEX IF NOT EXISTS idx_performance_data_date ON performance_data(date);
CREATE INDEX IF NOT EXISTS idx_pro_usage_dates ON pro_usage(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_recommendations_handicap ON recommendations(handicap_range);
CREATE INDEX IF NOT EXISTS idx_data_collection_logs_status ON data_collection_logs(status);

-- トリガー
CREATE TRIGGER IF NOT EXISTS update_manufacturers_timestamp
    AFTER UPDATE ON manufacturers
    FOR EACH ROW
    BEGIN
        UPDATE manufacturers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_series_timestamp
    AFTER UPDATE ON series
    FOR EACH ROW
    BEGIN
        UPDATE series SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_models_timestamp
    AFTER UPDATE ON models
    FOR EACH ROW
    BEGIN
        UPDATE models SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_shafts_timestamp
    AFTER UPDATE ON shafts
    FOR EACH ROW
    BEGIN
        UPDATE shafts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_grips_timestamp
    AFTER UPDATE ON grips
    FOR EACH ROW
    BEGIN
        UPDATE grips SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_performance_data_timestamp
    AFTER UPDATE ON performance_data
    FOR EACH ROW
    BEGIN
        UPDATE performance_data SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- メーカーテーブル
CREATE TABLE manufacturers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- クラブ基本情報テーブル
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id),
    model VARCHAR(50) NOT NULL,
    head_volume VARCHAR(20),
    price INTEGER,
    features TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ロフト角テーブル
CREATE TABLE lofts (
    id SERIAL PRIMARY KEY,
    club_id INTEGER REFERENCES clubs(id),
    loft VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- シャフトオプションテーブル
CREATE TABLE shafts (
    id SERIAL PRIMARY KEY,
    club_id INTEGER REFERENCES clubs(id),
    shaft VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- フレックステーブル
CREATE TABLE flexes (
    id SERIAL PRIMARY KEY,
    club_id INTEGER REFERENCES clubs(id),
    flex VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 