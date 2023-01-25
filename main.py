from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'muzik4813324'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)',validators=[URL(), DataRequired()])
    open = StringField('Opening time e.g. 8AM', validators=[DataRequired()])
    close = StringField('Closing time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=['☕️',"☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"])
    wifi_strength_rating = SelectField('Wifi Strength Rating', choices=['✘',"💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"])
    power_socket_availability = SelectField('Power Socket Availability', choices=['✘',"🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')


# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv',mode="a") as cafe_data:
            cafe_data.write(f"{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee_rating.data},{form.wifi_strength_rating.data},{form.power_socket_availability.data}")
        return redirect(url_for('cafes'))
    
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)



if __name__ == '__main__':
    app.run(debug=True)
