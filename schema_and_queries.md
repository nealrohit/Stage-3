# Schema & Query Inventory

## Schema Inventory

```sql
CREATE TABLE item (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
```
## Query Inventory

1. Insertion (manage_items POST)

```py
new_item = Item(name=new_item_name)
db.session.add(new_item)
db.session.commit()
```