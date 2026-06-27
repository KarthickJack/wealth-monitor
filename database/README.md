# Wealth Monitor Database

## Overview

The Wealth Monitor database is built on PostgreSQL and is designed with simplicity, scalability, and teaching in mind.

The design follows three core principles:

* Normalize data where appropriate.
* Keep business rules in the backend.
* Keep data integrity in the database.

---

## Database Structure

```
database/
│
├── migrations/
│   ├── 001_schema.sql
│   └── 002_seed.sql
│
├── diagrams/
│
└── README.md
```

---

## Tables

| Table                   | Purpose                                               |
| ----------------------- | ----------------------------------------------------- |
| transaction_types       | Defines supported transaction types (Expense, Income) |
| users                   | Application users                                     |
| categories              | System and user-defined transaction categories        |
| parties                 | System and user-defined transaction parties           |
| transactions            | Income and expense records                            |
| transaction_attachments | Receipts and supporting documents                     |

---

## Design Decisions

### One Transactions Table

Income and Expense are stored in a single `transactions` table.

Advantages:

* Simpler queries
* Easier reporting
* Future support for Transfer, Investment, Loan, etc.

---

### One Parties Table

Instead of maintaining separate Payer and Payee tables, all business entities are stored in a single `parties` table.

A party may participate in both income and expense transactions.

---

### Categories

Categories support both:

* System categories
* User-created categories

System categories have:

```
user_id = NULL
is_system = TRUE
```

User categories have:

```
user_id = <User UUID>
is_system = FALSE
```

Business rules preventing duplicate category names are enforced in the backend.

---

### Soft Delete

Transactions are never physically deleted.

Instead:

```
is_deleted = TRUE
```

This preserves history and supports future auditing.

---

## Validation Strategy

| Layer    | Responsibility                       |
| -------- | ------------------------------------ |
| Frontend | User experience and input validation |
| Backend  | Business rules                       |
| Database | Data integrity                       |

---

## Migration Order

Execute migrations in order:

```
001_schema.sql

↓

002_seed.sql
```

---

## Future Enhancements

Planned for future versions:

* Budgets
* Recurring Transactions
* Tags
* Accounts
* Multi-Currency
* Audit Logs

Version: 1.0