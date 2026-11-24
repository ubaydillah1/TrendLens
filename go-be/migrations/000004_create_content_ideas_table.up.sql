CREATE TABLE IF NOT EXISTS content_ideas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES research_reports(id) ON DELETE CASCADE,
    category VARCHAR(100),
    topic_title TEXT NOT NULL,
    viral_hooks JSONB DEFAULT '[]'::jsonb,
    visual_hook_direction TEXT,
    content_outline JSONB DEFAULT '[]'::jsonb,
    technical_datapoint TEXT,
    engagement_cta TEXT,
    why_it_works TEXT,
    source_technical_topic TEXT,
    news_source_url TEXT,
    community_discussion_url TEXT,
    inspiration_video_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_ideas_report_id ON content_ideas(report_id);
