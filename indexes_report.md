# Indexes Report

This report lists each index created to optimize our Flask app’s queries (Stage 3, Deliverable #1).

-- Index on item.name to speed up lookups and LIKE searches
CREATE INDEX idx_item_name ON item(name);

### idx_item_name
- **Table:** `item`
- **Column:** `name`
- **Supported Query:**  
  ```sql
  SELECT id, name
  FROM item
  WHERE name LIKE ?;