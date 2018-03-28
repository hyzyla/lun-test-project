from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired


class CityForm(FlaskForm):
    name = StringField('Назва', validators=[InputRequired(), ])
    clarification = StringField('Уточнення', validators=[])


class BuildingGroupForm(FlaskForm):
    name = StringField('Назва:', validators=[InputRequired(), ])
    city_id = SelectField("", validators=[InputRequired(), ], coerce=int)


class BuildingForm(FlaskForm):
    name = StringField('Назва', validators=[InputRequired(), ])


class FlatForm(FlaskForm):
    room_count = IntegerField('Кількість кімнат:', validators=[InputRequired(), ])
    level_count = IntegerField('Кількість рівнів/поверхів:', validators=[InputRequired(), ])
    is_studio = BooleanField('Студія:', validators=[])
    total_area = IntegerField('Загальна площа (кв.м):', validators=[InputRequired(), ])
    display_per_smeter = BooleanField("Ціна за квадратний метр", validators=[])
    price = IntegerField('Ціна (грн):', validators=[InputRequired(), ])
    buildings = QuerySelectMultipleField(get_label=lambda b: str(b),
                                         get_pk=lambda b: b.id)
    is_typical = BooleanField('Типова квартира', validators=[])


class SearchForm(FlaskForm):
    city = StringField('Назва міста')
    room_count = IntegerField('Мінімальна ціна')
