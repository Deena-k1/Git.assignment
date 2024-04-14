import requests
import json
from db_utils import get_available_books

from db_utils import get_all_waitlisted_books, all_books, reader_review, update_stock_quantity

### Functions to connect to app endpoints with user input ###




# function to add a new book order to the database
def add_new_order(customer_name, book_id, delivery):

    new_order = {
         "customer_name": customer_name,
         "book_id": book_id,
         "delivery": delivery,
    }

    # post request adds a new row to the database
    result = requests.post(
        'http://127.0.0.1:5000/purchase',  # goes to the endpoint in app.py for the link
        headers={'content-type': 'application/json'},
        data=json.dumps(new_order)
    )

    
    if result.status_code == 200:  # Check if the request was successful
     update_stock_quantity()  # Call the function to update stock quantity

    return result.json()

### Run function that interacts with user in terminal ###

#function that will recieve review input from user 
def handle_review():
    print("\n" + "ɷ" * 25 + " Review a Book " + "ɷ" * 25)
    all_books()
    valid_book_ids = [f'b{i}' for i in range(1, 12)]
    print("\nPlease select a book to review:")
    while True:
        book_id = input("Enter the ID of the book you want to review, e.g., 'b1': ")
        if book_id in valid_book_ids:
            break
        else:
            print("Invalid book ID. Please enter a valid book ID.")

    customer_name = input("Enter your name: ")
    while True:
        ratingstr = input("Enter your rating (1-5): ")
        try:
            rating = int(ratingstr)
            if 1 <= rating <= 5:
                break
            else:
                print("Rating must be between 1 and 5.")
        except ValueError:
            print("Please enter a valid number")

    if rating >= 1 and rating <= 5: 
        reader_review(customer_name, book_id, rating)
        print("Review added successfully!")  # Display success message
    else: 
        print('You have input an invalid option, please select one of the four choices')



def userOptionSelect(optionSelect):
    if optionSelect == 'waitlist':
        waitlisted_books = get_all_waitlisted_books()
        for book in waitlisted_books:
            print("Title:", book['title'])
            print("Author:", book['author'])
            print("Waitlist Date:", book['waitlist_date'])
            print("Waiting Days:", book['waiting_days'])
            print()
            print('Thanks for viewing our waitlist')
            print()
    elif optionSelect == 'view':
        # Add view books functionality here
        pass
    # purchase books functionality:
    elif optionSelect == 'purchase':
        cust = input('Enter your name: ')
        book_order_id = input('Enter the book ID of the book you would like to purchase: ')
        shipping = input('Choose if you would like the book to be delivered (yes/no): ')
        add_new_order(cust, book_order_id, shipping)
        print("Order is Successful")
        print()
        print('Thank you for your order!')

        pass
    elif optionSelect == 'review':
        handle_review()
       
        pass
    elif optionSelect == 'exit':
        print('Thanks for stopping by!')
    else: 
        print('You have input an invalid option, please select one of the valid choices')

def run():
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print('Welcome to ReadFirstGirls - your online bookstore')
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print()
    print()
    while True:
        optionSelect = input('''
             Would you like to:
                         
                * view our books
                * purchase a book 
                * review a book 
                * check out our waitlist
                             
            Please enter: view / purchase / review / waitlist / exit \n'''.lower())
        userOptionSelect(optionSelect)
        if optionSelect == 'exit':
            break


if __name__ == '__main__':
    run()

      