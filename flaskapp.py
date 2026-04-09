# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT


############## Day 15 Slides Has Useful Info ##############


from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCodeRDS import *
from dbCodeDynamo import*

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

####### PAGE ROUTES #######
@app.route('/')
def landingPage():
    '''Brings user to the landing page and redirects if they are signed in'''

@app.route('/SignInPage', methods=['GET'])
def signInPage():
    '''Brings user to the signin page'''

@app.route('/SignUpPage', methods=['GET'])
def signUpPage():
    '''Brings user to the sign up page'''

@app.route('/HomePage', methods=['GET'])
def homePage():
    '''Brings user to the home page'''

@app.route('/UserPage', methods=['GET'])
def userPage():
    '''Brings user to user page'''

@app.route('/CheckoutPage', methods=['GET'])
def checkoutPage():
    '''Brings user ot checkout page'''


####### Action Routes #######
##-!-!- No Encryption Yet -!-!-##

@app.route('/SignIn', methods=['POST'])
def signIn():
    '''Signs in user and creates session'''

@app.route('/SignOut', methods=['POST'])
def signOut():
    '''Signs out user and deletes session'''

@app.route('/CreateUser', methods=['POST'])
def createUser():
    '''Creates a new user (email must be unique)'''

@app.route('/ChangeUsername', methods=['PUT'])
def changeUsername():
    '''Changes a user's username'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

@app.route('/ChangePassword', methods=['PUT'])
def changePassword():
    '''Changes a user's password'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

@app.route('/ChangeEmail', methods=['PUT'])
def changeEmail():
    '''Changes a user's email'''
    #remember to incorporate flash message
    #remember to make sure the user can only change their own

@app.route('/DeleteAccount', methods=['DELETE'])
def deleteAccount():
    '''Deletes a user's account'''
    #remember to incorporate flash message
    #remember to make sure the user can only delete their own

@app.route('/MakePurchase', methods=['PUT'])
def makePurchase():
    '''Reduces the stock of items in the database based on how many of each item the user has in their cart'''




'''
@app.route('/')
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

"""==============================================================="""

'''

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
