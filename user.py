import sqlite3
import csv  

DB_NAME = "users.db"
FILE = "sample_users.csv"

INPUT_STRING = """
Enter the option:
    1. CREATE TABLE users
    2. Import data from CSV file
    3. Add new record to database
    4. Delete a record from id of user
    5. Delete all records from user table
    6. Query all records from user table
    7. Update a record using id of user
    8. Press any key to quit
"""
CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name CHAR(255) NOT NULL,
        last_name CHAR(225) NOT NULL,
        company_name CHAR(225) NOT NULL,
        address CHAR(225) NOT NULL,
        city CHAR(225) NOT NULL,
        county CHAR(225) NOT NULL,
        state CHAR(225) NOT NULL,
        zip REAL NOT NULL,
        phone1 CHAR(225) NOT NULL,
        phone2 CHAR(225),
        email CHAR(225) NOT NULL,
        web text
    );
"""

COLUMNS = (
    'first_name',
    'last_name',
    'company_name',
    'address',
    'city',
    'county',
    'state',
    'zip',
    'phone1',
    'phone2',
    'email',
    'web',
)

COLUMN_INPUT_STRING = f"""
Which column would you like to update? Please make sure column is one of the following:
{COLUMNS}
"""

#CRUDE => create, retrieve(select), update, delete


def create_connection(db_name):
    """creating connection and return cursor object
    
    Returns:
        conn: sqlite3 connection object
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except Exception as e:
        print(str(e))
    finally:
        return conn

def create_table(conn):
    """create a table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
    """
    cur = conn.cursor()    # creating cursor object for CRUDE operation
    cur.execute(CREATE_USERS_TABLE_QUERY)
    conn.commit()
    print("User table was successfully created.")

def open_csv_file(FILE):
    """opens csv files and return all records in list of tuple

    Args:
        FILE (str): name of file

    Returns:
        list[tuple]: all records from csv file
    """
    db_data = []    # to keep it in tuple under list
    with open(FILE) as f:
        data = csv.reader(f, delimiter = ',')
        for abc in data:
            db_data.append(tuple(abc))
    return db_data[1:]

def insert_users(conn, db_data):
    """Insert record to table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
        db_data (list[tuple]): all records for table

    Returns:
        None: None
    """
    user_add_query = '''
    INSERT INTO users
    (first_name, last_name, company_name, address, city, county, state, zip, phone1, phone2, email, web)

    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cur = conn.cursor()    # creating cursor object for CRUDE operation
    cur.executemany(user_add_query, db_data)
    conn.commit()
    print("Successfully inserted data into user table.")

def select_all_records(conn):
    """select and print records from table

    Args:
        conn (sqlite3 connection): sqlite3 connection object

    Returns:
        None: None
    """
    cur = conn.execute("SELECT * from users;")
    for xyz in cur:
        print(xyz)

def update_user(conn, column_name, user_id, column_value):
    """update single record to table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
        column_name (str): name of column
        user_id (int): id of user
        column_value (str): value of column
    """
    cur = conn.execute(f"UPDATE users set {column_name}=? where id = ?", (column_value, user_id,))
    conn.commit()
    print(f"Successfully updated {column_name} of user {user_id}")

def delete_user_id(conn, user_id):
    """delete single record from table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
        user_id (int): id of user
    """
    cur = conn.execute("DELETE from users where id = ?", (user_id,))    # here, ? is used for injection/protection
    conn.commit()
    print("Successfully deleted record from user table")

def delete_all_records(conn):
    """delete all records from table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
    """
    cur = conn.execute("DELETE from users")
    conn.commit()
    print("Successfully deleted all records from user table")

def main():
    conn = create_connection(DB_NAME)

    while True:

        user_input = input(INPUT_STRING)

        if user_input == '1':
            create_table(conn)

        elif user_input == "2":
            data = open_csv_file(FILE)
            insert_users(conn, data)

        elif user_input == "3":
            data = []
            for column in COLUMNS:
                user_input = input(f"Enter {column}: ")
                data.append(user_input)

            data = tuple(data)
            print(data)
            insert_users(conn, [data])

        elif user_input == "4":
            user_id = input("Enter id of user: ")
            if user_id.isnumeric():
                delete_user_id(conn, user_id)

        elif user_input == "5":
            confirmation = input(
                "Are you sure? \
                Press y or Yes to continue. \
                Or, Press n or No to skip."
            )
            if confirmation.lower() in ["y", "yes"]:
                delete_all_records(conn)

        elif user_input == "6":
            select_all_records(conn)

        elif user_input == "7":
            user_id = input("Enter id of user: ")
            if user_id.isnumeric():
                column_name = input(COLUMN_INPUT_STRING)
                column_value = input(f"Enter value of {column_name}: ")
                update_user(conn, column_name, user_id, column_value)

        else:
            exit()

if __name__ == "__main__":
    main()