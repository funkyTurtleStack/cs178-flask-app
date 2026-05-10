# [Shop Project]

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Braedon Stapelman]
**GitHub:** [funkyTurtleStack]

---

## Overview

<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->
My Project is a verry bare bones shop project. You can sign in, add things to your cart, checkout, and change your user information. I have not incorporated encryption into this project simply because that makes it easier while making it and testing database interactions.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py                # Main Flask application — routes and app logic
├── dbCodeDynamo.py            # Database helper functions for dynamo (doesn't really get used)
├── dbCodeRDS.py               # Database helper functions for RDS (MySQL connection + queries)
├── creds_sample.py            # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html              # From boilerplate (not used)
│   ├── add_user.html          # From boilerplate (not used)
│   ├── delete_user.html       # From boilerplate (not used)
│   ├── display_users.html     # From boilerplate (not used)
│   ├── landing_page.html      # Where the user is sent to when they aren't logged in
│   ├── sign_in_page.html      # Page for signing in
│   ├── sign_up_page.html      # Page for making a new account
│   ├── home_page.html         # Page where you can add and remove items from your shopping cart
│   ├── user_page.html         # Page where users can change their user info or delete their account
│   ├── checkout_page.html     # Page where users "checkout"
├── .gitignore                 # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/funkyTurtleStack/cs178-flask-app.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://http://ec2-54-198-18-249.compute-1.amazonaws.com:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
Table_Name_Dynamo = "dynamo table name for users"
DynamoRegion = "dynamo database's region"
```

---

## Database Design

### SQL (MySQL on RDS)

For my relational database there are two tables. One for item categories and one for item info.

**Example:**

- `[Categories]` — categoryID, name; primary key is `[categoryID]`
- `[Inventory]` — ID, description, price, categoryID; primary key is `[ID]`; foreign key links to `[Categories]`

The JOIN query used in this project: 

rows = execute_query("""
        SELECT Inventory.ID, Inventory.description, Inventory.price, Inventory.categoryID, Category.name
        FROM Inventory
        JOIN Category USING (categoryID)
        ORDER BY Inventory.ID
        LIMIT 20
    """)

    It was used to combine the two tables so the item category could be listed for each item.

### DynamoDB

Mt dynamoDB table is just a users table.

- **Table name:** `Users`
- **Partition key:** `Email`
- **Other Column**  `Password`
- **Other Column**  `UserName`

---

## CRUD Operations

| Operation       | Route              | Description                    |
| ---------       | ----------         | --------------                 |
| GET             | `/`                | redirects to the landing page  |
| GET             | `/SignInPage`      | redirects to the sign in page  |
| GET             | `/SignUpPage`      | redirects to the sign up page  |
| GET             | `/HomePage`        | redirects to the home page     |
| GET             | `/UserPage`        | redirects to the user page     |
| GET             | `/CheckoutPage`    | redirects to the checkout page |S
| POST            | `/SignIn`          | signs in user                  |
| POST, Delete    | `/SignOut`         | signs out user                 |
| POST            | `/CreateUser`      | creates a new user             |
| POST, PUT       | `/ChangeUsername`  | changes a user's name          |
| POST, PUT       | `/ChangePassword`  | changes a user's password      |
| POST, PUT       | `/ChangeEmail`     | changes a user's email         |
| POST, DELETE    | `/DeleteAccount`   | deletes a user's account       |
| POST            | `/MakePurchase`    | makes a purchase               |
| POST, PUT       | `/AddItem`         | adds an item to the cart       |
| POST, PUT       | `/RemoveItem`      | removes an item from the cart  |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
The hardest part was probably getting the html to load with the right data. I learned how to use JINJA. I decided to use flask sessions for the cart.

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->

# Used AI to help with stopping repeat users from entering the database
# (In the '/CreateUser' route)
https://chatgpt.com/share/69d8c034-1388-8333-a482-775330c54bc5

# Used AI to get a refresher on routes as well as help understanding how to use flask sessions
# (This was mostly while creating the '/CreateUser' route)
https://claude.ai/share/630b7c78-8d92-4eaf-b58b-534fdead770c

# Used AI to help with jinja
# (This was mostly used in the making of home_page.html)
https://claude.ai/share/53d23cc3-dec5-4652-b836-32c080eec938