from flask_mail import Mail, Message
from flask import current_app

mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mctestersontesty14@gmail.com'
app.config['MAIL_PASSWORD'] = 'yeehaw21'
mail.init_app(app)
