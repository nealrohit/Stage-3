# Indexes Report

This document describes all indexes on our database tables and the queries/reports they accelerate (Stage 3 Deliverable #1).

---

## 1. Primary‑Key Index on `item.id`

**Index name**  
- `sqlite_autoindex_item_1` (created automatically by SQLite)

**Table & column**  
- **Table:** `item`  
- **Column:** `id`

**Supported query(ies)**  
```sql
-- Lookup a single item by ID (used in edit & delete operations)
SELECT id, name
FROM item
WHERE id = :item_id;