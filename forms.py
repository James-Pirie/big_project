from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Create_new_mod_form(FlaskForm):
    mod_name = StringField('Mod Name', validators=[DataRequired()])
    path = StringField("Documents File Path", validators=[DataRequired()])
    submit = SubmitField("Create Mod", validators=[DataRequired()])


class Create_New_Country(FlaskForm):
    country_name = StringField("Country Name", validators=[DataRequired()])
    country_name_fascist = StringField("Country Name Fascist", validators=[DataRequired()])
    country_name_democratic = StringField("Country Name Democratic", validators=[DataRequired()])
    country_name_communist = StringField("Country Name Communist", validators=[DataRequired()])
    country_name_neutral = StringField("Country Name Non-Aligned", validators=[DataRequired()])
    country_tag = StringField("Country Tag", validators=[DataRequired(), Length(min=3, max=3)])
    ruling_ideology = SelectField("Ruling Ideology", choices=[('ideology', 'Neutrality'),
                                                              ('ideology', 'Fascism'),
                                                              ('ideology', 'Communism'),
                                                              ('ideology', 'Democratic')],
                                  validators=[DataRequired()])
    culture = SelectField("Culture", choices=[('culture', 'Middle Eastern'),
                                                              ('culture', 'Eastern European'),
                                                              ('culture', 'South American'),
                                                              ('culture', 'Commonwealth'),
                                                              ('culture', 'Western European'),
                                                              ('culture', 'African'),
                                                              ('culture', 'Asian')],
                                  validators=[DataRequired()])
    submit = SubmitField("Confirm", validators=[DataRequired()])


class Set_Territory(FlaskForm):
    cored_owned = StringField("Owned Core Territory", validators=[DataRequired()])
    cored_not_owned = StringField("Claimed Core Territory")
    occupied_not_owned = StringField("Owned Occupied Territory")
    submit = SubmitField("Confirm", validators=[DataRequired()])


class Create_Leader(FlaskForm):
    Leader_Name = StringField("Leader Name", validators=[DataRequired()])

    submit = SubmitField("Confirm", validators=[DataRequired()])




