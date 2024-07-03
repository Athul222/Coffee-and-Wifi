from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label="Cafe location on Google Maps", validators=[URL(require_tld=True, message="Invalid URL")])
    open_time = StringField(label="Openning Time e.g. 8AM", validators=[DataRequired()])
    close_time = StringField(label="Closing Time e.g. 5:30PM", validators=[DataRequired()])
    rating_choices = [i * "☕️" for i in range(1, 6)]
    rating = SelectField(label="Coffee Rating", choices=rating_choices, validators=[DataRequired()])
    wifi_rating_choices = [i * "💪" for i in range(1, 6)]
    wifi_rating_choices.insert(0, "✘")
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=wifi_rating_choices, validators=[DataRequired()])
    power_rating_choices = [i * "🔌" for i in range(1, 6)]
    power_rating_choices.insert(0,'✘')
    power = SelectField(label="Power Socket Availability", choices=power_rating_choices, validators=[DataRequired(DataRequired())])
    submit = SubmitField(label='Submit')

# home route
@app.route("/")
def home():
    return render_template("index.html")


# add route
@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        data = f"{form.cafe.data},{form.location.data},{form.open_time.data},{form.close_time.data},{form.rating.data},{form.wifi_rating.data},{form.power.data}"
        with open('cafe-data.csv', mode='a', encoding='utf-8') as file:
            file.write(f"\n{data}")
            
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


# cafes route
@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
