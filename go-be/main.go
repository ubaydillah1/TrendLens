package main

import (
	"net/http"

	"trendlens-core/config"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize database connection (Schema managed via migrations/)
	db := config.ConnectDB()
	_ = db

	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message":  "pong",
			"database": "connected",
		})
	})

	r.Run(":8080")
}
