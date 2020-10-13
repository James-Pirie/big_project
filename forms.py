from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField
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

    ruling_ideology = SelectField("Ruling Ideology", choices=[('neutrality', 'Neutrality'),
                                                              ('fascism', 'Fascism'),
                                                              ('communism', 'Communism'),
                                                              ('democratic', 'Democratic')],
                                  validators=[DataRequired()])
    culture = SelectField("Culture", choices=[('middle_eastern_', 'Middle Eastern'),
                                                              ('eastern_european_', 'Eastern European'),
                                                              ('southamerican_', 'South American'),
                                                              ('commonwealth_', 'Commonwealth'),
                                                              ('western_european_', 'Western European'),
                                                              ('african_', 'African'),
                                                              ('asian_', 'Asian')],
                                  validators=[DataRequired()])
    RGB_color = StringField("Red Color Value", validators=[DataRequired()])
    submit = SubmitField("Confirm", validators=[DataRequired()])


class Set_Territory(FlaskForm):
    cored_owned = StringField("Owned Core Territory", validators=[DataRequired()])
    nations_capital = StringField("Set Capital", validators=[Length(min=1, max=3)])
    cored_not_owned = StringField("Claimed Core Territory")
    occupied_not_owned = StringField("Owned Occupied Territory")
    submit = SubmitField("Confirm", validators=[DataRequired()])


class Create_Leader(FlaskForm):
    Leader_Name_d = StringField("Democratic Leader Name", validators=[DataRequired()])
    Leader_Name_f = StringField("Fascist Leader Name", validators=[DataRequired()])
    Leader_Name_c = StringField("Communist Leader Name", validators=[DataRequired()])
    Leader_Name_n = StringField("Non-Aligned Leader Name", validators=[DataRequired()])
    submit = SubmitField("Confirm", validators=[DataRequired()])




