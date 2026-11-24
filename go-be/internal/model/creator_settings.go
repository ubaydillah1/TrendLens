package model

import (
	"time"

	"github.com/google/uuid"
)

type CreatorSettings struct {
	ID              uuid.UUID `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID          uuid.UUID `gorm:"type:uuid;uniqueIndex;not null" json:"user_id"`
	Niche           string    `gorm:"default:'AI & Software Engineering'" json:"niche"`
	UserPositioning string    `gorm:"type:text" json:"user_positioning"`
	ScheduleHour    int       `gorm:"default:6" json:"schedule_hour"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}
