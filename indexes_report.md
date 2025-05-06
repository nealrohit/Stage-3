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
- `edit/<int:item_id>` route in app2.py (loads item for editing)
- `/delete/<int:item_id>` route in app2.py (fetches then deletes item)

## 2. Explicit Index on `item.name`

**Index name**
- `idx_item_name` (created by me)

**Table & column**  
- **Table:** `item`  
- **Column:** `name`

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
- `/report` route in app2.py (renders report.html)
- Future dynamic filtering on the report page (e.g., adding a text box to narrow by name)

## 3. Case‑Insensitive Index on `item.name`

**Index name**
- `idx_item_name_ci` 

**Table & column**  
- **Table:** `item`  
- **Column:** `name COLLATE NOCASE`

**DDL statement**
```sql
CREATE INDEX IF NOT EXISTS idx_item_name_ci
ON item(name COLLATE NOCASE);
```

**Supported query(ies)**  
```sql
-- Case‑insensitive name search
SELECT id, name
FROM item
WHERE name LIKE :pattern COLLATE NOCASE;
```

**Used in**
- Potential `/report?search=…` feature that ignores case differences

## 4. Covering Index on `(name, id)`

**Index name**
- `idx_item_name_id` 

**Table & column**  
- **Table:** `item`  
- **Column:** `(name, id)`

**DDL statement**
```sql
CREATE INDEX IF NOT EXISTS idx_item_name_id
ON item(name, id);
```

**Supported query(ies)**  
```sql
-- Covering index for name‑based report
SELECT id, name
FROM item
WHERE name LIKE :pattern;
```

**Benefit**
- Satisfies the query entirely from the index without touching the table (covering index)

## 5. Full‑Text Search Virtual Table

**FTS table name**
- `item_fts` (FTS5 virtual table)

**Schema**
```sql
CREATE VIRTUAL TABLE IF NOT EXISTS item_fts
USING fts5(name);
```

**Setup query**
```sql
INSERT INTO item_fts(rowid, name)
SELECT id, name
FROM item;
```

**Supported query(ies)**  
```sql
-- Prefix/full-text search on item names
SELECT rowid AS id, name
FROM item_fts
WHERE item_fts MATCH 'app*';
```

**Used in**
- A future `/search` endpoint leveraging FTS for advanced text matching