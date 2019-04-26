from flask import Flask, render_template, url_for, request, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SelectField, IntegerField, RadioField, BooleanField, SelectMultipleField
from wtforms.validators import input_required, length, NumberRange

import os
import model

secret_key = os.urandom(24)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

Bootstrap(app)


# Class
class arpu_form(FlaskForm):
    age = IntegerField(
        'Age', validators=[input_required(), NumberRange(min=0, max=116, message='Age must be valid')])
    gender = RadioField(
        'Gender', default='1', choices=[('1', 'Male'), ('0', 'Female')])
    education = SelectField('Education', default='2', choices=[(
        '0', 'Primary'), ('1', 'Secondary'), ('2', 'University')])
    marital_status = SelectField('Marital Status', default='0', choices=[(
        '0', 'Single'), ('1', 'Married - no children'), ('2', 'Married - with children')])
    ses = SelectField('Socio Economic Status', default='7', choices=[(
        '0', 'E'), ('1', 'D'), ('2', 'C2'), ('3', 'C1'), ('4', 'B2'), ('5', 'B1'), ('6', 'A2'), ('7', 'A1')])
    status = SelectField('Status', default='2', choices=[(
        '0', 'Dormant'), ('1', 'Less'), ('2', 'Active')])
    bbm = BooleanField('BBM')
    fb = BooleanField('Facebook')
    ig = BooleanField('Instagram')
    line = BooleanField('Line')
    wa = BooleanField('Whatsapp')


# Routing
@app.route('/')
def index():
    form = arpu_form()
    return render_template('index.html', form=form)


@app.route('/preview')
def preview():
    cols = ['age', 'gender', 'education', 'marital_status',
            'ses', 'status', 'BBM', 'FB', 'IG', 'LINE', 'WA', 'arpu']
    df = model.read_with_column('static/data/clean.csv', cols)
    return render_template('preview.html', df_view=df)


# Predict Arpu
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = arpu_form()
    if form.validate_on_submit():
        # Get data
        age = form.age.data
        gender = int(form.gender.data)
        education = int(form.education.data)
        marital_status = int(form.marital_status.data)
        ses = int(form.ses.data)
        status = int(form.status.data)
        bbm = setcondition(form.bbm.data)
        fb = setcondition(form.fb.data)
        ig = setcondition(form.ig.data)
        line = setcondition(form.line.data)
        wa = setcondition(form.wa.data)

        # validate checkbox
        mark = bbm + fb + ig + line + wa

        if mark != 0:
            # Organize perdictor
            sample = [age, gender, education, marital_status,
                      ses, status, bbm, fb, ig, line, wa]
            cleaned_sample = model.cleaning(sample)

            # # Start Classifier
            rf = model.rf_prediction()
            result = rf.predict(cleaned_sample)

            return render_template('index.html', form=form, age=age, gender=gender, education=education, marital_status=marital_status, ses=ses, status=status, bbm=bbm, fb=fb, ig=ig, line=line, wa=wa, sample=sample, result=result)

        else:
            warn = 'at least one app checked!'
            return render_template('index.html', form=form, warn=warn)

    return render_template('index.html', form=form)


# Functions
def setcondition(x):
    if x == True:
        return 1
    else:
        return 0


if __name__ == '__main__':
    app.run(debug=True)
