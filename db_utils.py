import mysql.connector
from config import USER, PASSWORD, HOST
from datetime import datetime

class DbConnectionError(Exception):

    pass

#function that uses mysql.connector to connect sql database to python using details in config file
def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx


# #functions to interact with SQL databases go here. Includes SQL queries
# Function to fetch all waitlisted books, using a join via the database. 
def get_all_waitlisted_books():
    waitlist = []
    try: 
        db_name = 'book_store_db'
        db_connection = _connect_to_db(db_name) #connect to database
        cur = db_connection.cursor()
        # Query the database
        query = """
            SELECT b.title, b.author, s.waitlist_date, s.waiting_days
            FROM books b
            JOIN book_stock s ON b.book_id = s.book_id
            WHERE waitlist = TRUE
            """
            
        cur.execute(query)
        
        # fetching the info
        result = cur.fetchall()  
        for row in result:
            waitlist.append({
            'title': row[0],
            'author': row[1],
            'waitlist_date': row[2],
            'waiting_days': row[3]
        })

        #checking for errors
    except Exception:
        raise DbConnectionError('Failed to fetch waitlist books')
        #closing connection
    finally: 
        if db_connection:
            cur.close()
            db_connection.close()
    # the output
    return waitlist
            

def add_purchase(customer_name, book_id, delivery):
    try:
        db_name = 'book_store_db'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        

        # generating the current date
        date = datetime.now().date().strftime('%Y-%m-%d')

        # query to get the current largest order id (should be the id of the latest entry in the table)
        order_id_query = """
            SELECT MAX(order_id)
            FROM orders
            """
        cur.execute(order_id_query)
        current_order_id = cur.fetchone()[0]  # here we are obtaining the result of the above query

        # now we use the above to set the order id of the new order
        # (we want it to automatically follow the previous order id)
        if current_order_id is None:
            order_id = 1
        else:
            order_id = current_order_id + 1

        # query to add a new row to the orders table
        new_order_query = """
            INSERT INTO orders
            (date, order_id, book_id, customer_name, delivery)
            VALUES
            ('{date}', '{order_id}', '{book_id}', '{customer_name}', '{delivery}')
        """.format(date=date, order_id=order_id, book_id=book_id, customer_name=customer_name, delivery=delivery)
        cur.execute(new_order_query)

        db_connection.commit()
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
     if db_connection:
        db_connection.close()

#Updates stock quantity and takes book_id as a parameter
def update_stock_quantity(book_id):
    try:
     db_name = 'book_store_db'
     db_connection = _connect_to_db(db_name)
     cur = db_connection.cursor()

#Decrements stock quantity by 1 for the given book_id
        
     update_stock_query = """
     UPDATE book_stock
     SET stock_quantity = stock_quantity - 1
     WHERE book_id = %s
     """

     cur.execute(update_stock_query, (book_id,))
     db_connection.commit()
     cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            # print("DB connection is closed")



def all_books(): # this will retrieve all the book titles to be used within reader_review() 
    try:
        db_name = 'book_store_db'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        get_books_query = """ SELECT book_id,
          title FROM books;"""
        cur.execute(get_books_query)
        result = cur.fetchall()#returning them as tuples 

        for i in result: #for loop to print the ids and names of all the books (return variable holds the output from the query)
            print(i)
        
        cur.close

    except mysql.connector.Error as error:
        print("Error:", error)
    finally: 
       
        if db_connection:
            db_connection.close()



def reader_review(customer_name, book_id, rating):
    try:
        review_date = datetime.now().date() 
        db_name = 'book_store_db'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)
         # query that will insert a review from customer into the reviews table
        
        add_review_q = """
            INSERT INTO reviews (customer_name, book_id, rating, review_date)
            VALUES (%s, %s, %s, %s)
        """
        review_data= (customer_name, book_id, rating, review_date)
        cur.execute(add_review_q, review_data)
        db_connection.commit()
        cur.close()
    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if _connect_to_db('book_store_db'):
            cur.close()

            print( "ɷ" * 25 )



#function to get all records for books currently available and not on waitlist
def get_available_books():
    try:
        book_data = []

        db_name = 'book_store_db' 
        db_connection = _connect_to_db(db_name)   #connects to mysql database book_store_db
        cur = db_connection.cursor()
        # print("Connected to DB: %s" % db_name)

        #SQL query to select all books that are in stock
        query = """
            SELECT b.book_id, b.title, b.author, b.year, s.stock_quantity, b.price 
            FROM books b
            INNER JOIN book_stock s
            ON b.book_id = 
            s.book_id
            WHERE s.stock_quantity > 0
            """
        cur.execute(query)   #execute sql query within connection to db
        result = cur.fetchall()  # this is a list with db records where each record is a tuple

        # tranform tuples into dictionaries
        for row in result:   #iterate over each row in the result frrom sql query
            book = {"book_id":row[0], "title":row[1], "author":row[2], "year":row[3], "stock_quantity":row[4], "price":row[5]} #transform each record into a dictionary with their column name as key
            book_data.append(book)   #add dictionary object of each book record into book_data list
        
        cur.close()   #close db

        return book_data
        
    except Exception:     #if any errors in try block raise this exception
        raise DbConnectionError("Failed to read books data from DB")

    finally:   #code to be executed anyway
        if db_connection:  #if connection to db successful, close connection and print message
            db_connection.close()
            # print("DB connection is closed")


#main file including all the functions created in this utils file
def main():  
    print(get_available_books())
    get_all_waitlisted_books()
    add_purchase()
    update_stock_quantity()
    all_books()
    reader_review()

if __name__ == '__main__':
    main()

