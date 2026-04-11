# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT


############## Day 15 Slides Has Useful Info ##############

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta
from dbCodeRDS import *
from dbCodeDynamo import*
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import creds

app = Flask(__name__)

#-!-!-!-!-!- In the actual thing make sure this is actually a secret string -!-!-!-!-!-#
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

app.permanent_session_lifetime = timedelta(days=7)

#constants
DynamoTableName = creds.TABLE_NAME_Dynamo
DynamoRegionName = creds.DynamoRegion

dynamodb = boto3.resource('dynamodb', region_name=DynamoRegionName)
dynamoTable = dynamodb.Table(DynamoTableName)


####### Functions #######
def createSession(username, email):
    '''Creates a user session'''
    if 'username' in session:
        flash(f'You are already signed in as {session.get("username")} with the email {session.get("email")}. If you have just made a new account, please log out of your current account to sign in to the new one.', 'error')
        return
    session.permanent = True
    session['username'] = username
    session['email'] = email
    session['cart'] = {}
    flash('You are now logged in', 'success')


####### PAGE ROUTES #######

@app.route('/')
def landingPage():
    '''Brings user to the landing page and redirects if they are signed in'''
    
    #if statement that redirects to home page if session exists
    if 'username' in session:
        return redirect(url_for('homePage'))
    
    return render_template('landing_page.html')
    
@app.route('/SignInPage', methods=['GET'])
def signInPage():
    '''Brings user to the signin page'''

    #if statement that redirects to home page if session exists
    if 'username' in session:
        return redirect(url_for('homePage'))

    return render_template('sign_in_page.html')

@app.route('/SignUpPage', methods=['GET'])
def signUpPage():
    '''Brings user to the sign up page'''

    #if statement that redirects to home page if session exists
    if 'username' in session:
        return redirect(url_for('homePage'))

    return render_template('sign_up_page.html')

@app.route('/HomePage', methods=['GET'])
def homePage():
    '''Brings user to the home page'''

    #if statement that redirects to landing page if session doesn't exist
    if 'username' not in session:
        return redirect(url_for('landingPage'))
    
    rows = execute_query("""
        SELECT Inventory.ID, Inventory.description, Inventory.price, Inventory.categoryID, Category.name
        FROM Inventory
        JOIN Category USING (categoryID)
        ORDER BY Inventory.ID
        LIMIT 20
    """)

    return render_template('home_page.html', items=rows)

'''-=-=-=-=-=-=-=-=-=-=-'''
@app.route('/UserPage', methods=['GET'])
def userPage():
    '''Brings user to user page'''

    #if statement that redirects to landing page if session doesn't exist
    if 'username' not in session:
        return redirect(url_for('landingPage'))

    return render_template('user_page.html')

@app.route('/CheckoutPage', methods=['GET'])
def checkoutPage():
    '''Brings user ot checkout page'''

    #if statement that redirects to landing page if session doesn't exist
    if 'username' not in session:
        return redirect(url_for('landingPage'))

    rows = execute_query("""
        SELECT Inventory.ID, Inventory.description, Inventory.price, Inventory.categoryID, Category.name
        FROM Inventory
        JOIN Category USING (categoryID)
        ORDER BY Inventory.ID
        LIMIT 20
    """)

    #get total price
    cart= session.get('cart', {})
    total = 0
    for item_id, quantity in cart.items():
        row = execute_query("""SELECT price FROM Inventory WHERE ID = %s""", (item_id,))
        if row:
            price = row[0]['price']
            total += price * quantity

    return render_template('checkout_page.html', items=rows, total=total)


####### Action Routes #######
##-!-!- No Encryption Yet -!-!-##

@app.route('/SignIn', methods=['POST'])
def signIn():
    '''Signs in user and creates session'''
    # Extract form data
    email = request.form['email']
    password = request.form['password']

    #get user from table
    user = dynamoTable.query(KeyConditionExpression=Key('Email').eq(email))
    items = user.get('Items', [])

    #check if email exists in database
    if not items:
        flash('Incorrect credentials', 'error')
        return redirect(url_for('signInPage'))
    
    userInfo = items[0]

    #check that password is correct and create the session
    if(password == userInfo['Password']):
        createSession(email, userInfo['Email'])
        return redirect(url_for('homePage'))
    
    #notify user that either their password or email is wrong
    flash('Incorrect credentials', 'error')
    return redirect(url_for('signInPage'))

