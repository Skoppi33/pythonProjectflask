from flask import Flask, render_template, url_for, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeck.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

# with app.app_context():
   # db.create_all()

def is_user_registered(login):
    """Проверяет, существует ли пользователь с данным логином."""
    user = Post.query.filter_by(login=login).first()
    return user is not None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password1 = request.form['password1']

        if password1 == password:
             if is_user_registered(login):
                 return "Пользователь с таким именем уже существует. Выберите другое имя"
             else:
                post = Post(login=login, password=password)
                try:
                    db.session.add(post)
                    db.session.commit()
                    # Сохраняем логин пользователя в куки
                    resp = make_response(redirect('/'))
                    resp.set_cookie('login', login)
                    return resp
                except Exception:
                    return "Непредвиденная ошибка. Попробуйте позже."

        else:
            return 'Пароли не одинаковы'
    else:
        return render_template("registr.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/video')
def video():
    return render_template("video.html")

@app.route('/spravochik')
def spravochik():
    return render_template("spravochik.html")


if __name__ == "__main__":
    app.run(debug=True)