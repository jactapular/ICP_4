from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from mysql.connector import MySQLConnection

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])


def send():
    conn = MySQLConnection( host = '10.0.10.220',
                                database = 'ICP',
                                user = 'tran',
                                password = 'GreenX0123')
    curs = conn.cursor()

    name = 'test send data 2'
    custID = 1

    add_proj = ("CALL addProj(%s, %s)")

    data = (name, custID)

    curs.execute(add_proj, data)

    conn.commit()

    curs.close()
    conn.close()
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        print name
 
        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
            send()
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('./hello.html', form=form)
 
if __name__ == "__main__":
    app.run()