from flask import render_template, flash, request, abort, redirect

from catalog.models import City
from .. import app
from .. import db
from ..forms import CityForm


@app.route('/city/delete/<city_id>', methods=['GET', 'POST'])
def delete_city(city_id):
    item = City.query.get(city_id)
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return redirect('/city/all')


@app.route('/city/new/', methods=['GET', 'POST'])
@app.route('/city/edit/<city_id>/', methods=['GET', 'POST'])
def edit_city(city_id=None):
    form = CityForm()
    if not city_id:
        item = City()
    else:
        item = City.query.get(city_id)
        if item is None:
            abort(404)
        form.name.data = item.name
        form.clarification.data = item.clarification

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Всі поля обов\'язкові')
        else:
            item.name = form.name.data
            item.clarification = form.clarification.data

            db.session.add(item)
            db.session.commit()

            return redirect('/city/all')

    return render_template('city.html', form=form)


@app.route('/city/all')
def all_cities():
    cities = City.query.all()
    return render_template('cities.html', cities=cities)
