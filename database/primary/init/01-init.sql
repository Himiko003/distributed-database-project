CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replication_dev';

CREATE TABLE IF NOT EXISTS inference_history (
    id BIGSERIAL PRIMARY KEY,
    input_data JSONB NOT NULL,
    predicted_class TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE inference_history TO app_user;
GRANT USAGE, SELECT ON SEQUENCE inference_history_id_seq TO app_user;
