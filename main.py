from flask import Flask, render_template, redirect, url_for , url_for, flash, request,session

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import or_

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, CafeForm, UpdateDetailsForm, ResetPasswordForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.context_processor
def global_variables():
    users = User.query.all()

    user_dict = {user.id:user.username for user in users}
    return dict(users=users, user_dict=user_dict)

# LOGIN 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    session['next_url'] = request.url
    # Redirect the user to the login page if they are not authenticated
    flash('You must be logged in first','danger')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATING DATA BASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafe.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    class User(UserMixin,db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(200), nullable=False, unique=True)
        email = db.Column(db.String(300), nullable=False, unique=True)
        password = db.Column(db.String(300), nullable=False)
        cafes = relationship("Cafe", back_populates='user')

    class Cafe(db.Model):
        __tablename__ = 'cafes'
        id = db.Column(db.Integer, primary_key=True)

        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        user = relationship("User", back_populates="cafes")

        name = db.Column(db.String(250),nullable=False)
        map_url = db.Column(db.String(500), nullable=False)
        img_url = db.Column(db.String(500), nullable=False)
        location = db.Column(db.String(250), nullable=False)
        seats = db.Column(db.String(250), nullable=False)
        has_toilet = db.Column(db.Boolean, nullable=False)
        has_wifi = db.Column(db.Boolean, nullable=False)
        has_sockets = db.Column(db.Boolean, nullable=False)
        can_take_calls = db.Column(db.Boolean, nullable=False)
        coffee_price = db.Column(db.String(250), nullable=True)

    db.create_all()
    
# ---------------------------------------------------------------------------

# all Flask routes below
@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of cafes to display per page
    cafes = Cafe.query.order_by(Cafe.id.desc()).paginate(page=page, per_page=per_page)
    return render_template('index.html', cafes=cafes)


