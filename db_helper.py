from logging import exception

import mysql.connector
import mysql.connector.errors

global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#######",
    database="pandeyji_eatery"
)

def get_next_order_id():
    cursor = cnx.cursor()
    query = f"SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    if result is None:
        return 1
    else:
        return result + 1

def insert_order_item(food_items, quantity, order_id):
    try:
        cursor = cnx.cursor()
        #calling 'stored procedure' (from inside sql database)
        cursor.callproc('insert_order_item', (food_items, quantity, order_id))
        cnx.commit()
        print("order Item inserted Successfully")
        return 1
    except mysql.connector.Error as err:
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred {e}")
        cnx.rollback()
        return -1

def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()
    insert_query = r"INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()

def get_total_order_price(order_id):
    cursor = cnx.cursor()
    #call the function within SQL database
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def get_order_status(order_id):
    cursor = cnx.cursor()
    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)
    # Fetching the result
    result = cursor.fetchone()
    # Closing the cursor
    cursor.close()
    # Returning the order status
    if result:
        return result[0]
    else:
        return None
