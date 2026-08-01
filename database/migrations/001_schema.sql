-- ==========================================================
-- Wealth Monitor
-- Database Schema v1.0
-- PostgreSQL
-- ==========================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ==========================================================
-- TRANSACTION TYPES
-- ==========================================================

CREATE TABLE transaction_types (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- ==========================================================
-- USERS
-- ==========================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- CATEGORIES
-- ==========================================================

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    name VARCHAR(100) NOT NULL,
    transaction_type SMALLINT NOT NULL,
    is_system BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_categories_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_categories_transaction_type
        FOREIGN KEY (transaction_type)
        REFERENCES transaction_types(id)
);

-- Prevent duplicate category names for the same owner/type
CREATE UNIQUE INDEX uq_categories
ON categories (
    COALESCE(user_id, '00000000-0000-0000-0000-000000000000'::uuid),
    name,
    transaction_type
);

-- ==========================================================
-- PARTIES
-- Payment channels in seed data: Cash, Wallet, Bank, UPI
-- ==========================================================

CREATE TABLE parties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    name VARCHAR(150) NOT NULL,
    is_system BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_parties_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Prevent duplicate party names for the same owner
CREATE UNIQUE INDEX uq_parties
ON parties (
    COALESCE(user_id, '00000000-0000-0000-0000-000000000000'::uuid),
    name
);

-- ==========================================================
-- TRANSACTIONS
-- ==========================================================

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    transaction_type SMALLINT NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    party_id UUID,
    category_id UUID,
    description VARCHAR(500),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transactions_party
        FOREIGN KEY (party_id)
        REFERENCES parties(id),

    CONSTRAINT fk_transactions_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id),

    CONSTRAINT fk_transactions_type
        FOREIGN KEY (transaction_type)
        REFERENCES transaction_types(id)
);

-- ==========================================================
-- TRANSACTION ATTACHMENTS
-- ==========================================================

CREATE TABLE transaction_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL,
    file_url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_attachments
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(id)
        ON DELETE CASCADE
);

-- ==========================================================
-- INDEXES
-- ==========================================================

CREATE INDEX idx_transactions_user
ON transactions(user_id);

CREATE INDEX idx_transactions_date
ON transactions(transaction_date);

CREATE INDEX idx_transactions_type
ON transactions(transaction_type);

CREATE INDEX idx_transactions_category
ON transactions(category_id);

CREATE INDEX idx_transactions_party
ON transactions(party_id);

CREATE INDEX idx_transactions_deleted
ON transactions(is_deleted);

CREATE INDEX idx_categories_user
ON categories(user_id);

CREATE INDEX idx_parties_user
ON parties(user_id);
