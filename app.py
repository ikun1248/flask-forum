from flask import Flask,request,render_template,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from blueprints.profile import bp as profile_bp
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate=Migrate(app,db)
csrf=CSRFProtect(app)
csrf.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)
app.register_blueprint(profile_bp)

@app.before_request
def before_request():
    user_id=session.get('user_id')
    if user_id:
        user=UserModel.query.get(user_id)
        setattr(g,'user',user)
    else:
        setattr(g,'user',None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)