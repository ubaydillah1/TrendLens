package model

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/datatypes"
)

type ResearchReport struct {
	ID              uuid.UUID `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID          uuid.UUID `gorm:"type:uuid;index;not null" json:"user_id"`
	Date            string    `gorm:"index;not null" json:"date"`
	TargetNiche     string    `json:"target_niche"`
	UserPositioning string    `gorm:"type:text" json:"user_positioning"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`

	Ideas []ContentIdea `gorm:"foreignKey:ReportID;constraint:OnDelete:CASCADE" json:"ideas"`
}

type ContentIdea struct {
	ID                     uuid.UUID                   `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	ReportID               uuid.UUID                   `gorm:"type:uuid;index;not null" json:"report_id"`
	Category               string                      `json:"category"`
	TopicTitle             string                      `gorm:"type:text" json:"topic_title"`
	ViralHooks             datatypes.JSONSlice[string] `gorm:"type:jsonb" json:"viral_hooks"`
	VisualHookDirection    string                      `gorm:"type:text" json:"visual_hook_direction"`
	ContentOutline         datatypes.JSONSlice[string] `gorm:"type:jsonb" json:"content_outline"`
	TechnicalDatapoint     string                      `gorm:"type:text" json:"technical_datapoint"`
	EngagementCTA          string                      `gorm:"type:text" json:"engagement_cta"`
	WhyItWorks             string                      `gorm:"type:text" json:"why_it_works"`
	SourceTechnicalTopic   string                      `gorm:"type:text" json:"source_technical_topic"`
	NewsSourceURL          string                      `gorm:"type:text" json:"news_source_url"`
	CommunityDiscussionURL string                      `gorm:"type:text" json:"community_discussion_url"`
	InspirationVideoURL    string                      `gorm:"type:text" json:"inspiration_video_url"`
	CreatedAt              time.Time                   `json:"created_at"`
}
