from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class ContactForm(FlaskForm):
    fullname=StringField("Enter your Fullname",validators=[DataRequired(),Length(min=7)])
    email=StringField("Enter Your Email", validators=[Email()])
    message=TextAreaField()
    submit=SubmitField('Submit')
    
class UserSignup(FlaskForm):
    g_firstname=StringField(validators=[DataRequired()])
    g_lastname=StringField(validators=[DataRequired()])
    g_email=StringField(validators=[DataRequired(),Email()])
    g_address=StringField(validators=[DataRequired()])
    g_pswd=PasswordField(validators=[DataRequired(),Length(min=5)])
    g_confirmpswd=PasswordField(validators=[DataRequired(),EqualTo("g_pswd")])
    Submit=SubmitField('Submit')