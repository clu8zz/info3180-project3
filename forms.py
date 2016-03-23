from wtforms import Form,TextField, PasswordField,validators

    

class LoginForm(Form):
	username=TextField('Username', [
    validators.Length(min=3, max=25),validators.Required()])

    
	password= PasswordField('New Password', [
        validators.Required()])