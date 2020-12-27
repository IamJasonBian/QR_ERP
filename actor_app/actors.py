from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


from modules import get_names, get_actor, get_id
import pyodbc
import json
import qrcode

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    
    #QR Codes goes here
    
    print("Updated")
    
    #Write SQL database into json location
    server = 'qrinventory.database.windows.net' 
    database = 'Main' 
    username = 'qr@umich.edu@qrinventory' 
    password = 'ScrambledEggs73' 
    
  
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute("Select * from dbo.Build")
    columns = [column[0] for column in cursor.description]
    
    
    #Write local validation code
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    print(results)
    
    def line_prepender(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(line.rstrip('\r') + content)
    
    with open("build_data.py", "w") as write_file:
        json.dump(results, write_file)
        
    line_prepender("build_data.py", "DB = ")
    
    
    
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute("Select * from dbo.Components")
    columns = [column[0] for column in cursor.description]
    
    
    #Write local validation code
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    print(results)
    
    def line_prepender(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(line.rstrip('\r') + content)
    
    with open("component_data.py", "w") as write_file:
        json.dump(results, write_file)
        
    line_prepender("component_data.py", "DB = ")
    
   
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute("Select Name from dbo.Build")
    selection = []
    for row in cursor.fetchall():
        selection.append(row[0])
    
    
    selection_2 = []
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute("Select Name from dbo.Components")
    for row in cursor.fetchall():
        selection_2.append(row[0])
        
    
    columns = selection + selection_2
    print(columns)
   
   

    from build_data import DB as Build_DB
    from component_data import DB as Comp_DB
    
    names = columns

    
    class NameForm(FlaskForm):
        name = SelectField(label = 'Possible Builds or Components are listed below', choices=columns)
        submit = SubmitField('Submit')
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        
        if name in names:
            return redirect( url_for('module', name=name))
        else:
            message = "Build or Component does not exist in database."
    return render_template('index.html', names=names, form=form, message=message)

@app.route('/module/<name>')
def module(name, type):
    from build_data import DB as Build_DB
    from component_data import DB as Comp_DB
    
    # run function to get actor data based on the id in the path
    
    img_base = "/static/"
    
    if(type == "Component"):
        id, name, qr = get_actor(Comp_DB, name, "Component")
    elif(type == "Inventory"):
        id, name, qr = get_actor(Build_DB, name, "Inventory")
    elif name == "Unknown":
        
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', id=id, name=name, qr= img_base + qr)
    

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