@app.route('/SignOut', methods=['POST'])
def signOut():
    '''Signs out user and deletes session'''

    #clear the session
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('landingPage'))

@app.route('/CreateUser', methods=['POST'])
def createUser():
    '''Creates a new user (email must be unique)'''
    # Extract form data
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    try: 
        #add new user to database
        dynamoTable.put_item(
            Item={
                'Email': email,
                'Password': password,
                'UserName': username
            },
            ConditionExpression='attribute_not_exists(Email)'
        )
        flash('User created successfully!', 'success')

        #creating a new session
        createSession(username, email)

        return redirect(url_for('homePage'))

    #error handling
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            flash('Email already exists! Please use a different email!', 'error')
            return redirect(url_for('signUpPage'))
        else:
            raise

'''-=-=-=-=-=-=-=-=-=-=-'''
@app.route('/ChangeUsername', methods=['PUT'])
def changeUsername():
    '''Changes a user's username'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

'''-=-=-=-=-=-=-=-=-=-=-'''
@app.route('/ChangePassword', methods=['PUT'])
def changePassword():
    '''Changes a user's password'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

'''-=-=-=-=-=-=-=-=-=-=-'''
@app.route('/ChangeEmail', methods=['PUT'])
def changeEmail():
    '''Changes a user's email'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

'''-=-=-=-=-=-=-=-=-=-=-'''
@app.route('/DeleteAccount', methods=['DELETE'])
def deleteAccount():
    '''Deletes a user's account'''
    #remember to incorporate flash message
    #remember to make sure the user can only delete their own

@app.route('/MakePurchase', methods=['POST'])
def makePurchase():
    '''Removes all items from the user's cart and gives them a summary'''
    #getting cart
    cart= session.get('cart', {})

    #finding the total price
    total = 0
    for item_id, quantity in cart.items():
        row = execute_query("""SELECT price FROM Inventory WHERE ID = %s""", (item_id,))
        if row:
            price = row[0]['price']
            total += price * quantity

    #deletes their cart
    session.pop('cart')
    flash(f'You made a purchase of ${round(total, 2)}', 'success')
    return redirect(url_for('homePage'))

@app.route('/AddItem', methods=['POST'])
def addItem():
    '''Adds an item to the user's cart'''
    #copies the cart
    cart = session.get('cart', {})
    #gets item_id from the form
    item_id = request.form['item_id']
    #adds one of that item to the cart
    cart[item_id] = cart.get(item_id, 0) + 1
    #replaces the cart with the newly made one
    session['cart'] = cart
    return redirect(url_for('homePage'))

@app.route('/RemoveItem', methods=['POST'])
def removeItem():
    '''Removes an item from the user's cart'''
    #copies the cart
    cart = session.get('cart', {})
    #gets item_id from the form
    item_id = request.form['item_id']
    #removes one of that item from the cart or delete it entirely if there is one
    if(cart[item_id] <= 1):
        cart.pop(item_id, None)
    else:
        cart[item_id] = cart.get(item_id, 0) - 1
    #replaces the cart with the newly made one
    session['cart'] = cart
    return redirect(url_for('homePage'))










''''''
@app.route('/l')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("First Name:", first_name, ":", "Last Name:", last_name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


"""==============================================================="""
"""This was used for testing. Remove it in end product if not used"""
"""==============================================================="""

@app.route('/viewdb')
def viewdb():
    """
    Fetches the first 20 items from the ProjectOneStore database
    and returns them as an HTML table.
    Route: /viewdb
    """
    rows = execute_query("""
        SELECT Inventory.ID, Inventory.description, Inventory.price, Inventory.categoryID, Category.name
        FROM Inventory
        JOIN Category USING (categoryID)
        ORDER BY Inventory.ID
        LIMIT 20
    """)
    return rows

@app.route('/DebugSession')
def debugSession():
    return {
        "session": dict(session)
    }

"""==============================================================="""

''''''

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
