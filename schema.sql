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