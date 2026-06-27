-- ==========================================================
-- Wealth Monitor
-- Seed Data v1.0
-- ==========================================================

-- ==========================================================
-- TRANSACTION TYPES
-- ==========================================================

INSERT INTO transaction_types (id, name)
VALUES
(0, 'Expense'),
(1, 'Income');

-- ==========================================================
-- SYSTEM CATEGORIES
-- ==========================================================

-- Expense Categories

INSERT INTO categories (
user_id,
name,
transaction_type,
is_system
)
VALUES
(NULL, 'Food',          0, TRUE),
(NULL, 'Travel',        0, TRUE),
(NULL, 'Shopping',      0, TRUE),
(NULL, 'Medical',       0, TRUE),
(NULL, 'Education',     0, TRUE),
(NULL, 'Bills',         0, TRUE),
(NULL, 'Entertainment', 0, TRUE),
(NULL, 'Others',        0, TRUE);

-- Income Categories

INSERT INTO categories (
user_id,
name,
transaction_type,
is_system
)
VALUES
(NULL, 'Salary',     1, TRUE),
(NULL, 'Business',   1, TRUE),
(NULL, 'Interest',   1, TRUE),
(NULL, 'Gift',       1, TRUE),
(NULL, 'Investment', 1, TRUE),
(NULL, 'Others',     1, TRUE);

-- ==========================================================
-- SYSTEM PARTIES
-- ==========================================================

INSERT INTO parties (
user_id,
name,
is_system
)
VALUES
(NULL, 'Cash', TRUE),
(NULL, 'Wallet', TRUE),
(NULL, 'Bank', TRUE),
(NULL, 'UPI', TRUE);