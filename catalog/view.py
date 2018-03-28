from flask import render_template, request
from sqlalchemy import or_, func

from catalog.forms import SearchForm
from catalog.models import Flat, City, Building, BuildingGroup
from . import app, db


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)

    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('index.html', form=form)

    city_name = form.city.data
    room_count = form.room_count.data

    query = db.session.query(Flat).join(Flat.buildings).join(Building.group).join(BuildingGroup.city)
    query = query.filter(or_(City.name.contains(city_name.capitalize()), City.name.contains(city_name.lower())))
    query = query.filter(Flat.room_count >= room_count)
    subquery = query.subquery()

    # Select minimal price in group of buildings
    grouped_subquery = db.session.query(
        Flat.id,
        func.min(Flat.price)
    ).join(Flat.buildings).join(subquery, Flat.id == subquery.c.id).group_by(Building.id).subquery()

    query = query.join(grouped_subquery, Flat.id == grouped_subquery.c.id)
    flats = query.order_by(Flat.full_price)

    return render_template('index.html', form=form, flats=flats)
