from flask import render_template, flash, request, abort, redirect

from catalog.models import BuildingGroup, Building
from .. import app
from .. import db
from ..forms import BuildingForm


@app.route('/building/flats/<building_id>')
def show_flats_by_building(building_id):
    building = Building.query.get(building_id)
    if building is None: abort(404)
    return render_template('flats.html', building=building)


@app.route('/building/delete/<building_id>', methods=['GET', 'POST'])
def delete_building(building_id):
    item = Building.query.get(building_id)
    if item is None: abort(404)

    # save building group id for redirecting to page with buildings of this group
    group_id = item.group_id

    db.session.delete(item)
    db.session.commit()
    return redirect('/group/buildings/{}'.format(group_id))


@app.route('/building/new/<group_id>', methods=['GET', 'POST'])
@app.route('/building/edit/<building_id>/', methods=['GET', 'POST'])
def edit_building(building_id=None, group_id=None):

    if building_id is None:
        item = Building()
        if BuildingGroup.query.get(group_id) is None:
            abort(404)
        item.group_id = group_id
    else:
        item = Building.query.get(building_id)
        if item is None:
            abort(404)

    form = BuildingForm(obj=item)

    if request.method == 'GET':
        return render_template('building.html', form=form)

    if not form.validate_on_submit():
        flash("Всі поля є обов'язковими.")
        return render_template('building.html', form=form)

    form.populate_obj(item)
    db.session.add(item)
    db.session.commit()

    return redirect('/group/buildings/{}'.format(item.group_id))
