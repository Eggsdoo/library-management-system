import sqlite3
from db import (
    insert_category, update_book_title, delete_review, get_books_by_author,
    add_book, add_author, add_review, get_categories, get_all_books, delete_book, 
    get_review_by_id, update_book_author, update_book_category
)
import textwrap
from colorama import Fore, Style # for my text coloring

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def view_categories():
    categories = get_categories()
    if not categories:
        print(Fore.RED + "No categories found." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "Categories:" + Style.RESET_ALL)
        for category in categories:
            print(f"ID: {category[0]}, Category: {category[1]}")
            print("=" * 25)
    print()

def view_all_books():
    books = get_all_books()
    if not books:
        print(Fore.RED + "No books found." + Style.RESET_ALL)
    else:
        print("All Books:")
        print(f"{'ID':<4}{'Book':<40}{'Author':<20}{'Category':<15}{'Rating':<8}{'Review':<50}")
        print("=" * 100)
        for book in books:
            book_id = book[0]
            book_title = book[1] if book[1] else "N/A"
            author_name = book[2] if book[2] else "N/A"
            category_name = book[3] if book[3] else "N/A"
            rating = book[4] if book[4] is not None else "N/A"
            review = book[5] if book[5] else "N/A"

            # wrapping the book title to a maximum width (in this case 40 characters)
            wrapped_title = textwrap.fill(book_title, width=40)

            print(f"{book_id:<4}{wrapped_title:<40}{author_name:<20}{category_name:<15}{rating:<8}{review:<50}")
            print("=" * 100)
    print()

def capitalize_words(text):
    # Capitalize the first letter of each word
    return ' '.join(word.capitalize() for word in text.split())

def view_books_with_ids():
    books = get_all_books()
    if not books:
        print("No books found.")
    else:
        print("Books:")
        print(f"{'ID':<4}{'Book':<40}")
        for book in books:
            book_id = book[0]
            book_title = book[1] if book[1] else "N/A"

            # wrapping the book title to a maximum width (in this case 40 characters)
            wrapped_title = textwrap.fill(book_title, width=40)

            print(f"{book_id:<4}{wrapped_title:<40}")

