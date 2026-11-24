package model

import (
	"time"

	"github.com/google/uuid"
)

type User struct {
	ID           uuid.UUID `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	Name         string    `gorm:"not null" json:"name"`
	Email        string    `gorm:"uniqueIndex;not null" json:"email"`
	PasswordHash string    `gorm:"not null" json:"-"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`

	Settings *CreatorSettings `gorm:"foreignKey:UserID;constraint:OnDelete:CASCADE" json:"settings,omitempty"`
	Reports  []ResearchReport `gorm:"foreignKey:UserID;constraint:OnDelete:CASCADE" json:"reports,omitempty"`
}