@app.route('/register/', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in. Please logout to Register a new account.', 'danger')
        return redirect(url_for('profile',username=current_user.username))
    
    register_form = RegisterForm()

    
    if register_form.validate_on_submit():
        entered_email = register_form.email.data
        if User.query.filter_by(email=register_form.email.data.lower()).first():
            flash('You have already signed up with that email.Log in instead','danger')
            return redirect(url_for('login'))
        
        elif User.query.filter_by(username=register_form.username.data.lower()).first():
            flash('There is user with the same name. Please enter another name','danger')
            # return redirect(url_for('register'))
            register_form.email.data = entered_email

        else:

            hashed_and_salted_password = generate_password_hash(
                password=register_form.password.data, 
                method="pbkdf2:sha256",salt_length=8)

            new_user = User(
                username=register_form.username.data.lower(),
                email=register_form.email.data.lower(),
                password=hashed_and_salted_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account was created , you can login now','primary')
            return redirect(url_for('login'))


    return render_template("register.html",form=register_form)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. Please logout to Login or to Register a new account.', 'danger')
        return redirect(url_for('profile',username=current_user.username))
    login_form = LoginForm()

    if login_form.validate_on_submit():
        entered_email = login_form.email.data
        entered_password = login_form.password.data
        user = User.query.filter_by(email=entered_email).first()

        if not user :
            flash(f'That email does not exist,please try again Or Register','danger')
            return redirect(url_for('login'))

        elif not check_password_hash(pwhash=user.password, password=entered_password):
            flash('The password is incorrect,please try again','danger')
            login_form.email.data = entered_email
            
        else:
            login_user(user)
            next_url = session.get('next_url')
            if next_url:
                # Clear the stored next_url from the session
                session.pop('next_url', None)
                # Redirect the user back to the original URL
                return redirect(next_url)
            return redirect(url_for('home'))
        
    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You logged out.You can login again','primary')
    return redirect(url_for('login'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of cafes to display per page
    cafes = Cafe.query.filter_by(user_id=user.id).order_by(Cafe.id.desc()).paginate(page=page, per_page=per_page)
    return render_template('profile.html',user=user, cafes=cafes)


@app.route('/search',methods=["GET"])
def search_by_location():
    location = request.args.get('location')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of cafes to display per page
    
    if location:
        # If a location is provided, perform the search
        searched_cafes = Cafe.query.filter(or_(Cafe.location == location, Cafe.location.ilike(f"%{location}%"))).paginate(page=page, per_page=per_page)
        if searched_cafes.total == 0:
            # If no cafes are found for the given location, redirect to the home page with a flash message
            flash(f"No Cafes were found in the given '{location}' location. Please ensure that you have added correct city name .", 'danger')

    else:
        # If no location is provided, show all cafes
        searched_cafes = db.session.query(Cafe).paginate(page=page, per_page=per_page)
        flash('No location added. Please first add location', 'danger')
        return redirect(url_for('home'))

    return render_template('index.html', searched_cafes=searched_cafes, location=location)
    

@app.route('/add', methods=["GET","POST"])
@login_required
def add_cafe():
    cafe_form = CafeForm()
    
    
    if cafe_form.validate_on_submit():
        new_cafe = Cafe(
            user_id = current_user.id,
            name = cafe_form.name.data,
            map_url = cafe_form.map_url.data,
            img_url = cafe_form.img_url.data,
            location = cafe_form.location.data.title(),
            seats = cafe_form.seats.data,
            has_toilet = bool(1 if cafe_form.has_toilet.data == '✅' else 0),
            has_wifi = bool(1 if cafe_form.has_wifi.data == '✅' else 0),
            has_sockets = bool(1 if cafe_form.has_sockets.data == '✅' else 0),
            can_take_calls = bool(1 if cafe_form.can_take_calls.data == '✅' else 0),
            coffee_price = cafe_form.coffee_price.data

        )
        db.session.add(new_cafe)
        db.session.commit()
        flash("New Cafe was added successfully",'success')
        return redirect(url_for('home'))
    
    elif request.method == "POST":
        flash('Form submission failed. Please check the entered URLs.', 'danger')

    return render_template('add.html', form=cafe_form)


@app.route('/update/cafe_id/<int:id>',methods=["GET","POST"])
@login_required
def update_cafe(id):
    cafe = Cafe.query.get(id)
    edit_form = CafeForm(obj=cafe)

    if current_user.id == cafe.user_id:
        if edit_form.validate_on_submit():
            cafe.name = edit_form.name.data
            cafe.map_url = edit_form.map_url.data
            cafe.img_url = edit_form.img_url.data
            cafe.location = edit_form.location.data.title()
            cafe.seats = edit_form.seats.data
            cafe.has_toilet = bool(1 if edit_form.has_toilet.data == '✅' else 0)
            cafe.has_wifi = bool(1 if edit_form.has_wifi.data == '✅' else 0)
            cafe.has_sockets = bool(1 if edit_form.has_sockets.data == '✅' else 0)
            cafe.can_take_calls = bool(1 if edit_form.can_take_calls.data == '✅' else 0)
            cafe.coffee_price = edit_form.coffee_price.data
            db.session.commit()
            flash('Cafe Was Updated Successfully','success')
            return redirect(url_for('profile',username=current_user.username))
    else:
        flash("You can only edit Your Cafes",'danger')
        return redirect(url_for('profile',username=current_user.username))


    return render_template('update.html',form=edit_form, cafe=cafe)


@app.route('/delete')
@login_required
def delete_cafe():
    cafe_id = request.args.get('id')
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash(f"Cafe '{cafe.name}' was deleted Successfully!",'danger')
    return redirect(url_for('profile',username=current_user.username))


@app.route('/update_details/<username>',methods=["GET","POST"])
@login_required
def update_details(username):
    user = User.query.filter_by(username=username).first_or_404()

    update_details_form = UpdateDetailsForm(obj=user)

    if current_user.id == user.id:
        if update_details_form.validate_on_submit():
            user.username = update_details_form.username.data
            user.email = update_details_form.email.data

            db.session.commit()
            flash('Your Details Were Updated Successfully','success')
            return redirect(url_for('profile',username=current_user.username))

    else:
        flash("You can only edit Your Details",'danger')
        return redirect(url_for('profile',username=current_user.username))
    
    return render_template('update_details.html', form=update_details_form)


@app.route('/reset_password/<username>',methods=['GET','POST'])
@login_required
def reset_password(username):
    user = User.query.filter_by(username=username).first_or_404()
    reset_password_form = ResetPasswordForm()

    if current_user.id == user.id:

        if reset_password_form.validate_on_submit():
            old_entered_password = reset_password_form.old_password.data
            if not check_password_hash(pwhash=user.password, password=old_entered_password):
                flash('The old password is incorrect,please try again','danger')
                return redirect(url_for('reset_password',username=user.username))

            else:
                hashed_and_salted_password = generate_password_hash(
                    password=reset_password_form.new_password.data, 
                    method="pbkdf2:sha256",salt_length=8)
                
                user.password = hashed_and_salted_password

                db.session.commit()
                logout_user()
                flash('Your Password Was Reset Successfully. Please now Log In','success')
                return redirect(url_for('login'))

    else:
        flash("You can only Reset Your Password",'danger')
        return redirect(url_for('profile',username=current_user.username))
    
    return render_template('reset_password.html', form=reset_password_form)



if __name__ == '__main__':
    app.run(debug=True)
