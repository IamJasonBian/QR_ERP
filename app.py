from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def hello():
    print("Handling request to home page.")
    
    import pandas as pd
    import pyodbc
    
    
    server = 'qrinventory.database.windows.net'
    database = 'Main'
    username = 'qr@umich.edu@qrinventory'
    password = 'Scrambledeggs73'   
    driver= '{ODBC Driver 17 for SQL Server}'
    
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from dbo.Build")
            row = cursor.fetchone()
            
            rows_list = []
    
                               
            while row:
                
                dict1 = {}
                print (str(row[0]) + " " + str(row[1]))
                dict1.update({"ITEM": str(row[0]) + " " + str(row[1])})
                
                rows_list.append(dict1)
                
                row = cursor.fetchone()
                
    df = pd.DataFrame(rows_list)
                
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('https://qrtest123315123.azurewebsites.net/')
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    
    return render_template("index.html", data = db, img=img)


