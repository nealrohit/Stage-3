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
2. Retrieval for UI (manage_items GET)
```py
items = Item.query.all()
```
3. Fetch single item for editing (edit_item GET)
```py
item = Item.query.get_or_404(item_id)
```
4. Update item (edit_item POST)
```py
item.name = request.form.get('name')
db.session.commit()
```
5. Delete item (delete_item POST)
```py
item = Item.query.get_or_404(item_id)
db.session.delete(item)
db.session.commit()
```
6. Batch update (batch_update POST)
```py
updates = request.form.getlist('names')
with db.session.begin():
    for idx, name in enumerate(updates, start=1):
        item = Item.query.get(idx)
        item.name = name
```
7. Report all items (report GET, unfiltered)
```py
query = text("SELECT id, name FROM item")
with db.engine.connect() as conn:
    items = conn.execute(query).fetchall()
```
8. Filtered report (report GET, with search)
```py
term = request.args.get('q', '')
query = text("SELECT id, name FROM item WHERE name LIKE :patt")
patt = f"%{term}%"
with db.engine.connect() as conn:
    items = conn.execute(query, {"patt": patt}).fetchall()
```
