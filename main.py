from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
import subprocess
import requests
from datetime import date
app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

link = {x: x for x in ["location", "product", "movement"]}
link["index"] = '/'

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    prod_id = request.form['prod_id']
    prod_quantity = request.form['prod_quantity']
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""SELECT stock from productss WHERE productId= ? """, (prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            inventory_stock = cur.fetchall()
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    print(inventory_stock)
    order_quant=prod_quantity
    prod_quantity=int(prod_quantity)+int(inventory_stock[0][0])
    # print(inventory_stock)
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""UPDATE productss SET stock = ?  WHERE productId= ? """, (prod_quantity,prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    dateToday = str(date.today())
    dateToday=dateToday.replace("-","")
    order_id=dateToday+"LI"+str(prod_id)
    print(dateToday,order_id)
    # order_quant
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""INSERT into ordersss (productId, orderId, orderPlacedOn, productQuantity) VALUES (?, ?, ?, ?)""", (prod_id,order_id,dateToday,order_quant))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    print(msg)
    # return "Hello"
    return redirect(url_for('dispdetails'))


@app.route("/")
def root():
    # return redirect(url_for('dispdetails'))
    return render_template('homepage.html')

@app.route("/location")
def location():
    return redirect(url_for('dispdetails'))
@app.route("/product")
def product():
    return redirect(url_for('dispdetails'))
@app.route("/movement")
def movement():
    return redirect(url_for('displayOrders'))


@app.route("/dispdetails")
def dispdetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, stock FROM productss")
        available = cur.fetchall()
    conn.close()
    return render_template('product.html',link=link, products=available)

@app.route("/futureDemand")
def futureDemand():
    pid = request.args.get('prod_id')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, stock FROM productss WHERE productId=?",pid)
        available = cur.fetchall()
    conn.close()
    os.system('python sales_prediction.py')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT stock FROM futuresales WHERE productId=?",pid)
        expectedDemand = cur.fetchall()
    conn.close()
    output=[]
    orderamount=expectedDemand[0][0]-available[0][2]
    output.append(tuple([available[0][0],available[0][1],available[0][2],expectedDemand[0][0],orderamount]))
    print(output)
    pname=available[0][1]
    if orderamount>10000:
        url = "https://www.fast2sms.com/dev/bulk"           
        msg="Available Stock for " +str(pname)+" in our inventory is low..Check the App to place order.."
        querystring = {"authorization":"2ndrfwRFhotlDvcy3P8mbKIWxGsq5j0V1gO4iTAQMLUJzYCe9ZsR0OdaCYXHPIm3kg9Lnufv5r2JTDWU","sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":"9834576425"}
        headers = {
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

    return render_template('product2.html',link=link, products=output)

@app.route("/futureDemand2")
def futureDemand2():
    pid = request.args.get('prod_id')
    # pid=1
    today = str(date.today())
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('''SELECT updatedOn,stock from futuresales2 where productId= ?''', (pid,))
            lastUpdated = cur.fetchall()
            msg="added successfully"
            print(lastUpdated[0][0])
        except:
            print("Some Error Occured")
    conn.close()
    if(lastUpdated):
        if (lastUpdated[0][0]!=today):
            stt='python sales_prediction2.py '+str(pid)
            os.system(stt)
    else:
        stt='python sales_prediction2.py '+str(pid)
        os.system(stt)
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, stock FROM productss WHERE productId=?",(pid,))
        available = cur.fetchall()
        print("Available")
        print(available)
    conn.close()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT stock FROM futuresales2 WHERE productId=?",(pid,))
        expectedDemand = cur.fetchall()
        print("expectedDemand")
        print(expectedDemand)
    conn.close()
    output=[]
    orderamount=expectedDemand[0][0]-available[0][2]
    output.append(tuple([available[0][0],available[0][1],available[0][2],expectedDemand[0][0],orderamount]))
    print(output)
    pname=available[0][1]
    if orderamount>10000:
        url = "https://www.fast2sms.com/dev/bulk"           
        msg="Available Stock for " +str(pname)+" in our inventory is low..Check the App to place order.."
        querystring = {"authorization":"2ndrfwRFhotlDvcy3P8mbKIWxGsq5j0V1gO4iTAQMLUJzYCe9ZsR0OdaCYXHPIm3kg9Lnufv5r2JTDWU","sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":"9834576425"}
        headers = {
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
    saved_img_name=str(pid)+".jpg"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], saved_img_name)
    # full_filename="static/uploads/site_icon.png"
    print(full_filename)

    return render_template('product2.html',link=link, products=output, user_image = full_filename)


@app.route("/trackOrder")
def trackOrder():
    orderid = request.args.get('order_id')
    # pid=1
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId,orderPlacedOn FROM ordersss WHERE orderId=?",(orderid,))
        resultData = cur.fetchall()
        print("resultData")
        print(resultData)
    conn.close()
    output=[]
    if resultData[0][0]==1 or resultData[0][0]==3:
        Location="Delhi"
    else:
        Location="Bengaluru"
    if(resultData[0][0]%4==0):
        p_loc="chn"
    elif(resultData[0][0]%4==1):
        p_loc="klk"
    elif(resultData[0][0]%4==2):
        p_loc="blr"
    else:
        p_loc="dl"
    saved_img_name=str(p_loc)+".png"
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], saved_img_name)
    # full_filename="static/uploads/site_icon.png"
    print(full_filename)
    return render_template('track_shipment.html',link=link, orders_id=orderid,locn= Location, user_image = full_filename)


@app.route("/displayOrders")
def displayOrders():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT orderId,productId,orderPlacedOn,productQuantity FROM ordersss")
        orderList = cur.fetchall()
        print("orderList")
        print(orderList)
    conn.close()
    return render_template('orders.html',link=link, products=orderList)





@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['prod_name']
        price = 50000
        stock = int(request.form['prod_quantity'])
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO productss (name, price, stock) VALUES (?, ?, ?)''', (name, price,  stock))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/enterform")
def enteform():
    return render_template('enter.html', error='')

@app.route("/enter", methods = ['POST', 'GET'])
def enter():
    email = request.form['email']
    password = request.form['password']
    if email=='admin@gmail.com' and password=='admin':
        session['email'] = email
        return redirect(url_for('dispdetails'))
    else:
        return render_template('enter.html', error='')

# @app.route("/login", methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         if is_valid(email, password):
#             session['email'] = email
#             return redirect(url_for('root'))
#         else:
#             error = 'Invalid UserId / Password'
#             return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

# def is_valid(email, password):
#     con = sqlite3.connect('database.db')
#     cur = con.cursor()
#     cur.execute('SELECT email, password FROM users')
#     data = cur.fetchall()
#     for row in data:
#         if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
#             return True
#     return False


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/lowstock")
def lowstock():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, stock FROM productss ORDER BY stock ASC LIMIT 5")
        available = cur.fetchall()
    conn.close()
    return render_template('low_stock.html',link=link, products=available)

@app.route("/buy")
def buy():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, stock FROM productss")
        available = cur.fetchall()
    conn.close()
    return render_template('buyItem.html',link=link, products=available)

def purchase(prod_id,prod_quantity):
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""SELECT stock from productss WHERE productId= ? """, (prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            inventory_stock = cur.fetchall()
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    print(inventory_stock)
    order_quant=int(prod_quantity)-int(inventory_stock[0][0])
    # print(inventory_stock)
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""UPDATE productss SET stock = ?  WHERE productId= ? """, (prod_quantity,prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    dateToday = str(date.today())
    dateToday=dateToday.replace("-","")
    order_id=dateToday+"LI"+str(prod_id)
    print(dateToday,order_id)
    # order_quant
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""INSERT into ordersss (productId, orderId, orderPlacedOn, productQuantity) VALUES (?, ?, ?, ?)""", (prod_id,order_id,dateToday,order_quant))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    print(msg)
    # return "Hello"
    return redirect(url_for('dispdetails'))

@app.route('/buyItem', methods=['POST', 'GET'])
def buyItem():
    prod_id = request.form['prod_id']
    prod_quantity = request.form['prod_quantity']
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""SELECT stock,name from productss WHERE productId= ? """, (prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            inventory_stock = cur.fetchall()
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    print(inventory_stock)
    order_quant=int(inventory_stock[0][0])-int(prod_quantity)
    # print(inventory_stock)
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("""UPDATE productss SET stock = ?  WHERE productId= ? """, (order_quant,prod_id))
            # cur.execute('''INSERT INTO orderss (productId, productQuantity) VALUES (?, ?)''', (prod_id, prod_quantity))
            conn.commit()
            msg="added successfully"
        except:
            msg="error occured"
            conn.rollback()
    conn.close()
    pname=inventory_stock[0][1]
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT stock FROM futuresales2 WHERE productId=?",(prod_id,))
        expectedDemand = cur.fetchall()
        print("expectedDemand")
        print(expectedDemand)
    conn.close()
    orderamount=expectedDemand[0][0]
    print(orderamount)
    if order_quant<500:
        url = "https://www.fast2sms.com/dev/bulk"           
        msg="Available Stock for " +str(pname)+" in our inventory is low..Auto Order Placed...Check the App.."
        querystring = {"authorization":"2ndrfwRFhotlDvcy3P8mbKIWxGsq5j0V1gO4iTAQMLUJzYCe9ZsR0OdaCYXHPIm3kg9Lnufv5r2JTDWU","sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":"9834576425"}
        headers = {
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        print("SMS will be Sent")
        purchase(prod_id,orderamount)
    return redirect(url_for('buy'))

if __name__ == '__main__':
    app.run(debug=True)
