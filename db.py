import sqlite3

# this will create a new database because we do not already have one
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# creating the categories table
cursor.execute('''CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT
)''')

# creating the authors table
cursor.execute('''CREATE TABLE IF NOT EXISTS Authors (
    author_id INTEGER PRIMARY KEY,
    author_name TEXT
)''')

# creating the books table with foreign keys
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors (author_id),
    FOREIGN KEY (category_id) REFERENCES Categories (category_id)
)''')

# creating the reviews table with a foreign key
cursor.execute('''CREATE TABLE IF NOT EXISTS Reviews (
    review_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    user_id INTEGER,
    rating INTEGER,
    review_text TEXT,
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
)''')

# Function to insert a new category into the Categories table
def insert_category(category_name):
    try:
        # Check for an existing category with the same name, ignoring capitalization
        cursor.execute("SELECT category_name FROM Categories WHERE lower(category_name) = lower(?)", (category_name,))
        existing_category = cursor.fetchone()
        
        if existing_category:
            existing_categories = get_categories()
            categories_list = [c[1] for c in existing_categories]
            return f"Category '{category_name}' already exists. Current categories: {', '.join(categories_list)}"

        cursor.execute("INSERT INTO Categories (category_name) VALUES (?)", (category_name,))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted category
    except sqlite3.Error as e:
        print(f"Error inserting category: {e}")
        return None

# Function to update the title of a book
def update_book_title(book_id, new_title):
    try:
        cursor.execute("UPDATE Books SET title = ? WHERE book_id = ?", (new_title, book_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating book title: {e}")

# Function to delete a review by review ID
def delete_review(review_id):
    try:
        cursor.execute("DELETE FROM Reviews WHERE review_id = ?", (review_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting review: {e}")

# Function to retrieve books by a specific author's name
def get_books_by_author(author_name):
    try:
        cursor.execute("SELECT * FROM Books WHERE author_id IN (SELECT author_id FROM Authors WHERE author_name = ?)", (author_name,))
        books = cursor.fetchall()
        return books
    except sqlite3.Error as e:
        print(f"Error retrieving books by author: {e}")
        return []

# Function to add a new book
def add_book(title, author_id, category_id):
    try:
        # Check if the book with the same title and author_id already exists
        cursor.execute("SELECT book_id FROM Books WHERE title = ? AND author_id = ?", (title, author_id))
        existing_book = cursor.fetchone()
        
        if existing_book:
            return "A book with the same title and author already exists."

        # Check if the category_id exists in Categories
        cursor.execute("SELECT category_id FROM Categories WHERE category_id = ?", (category_id,))
        existing_category = cursor.fetchone()

        if not existing_category:
            category_info = get_categories()  # Retrieve available categories
            return "Category with the given ID does not exist. Available categories: " + ", ".join(c[1] for c in category_info)

        cursor.execute("INSERT INTO Books (title, author_id, category_id) VALUES (?, ?, ?)",
                       (title, author_id, category_id))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted book
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")
        return None

# Function to add a new author
def add_author(author_name):
    # Check if the author with the same name already exists
    cursor.execute("SELECT author_id FROM Authors WHERE author_name = ?", (author_name,))
    existing_author = cursor.fetchone()

    if existing_author:
        print("Error: Author with the same name already exists.")
        return "Author with the same name already exists."

    try:
        cursor.execute("INSERT INTO Authors (author_name) VALUES (?)", (author_name,))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted author
    except sqlite3.Error as e:
        print(f"Error adding author: {e}")
        return None

# Function to add a new review
def add_review(book_id, user_id, rating, review_text):
    try:
        cursor.execute("INSERT INTO Reviews (book_id, user_id, rating, review_text) VALUES (?, ?, ?, ?)",
                       (book_id, user_id, rating, review_text))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted review
    except sqlite3.Error as e:
        print(f"Error adding review: {e}")
        return None
    
# Function to retrieve all categories
def get_categories():
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    return categories

# Function to retrieve all books with details (including category name)
def get_all_books():
    cursor.execute('''SELECT Books.book_id, Books.title, Authors.author_name, Categories.category_name, Reviews.rating, Reviews.review_text
                    FROM Books
                    LEFT JOIN Authors ON Books.author_id = Authors.author_id
                    LEFT JOIN Categories ON Books.category_id = Categories.category_id
                    LEFT JOIN Reviews ON Books.book_id = Reviews.book_id''')
    books = cursor.fetchall()
    return books

conn.commit()
# conn.close()