def main_menu():
    while True:
        print("Library Management System")
        print("1. Add Book")
        print("2. Add Author")
        print("3. Add Category")
        print("4. Add Review")
        print("5. Update Book")
        print("6. Delete Review")
        print("7. Delete Book")
        print("8. Search Books by Author")
        print("9. Search Books by Category")
        print("10. View All Books")
        print("11. View Categories")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the book title: ")
            author_name = input("Enter the author's name: ")
            author_name = capitalize_words(author_name)

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

            result = add_book(title, author_name, category_id)

            if result > 0:
                print(f"Book successfully added: Book ID {result}, Book Name: {title}, Author Name: {author_name}, Category: {category_id}")
            else:
                print(f"Error: Invalid (Please check for duplicate entry).")

        elif choice == "2":
            author_name = input("Enter the author's name: ")
            author_name = capitalize_words(author_name)

            result = add_author(author_name)

            if result:
                print(f"Author successfully added: Author ID {result}, Author Name: {author_name}")
            else:
                print("Error: Author with the same name already exists.")

        elif choice == "3":
            while True:
                category_name = input("Enter the category name: ")
                category_name = capitalize_words(category_name)

                result = insert_category(category_name)

                if isinstance(result, int):
                    print(f"Category '{category_name}' added with ID: {result}")
                    break
                else:
                    print(f"Error: {result}")

        elif choice == "4":
            book_id = int(input("Enter the book ID: "))

            # Check if the book exists before allowing the review
            book = [book for book in get_all_books() if book[0] == book_id]
            if not book:
                print(f"Error: No book found with ID {book_id}.")
                continue

            user_id = int(input("Enter the user ID: "))
            while True:
                rating = input("Enter the rating (0-5): ")
                try:
                    rating = float(rating)
                    if 0 <= rating <= 5:
                        break
                    else:
                        print("Error: Rating should be between 0 and 5.")
                except ValueError:
                    print("Error: Please enter a valid numeric rating.")
            review_text = input("Enter the review text: ")
            review_id = add_review(book_id, user_id, rating, review_text)

            if review_id:
                print("Review successfully added.")
            else:
                print("Error: Failed to add the review.")

        elif choice == "5":
            book_name = input("Enter the book name: ")
            book_name = capitalize_words(book_name)
            books = [book for book in get_all_books() if book[1] == book_name]
            if not books:
                print(f"Error: No book found with the name '{book_name}'.")
                continue

            # Display book details and confirm with the user
            for book in books:
                book_id, book_title, author_name, category_name = book[0], book[1], book[2], book[3]
                print(f"Book ID: {book_id}")
                print(f"Book Name: {book_title}")
                print(f"Author: {author_name}")
                print(f"Category: {category_name}")
                confirm = input("Is this the correct book? (y/n): ").strip().lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    continue
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            # Allow the user to update book details
            if confirm == 'y':
                new_title = input("Enter a new title: ")
                new_author_name = input("Enter a new author name: ")
                new_category_id = int(input("Enter a new category ID: "))
                if new_category_id not in existing_category_ids:
                    print("Error: Invalid category ID.")
                    continue

                # Update the book details
                update_book_title(book_id, new_title)
                update_book_author(book_id, new_author_name)
                update_book_category(book_id, new_category_id)
                print("Book details updated successfully.")

        elif choice == "6":
            review_id = int(input("Enter the review ID: "))
            
            # we will check to see if the review with the provided ID exists
            review = get_review_by_id(review_id)
            if review:
                print("Review Details: ")
                print(f"Review ID: {review[0]}")
                print(f"Book ID: {review[1]}")
                print(f"User ID: {review[2]}")
                print(f"Rating: {review[3]}")
                print(f"Review Text: {review[4]}")
                
                # asking user for confirmation next
                confirmation = input("Do you want to delete this review? (y/n): ").strip().lower()
                if confirmation == "y":
                    delete_review(review_id)
                    print("Review deleted successfully.")
                elif confirmation == "n":
                    print("Review not deleted.")
                else:
                    print("Error: Invalid input. Please enter 'y' to delete or 'n' to cancel.")
            else:
                print(f"Error: Review with ID {review_id} does not exist.")

        elif choice == "7":
            view_books_with_ids()
            book_id_to_delete = int(input("Enter the book ID to delete: "))
            result = delete_book(book_id_to_delete)
            if result:
                print("Book deleted successfully.")
            else:
                print("Error: Failed to delete the book.")

        elif choice == "8":
            author_name = input("Enter the author's name: ")
            author_name = capitalize_words(author_name)
            books = get_books_by_author(author_name)
            for book in books:
                print(f"Book ID: {book[0]}, Title: {book[1]}")
       
        elif choice == "9":
            view_categories()
            while True:
                category_id = input("Enter a Category ID: ")
                try:
                    category_id = int(category_id)
                    existing_categories = get_categories()
                    existing_category_ids = [category[0] for category in existing_categories]

                    if category_id in existing_category_ids:
                        break  # Exit the loop if the category is valid
                    else:
                        print("Error: Invalid category ID. Please try again.")
                except ValueError:
                    print("Error: Please enter a valid numeric category ID.")

            # Display books in the selected category
            books_in_category = [book for book in get_all_books(category_id)]
            category_name = next((cat[1] for cat in existing_categories if cat[0] == category_id), "N/A")

            if not books_in_category:
                print(f"No books found in '{category_name}'.")
            else:
                print(f"Books in '{category_name}':")
                print(f"{'ID':<4}{'Book':<40}{'Author':<20}{'Rating':<8}{'Review':<50}")
                print("=" * 100)  
                for book in books_in_category:
                    book_id = book[0]
                    book_title = book[1] if book[1] else "N/A"
                    author_name = book[2] if book[2] else "N/A"
                    rating = book[4] if book[4] is not None else "N/A"
                    review = book[5] if book[5] else "N/A"
                    wrapped_title = textwrap.fill(book_title, width=40)
                    print(f"{book_id:<4}{wrapped_title:<40}{author_name:<20}{rating:<8}{review:<50}")
                print("=" * 100)  
                print()

        elif choice == "10":
            view_all_books()

        elif choice == "11":
            view_categories()

        elif choice == "12":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

conn.close()
