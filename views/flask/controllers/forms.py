from wtforms import Form, HiddenField, StringField
from wtforms.validators import InputRequired, Length


class CodeForm(Form):
    company_code = StringField("company_code", validators=[
        InputRequired(), Length(4)
    ])