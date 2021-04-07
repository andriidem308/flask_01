"""Flask project."""

from faker import Faker

from flask import Flask, jsonify, redirect, render_template, request, url_for

from flask_sqlalchemy import SQLAlchemy

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    """Model of User."""

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        """Create user."""
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Represent user."""
        return '<User %r>' % self.name


@app.route('/')
def home():
    """Route to homepage."""
    return 'Main Page'


@app.route('/users/all')
def users_all():
    """Route to all users."""
    tab = User.query.all()
    users = [
        dict(id=usr.user_id, name=usr.name, email=usr.email)
        for usr in tab
    ]
    db.session.commit()
    return jsonify(users)


@app.route('/users/gen')
def users_gen():
    """Route to generator of users."""
    usr = User(name=fake.name(), email=fake.email())
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route('/users/delete-all')
def users_del_all():
    """Route for delete all users."""
    db.session.query(User).delete()
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route('/users/count')
def users_count():
    """Route to count users."""
    tab = User.query.count()
    if tab is None:
        return ValueError('Could not count users')
    return jsonify({'count': tab})


@app.route('/users/add', methods=['GET', 'POST'])
def users_add():
    """Route to add users."""
    if request.method == 'GET':
        return render_template('user_add.html')
    else:
        name = request.form['user_name']
        email = request.form['email']

    db.session.add(User(name=name, email=email))
    db.session.commit()
    return redirect(url_for('users_all'))


if __name__ == '__main__':
    app.run()
