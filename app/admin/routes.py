from flask import Blueprint, render_template, url_for, flash
from werkzeug.utils import redirect
from ..db_models import Order, Item, db
from ..admin.forms import AddItemForm, OrderEditForm
from ..funcs import admin_only


admin = Blueprint("admin", __name__, url_prefix="/admin", static_folder="static", template_folder="templates")

@admin.route('/')
@admin_only
def dashboard():
    orders = Order.query.all()
    return render_template("admin/home.html", orders=orders)

@admin.route('/items')
@admin_only
def items():
    items = Item.query.all()
    return render_template("admin/items.html", items=items)

@admin.route('/add', methods=['POST', 'GET'])
@admin_only
def add():
    form = AddItemForm()

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        category = form.category.data
        details = form.details.data
        form.image.data.save('app/static/uploads/' + form.image.data.filename)
        image = url_for('static', filename=f'uploads/{form.image.data.filename}')
        price_id = form.price_id.data
        item = Item(name=name, price=price, category=category, details=details, image=image, price_id=price_id)
        db.session.add(item)
        db.session.commit()
        flash(f'{name} added successfully!','success')
        return redirect(url_for('admin.items'))
    return render_template("admin/add.html", form=form)

@admin.route('/edit/<string:type>/<int:id>', methods=['POST', 'GET'])
@admin_only
def edit(type, id):
    if type == "item":
        item = Item.query.get(id)
        form = AddItemForm(
            name = item.name,
            price = item.price,
            category = item.category,
            details = item.details,
            image = item.image,
            price_id = item.price_id,
        )
        if form.validate_on_submit():
            item.name = form.name.data
            item.price = form.price.data
            item.category = form.category.data
            item.details = form.details.data
            item.price_id = form.price_id.data
            form.image.data.save('app/static/uploads/' + form.image.data.filename)
            item.image = url_for('static', filename=f'uploads/{form.image.data.filename}')
            db.session.commit()
            return redirect(url_for('admin.items'))
    elif type == "order":
        order = Order.query.get(id)
        form = OrderEditForm(status = order.status)
        if form.validate_on_submit():
            order.status = form.status.data
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/add.html', form=form)

@admin.route('/delete/<int:id>')
@admin_only
def delete(id):
    to_delete = Item.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    flash(f'{to_delete.name} deleted successfully', 'error')
    return redirect(url_for('admin.items'))