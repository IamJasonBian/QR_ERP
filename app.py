from flask import Flask, render_template, url_for, request, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'



class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
    @app.route("/form", methods=['GET', 'POST'])
    def form():
        form = ReusableForm(request.form)
    
        print (form.errors)
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            print (name, " ", email, " ", password)
    
        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('form.html', form=form)



@app.route("/index")
def hello():
    print("Handling request to home page.")
    
    import pyodbc 
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = 'qrinventory.database.windows.net' 
    database = 'Main' 
    username = 'qr@umich.edu@qrinventory' 
    password = 'ScrambledEggs73' 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    #Sample select query
    cursor.execute("SELECT * from dbo.Components;") 
    row = cursor.fetchone() 
    while row: 
        print(row[0])
        row = cursor.fetchone()
                
    return "index"

@app.route("/increment_component")
def increment_component():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Main', user=user, posts=posts)

@app.route("/build")
def build():
    return 'build'

@app.route("/send_inventory")
def send_inventory():
    return 'send_inventory'

with app.test_request_context():
    print(url_for('increment_component'))
    print(url_for('build'))
    print(url_for('send_inventory'))


if __name__ == "__main__":
    app.run()