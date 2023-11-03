import sqlite3
from db import insert_category, update_book_title, delete_review, get_books_by_author, add_book, add_author, add_review, get_categories, get_all_books

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def view_categories():
    categories = get_categories()
    if not categories:
        print("No categories found.")
    else:
        print("Categories:")
        for category in categories:
            print(f"ID: {category[0]}, Category: {category[1]}")
    print()

def view_all_books():
    books = get_all_books()
    if not books:
        print("No books found.")
    else:
        print("All Books:")
        print(f"{'ID':<4}{'Book':<30}{'Author':<20}{'Category':<15}{'Rating':<8}{'Review':<50}")
        for book in books:
            book_id = book[0]
            book_title = book[1] if book[1] else "N/A"
            author_name = book[2] if book[2] else "N/A"
            category_name = book[3] if book[3] else "N/A"
            rating = book[4] if book[4] is not None else "N/A"
            review = book[5] if book[5] else "N/A"
            print(f"{book_id:<4}{book_title:<30}{author_name:<20}{category_name:<15}{rating:<8}{review:<50}")
    print()

def capitalize_words(text):
    # Capitalize the first letter of each word
    return ' '.join(word.capitalize() for word in text.split())

def main_menu():
    while True:
        print("Library Management System")
        print("1. Add Book")
        print("2. Add Author")
        print("3. Add Category")
        print("4. Add Review")
        print("5. Update Book Title")
        print("6. Delete Review")
        print("7. Search Books by Author")
        print("8. View All Books")
        print("9. View Categories")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the book title: ")
            author_id = int(input("Enter the author ID: "))

            while True:
                category_id = int(input("Enter the category ID: "))
                existing_categories = get_categories()
                existing_category_ids = [category[0] for category in existing_categories]

                if category_id in existing_category_ids:
                    break  # Exit the loop if the category is valid
                else:
                    print("Error: Invalid category ID. Please try again.")

            # Capitalize book title
            title = capitalize_words(title)

            result = add_book(title, author_id, category_id)

            if isinstance(result, int):
                print(f"Book added with ID: {result}")
            else:
                print(f"Error: {result}")
        elif choice == "2":
            author_name = input("Enter the author's name: ")

            # Capitalize author name
            author_name = capitalize_words(author_name)

            add_author(author_name)
        elif choice == "3":
            while True:
                category_name = input("Enter the category name: ")

                # Capitalize category name
                category_name = capitalize_words(category_name)

                result = insert_category(category_name)
                if isinstance(result, int):
                    print(f"Category '{category_name}' added with ID: {result}")
                    break
                else:
                    print(f"Error: {result}")
        elif choice == "4":
            book_id = int(input("Enter the book ID: "))
            user_id = int(input("Enter the user ID: "))
            rating = int(input("Enter the rating: "))
            review_text = input("Enter the review text: ")
            add_review(book_id, user_id, rating, review_text)
        elif choice == "5":
            book_id = int(input("Enter the book ID: "))
            new_title = input("Enter the new title: ")

            # Capitalize new book title
            new_title = capitalize_words(new_title)

            update_book_title(book_id, new_title)
        elif choice == "6":
            review_id = int(input("Enter the review ID: "))
            delete_review(review_id)
        elif choice == "7":
            author_name = input("Enter the author's name: ")

            # Capitalize author name
            author_name = capitalize_words(author_name)

            books = get_books_by_author(author_name)
            for book in books:
                print(f"Book ID: {book[0]}, Title: {book[1]}")
        elif choice == "8":
            view_all_books()
        elif choice == "9":
            view_categories()
        elif choice == "10":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

conn.close()
