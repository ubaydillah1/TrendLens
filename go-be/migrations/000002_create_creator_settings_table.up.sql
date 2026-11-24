CREATE TABLE IF NOT EXISTS creator_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    niche VARCHAR(255) NOT NULL DEFAULT 'AI & Software Engineering',
    user_positioning TEXT,
    schedule_hour INT DEFAULT 6,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
