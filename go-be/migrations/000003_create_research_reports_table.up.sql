CREATE TABLE IF NOT EXISTS research_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date VARCHAR(50) NOT NULL,
    target_niche VARCHAR(255),
    user_positioning TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_research_reports_user_id ON research_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_research_reports_date ON research_reports(date);
