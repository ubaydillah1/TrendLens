param (
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet("up", "down", "create", "version", "force")]
    [string]$Action,

    [Parameter(Position = 1, Mandatory = $false)]
    [string]$Arg = ""
)

$DB_URL = if ($env:DATABASE_URL) {
    $env:DATABASE_URL
} else {
    "postgres://postgres:postgres@localhost:5432/trendlens_core?sslmode=disable"
}

$MIGRATIONS_DIR = "migrations"

switch ($Action) {
    "up" {
        Write-Host "🚀 Running migrations UP on trendlens_core..." -ForegroundColor Cyan
        migrate -path $MIGRATIONS_DIR -database $DB_URL up
    }
    "down" {
        $count = if ($Arg) { $Arg } else { "1" }
        Write-Host "⏪ Rolling back $count migration(s) on trendlens_core..." -ForegroundColor Yellow
        migrate -path $MIGRATIONS_DIR -database $DB_URL down $count
    }
    "version" {
        Write-Host "📌 Current migration version:" -ForegroundColor Green
        migrate -path $MIGRATIONS_DIR -database $DB_URL version
    }
    "force" {
        if (-not $Arg) {
            Write-Error "Please specify the version to force, e.g.: .\migrate.ps1 force 1"
            exit 1
        }
        Write-Host "⚠️ Forcing migration version to $Arg..." -ForegroundColor Red
        migrate -path $MIGRATIONS_DIR -database $DB_URL force $Arg
    }
    "create" {
        if (-not $Arg) {
            Write-Error "Please specify migration name, e.g.: .\migrate.ps1 create add_status_to_users"
            exit 1
        }
        Write-Host "📝 Creating new migration: $Arg..." -ForegroundColor Cyan
        migrate create -ext sql -dir $MIGRATIONS_DIR -seq $Arg
    }
}
