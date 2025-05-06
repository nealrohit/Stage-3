# Indexes Report

This document describes all indexes on my database tables and the queries/reports they accelerate (Stage 3 Deliverable #1).

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
```

**Used in**
- edit/<int:item_id> route in app2.py (loads item for editing)
- /delete/<int:item_id> route in app2.py (fetches then deletes item)

## 2. Explicit Index on 'item.name'

**Index name**
- idx_item_name (created by me)

**Table & column**
- Table: item
- Column: name

**DDL statement**
```sql
CREATE INDEX IF NOT EXISTS idx_item_name
ON item(name);
```

**Supported query(ies)**  
```sql
-- Report of all items, optionally filtered by name
SELECT id, name
FROM item
WHERE name LIKE :search_pattern;
```

**Used in**
- /report route in app2.py (renders report.html)
- Future dynamic filtering on the report page (e.g., adding a text box to narrow by name)