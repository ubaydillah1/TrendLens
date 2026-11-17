-- Create dual isolated databases for Go backend and Python AI backend
CREATE DATABASE trendlens_core;
CREATE DATABASE trendlens_ai;

-- Grant all privileges to the default user
GRANT ALL PRIVILEGES ON DATABASE trendlens_core TO postgres;
GRANT ALL PRIVILEGES ON DATABASE trendlens_ai TO postgres;
