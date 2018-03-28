from flask import render_template, flash, request, abort, redirect

from catalog.forms import BuildingGroupForm
from catalog.models import BuildingGroup, City
from .. import app
from .. import db


@app.route('/group/buildings/<id>')
def show_buildings_by_group(id):
    group = BuildingGroup.query.get(id)
    if group is None:
        abort(404)
    return render_template('buildings.html', group=group)


@app.route('/group/delete/<id>', methods=['GET', 'POST'])
def delete_group(id):
    item = BuildingGroup.query.get(id)
    if item is None: abort(404)
    db.session.delete(item)
    db.session.commit()
    return redirect('/group/all')


@app.route('/group/new/', methods=['GET', 'POST'])
@app.route('/group/edit/<group_id>', methods=['GET', 'POST'])
def edit_group(group_id=None):

    if not group_id:
        item = BuildingGroup()
    else:
        item = BuildingGroup.query.get(group_id)
        if item is None: abort(404)

    form = BuildingGroupForm(obj=item)
    form.city_id.choices = [(g.id, g.name) for g in City.query.all()]

    if request.method == 'GET':
        return render_template('group.html', form=form)

    if not form.validate_on_submit():
        flash("Всі поля є обов'язковоми.")
        return render_template('group.html', form=form)

    form.populate_obj(item)
    db.session.add(item)
    db.session.commit()
    return redirect('/group/all')


@app.route('/group/all')
def show_cities():
    return render_template('groups.html', groups=BuildingGroup.query.all())
