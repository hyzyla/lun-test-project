from flask import render_template, flash, request, abort, redirect

from catalog.models import Flat, Building
from .. import app
from .. import db
from ..forms import FlatForm


@app.route('/building/flats/<building_id>')
def show_flats_by_bulding(building_id):
    building = Building.query.get(building_id)
    if building is None:
        abort(404)
    return render_template('flats.html', building=building)


@app.route('/flat/delete/<building_id>/<flat_id>/all', methods=['GET', 'POST'])
def delete_all_flats(building_id, flat_id):
    item = Flat.query.get(flat_id)
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return redirect('/building/flats/{}'.format(building_id))


@app.route('/flat/delete/<building_id>/<flat_id>', methods=['GET', 'POST'])
def delete_flat(building_id, flat_id):
    flat = Flat.query.get(flat_id)
    building = Building.query.get(building_id)
    if flat is None or building is None:
        abort(404)
    flat.buildings.remove(building)
    db.session.commit()
    return redirect('/building/flats/{}'.format(building_id))


@app.route('/flat/new/<building_id>', methods=['GET', 'POST'])
@app.route('/flat/edit/<building_id>/<flat_id>/', methods=['GET', 'POST'])
def edit_flat(building_id, flat_id=None):
    building = Building.query.get(building_id)
    if building is None: abort(404)

    if flat_id is None:
        item = Flat()
        item.buildings.append(building)
    else:
        item = Flat.query.get(flat_id)
        if item is None:
            abort(404)

    form = FlatForm(obj=item)
    form.buildings.query = Building.query.filter(Building.group_id == building.group_id)

    if request.method == 'GET':
        return render_template('flat.html', form=form)

    if not form.validate_on_submit():
        flash("Всі поля є обов'язковими.")
        return render_template('flat.html', form=form)

    if not form.is_typical.data:
        form.buildings.data = [building,]

    form.populate_obj(item)
    db.session.add(item)
    db.session.commit()

    return redirect('/building/flats/{}'.format(building_id))
