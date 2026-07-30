-- ClaimVox database schema
-- This script runs on first container start (docker-entrypoint-initdb.d)

-- Create application user with minimum privilege
CREATE USER claimvox_app WITH PASSWORD 'claimvox_secret';

-- Schema migrations tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY
);

-- Predictions log: stores metadata only, NEVER the narrative
CREATE TABLE predictions (
    id TEXT PRIMARY KEY,
    predicted_class VARCHAR(100) NOT NULL,
    confidence DOUBLE PRECISION,
    review_required BOOLEAN NOT NULL DEFAULT TRUE,
    model_version VARCHAR(50) NOT NULL,
    taxonomy_version VARCHAR(10) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Feedback: human correction after prediction (same schema as SQLite version)
CREATE TABLE feedback_records (
    feedback_id TEXT PRIMARY KEY,
    prediction_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    taxonomy_version TEXT NOT NULL,
    suggested_class TEXT NOT NULL,
    reviewed_class TEXT,
    decision TEXT NOT NULL,
    purpose TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);

-- Indexes
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_predictions_model_version ON predictions(model_version);
CREATE INDEX idx_feedback_prediction_id ON feedback_records(prediction_id);

-- Record schema version
INSERT INTO schema_migrations(version) VALUES ('1');

-- Grant minimum privileges to app user (no DROP, no CREATE, no SUPERUSER)
GRANT CONNECT ON DATABASE claimvox TO claimvox_app;
GRANT USAGE ON SCHEMA public TO claimvox_app;
GRANT SELECT, INSERT, DELETE ON predictions TO claimvox_app;
GRANT SELECT, INSERT, DELETE ON feedback_records TO claimvox_app;
GRANT SELECT, INSERT ON schema_migrations TO claimvox_app;

-- Explicitly deny dangerous operations
REVOKE CREATE ON SCHEMA public FROM claimvox_app;

COMMENT ON TABLE predictions IS 'Prediction metadata only. Narratives are NEVER stored.';
COMMENT ON TABLE feedback_records IS 'Human corrections. Same schema as local SQLite for portability.';
