from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from modules import get_names, get_actor, get_id
import pyodbc
import json

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Possible Components are listed below', validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    

      
    #Write SQL database into json location
    server = 'qrinventory.database.windows.net' 
    database = 'Main' 
    username = 'qr@umich.edu@qrinventory' 
    password = 'ScrambledEggs73' 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute("Select * from dbo.Build")
    columns = [column[0] for column in cursor.description]
    print(columns)
    
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    print(results)
    
    def line_prepender(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(line.rstrip('\r') + content)
    
    with open("sql_data.py", "w") as write_file:
        json.dump(results, write_file)
        
    line_prepender("sql_data.py", "DB = ")

    from sql_data import DB
    
    names = get_names(DB)
    
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = get_id(DB, name)
            # redirect the browser to another route and template
            return redirect( url_for('module', id=id) )
        else:
            message = "Build or Component does not exist in database."
    return render_template('index.html', names=names, form=form, message=message)

@app.route('/module/<id>')
def module(id):
    from sql_data import DB
    # run function to get actor data based on the id in the path
    id, name, qr = get_actor(DB, id)
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', id=id, name=name, qr=qr)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
