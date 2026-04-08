import creds
import boto3
from boto3.dynamodb.conditions import Key

def get_users_table():
    """Return a reference to the DynamoDB Users table"""
    dynamodb = boto3.resource("dynamodb", region_name=creds.DynamoRegion)
    return dynamodb.Table(creds.TABLE_NAME_Dynamo)





"""-!-!-!-!-!-TO ONLY BE USED FOR TESTING-!-!-!-!-!-"""

def print_user(user):
    """Print a single user's user data."""
    UserID = user.get("UserID", "Unknown Id")
    Email = user.get("Email", "Unknown Email")
    Password = user.get("Password", "Unknown Password")
    UserName = user.get("UserName", "Unknown User Name")
    
    
    print(f"  UserID  : {UserID}")
    print(f"  Email   : {Email}")
    print(f"  Password: {Password}")
    print(f"  UserName: {UserName}")
    print()

def print_all_users():
    """Prints every user from the user table"""
    table = get_users_table()

    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No users found. Make sure the table has data and is connected properly.")
        return
    
    print(f"Found {len(items)} user(s):\n")
    for user in items:
        print_user(user)

def main():
    print("===== Reading from DynamoDB =====\n")
    print_all_users()


if __name__ == "__main__":
    main()



"""-!-!-!-!-!-TO ONLY BE USED FOR TESTING-!-!-!-!-!-"""