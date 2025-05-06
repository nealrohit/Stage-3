from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'item'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()
    print("Database tables created.")
    with db.engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_item_name ON item(name);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_item_name_ci ON item(name COLLATE NOCASE);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_item_name_id ON item(name, id);"))
        

@app.route('/')
def home():
    return redirect(url_for('manage_items'))

# Requirement 1
@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        new_item_name = request.form.get('name')
        if new_item_name:
            new_item = Item(name=new_item_name)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!')
            return redirect(url_for('manage_items'))
    items = Item.query.all()
    return render_template('items.html', items=items)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        db.session.commit()
        flash('Item updated successfully!')
        return redirect(url_for('manage_items'))
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!')
    return redirect(url_for('manage_items'))

@app.route('/batch_update', methods=['POST'])
def batch_update():
    updates = request.form.getlist('names')  # example list
    with db.session.begin():
        for idx, name in enumerate(updates, start=1):
            item = Item.query.get(idx)
            item.name = name
    flash('Batch update committed atomically!')
    return redirect(url_for('manage_items'))

#Requirement 2
@app.route('/report')
def report():
    term = request.args.get('q', '')
    if term:
        query = text("SELECT id, name FROM item WHERE name LIKE :patt")
        patt = f"%{term}%"
        with db.engine.connect() as conn:
            items = conn.execute(query, {"patt": patt}).fetchall()
    else:
        query = text("SELECT id, name FROM item")
        with db.engine.connect() as conn:
            items = conn.execute(query).fetchall()
    return render_template('report.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
