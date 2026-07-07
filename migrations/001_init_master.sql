CREATE TABLE IF NOT EXISTS tenants (
    tenant_id VARCHAR(64) PRIMARY KEY,
    domain VARCHAR(255) UNIQUE NOT NULL,
    isolation_type VARCHAR(32) NOT NULL,
    schema_name VARCHAR(128),
    database_name VARCHAR(128),
    plan VARCHAR(64) NOT NULL DEFAULT 'standard',
    region VARCHAR(64) NOT NULL DEFAULT 'ap-south-1',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_user_profiles_tenant_id ON user_profiles(tenant_id);

CREATE TABLE IF NOT EXISTS claims (
    claim_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL,
    title VARCHAR(255) NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_claims_tenant_id ON claims(tenant_id);

CREATE TABLE IF NOT EXISTS notification_logs (
    notification_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL,
    channel VARCHAR(32) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'queued',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notification_logs_tenant_id ON notification_logs(tenant_id);

INSERT INTO tenants (
    tenant_id, domain, isolation_type, schema_name, database_name, plan, region, status
) VALUES
    ('tenant_acme', 'acme.example.com', 'schema', 'tenant_acme', NULL, 'pro', 'ap-south-1', 'active'),
    ('tenant_enterprise', 'enterprise.example.com', 'database', NULL, 'tenant_enterprise_db', 'enterprise', 'ap-south-1', 'active')
ON CONFLICT (tenant_id) DO NOTHING;
