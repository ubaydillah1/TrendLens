DB_URL ?= postgres://postgres:postgres@localhost:5432/trendlens_core?sslmode=disable

.PHONY: migrate-up migrate-down migrate-version migrate-create

migrate-up:
	migrate -path migrations -database "$(DB_URL)" up

migrate-down:
	migrate -path migrations -database "$(DB_URL)" down 1

migrate-version:
	migrate -path migrations -database "$(DB_URL)" version

migrate-create:
	@if [ -z "$(name)" ]; then echo "Error: 'name' is required. Example: make migrate-create name=add_tags"; exit 1; fi
	migrate create -ext sql -dir migrations -seq $(name)
