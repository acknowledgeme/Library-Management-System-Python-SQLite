import sqlite3
from sqlite3 import Error

def establish_db_link():
    db_link=None
    try:
        db_link=sqlite3.connect('mydatabase.db')
        print(f"Connected to SQLite, SQLite version: {sqlite3.sqlite_version}")
        return db_link
    except Error as e:
        print(e)
        return db_link

def generate_literacture_table(db_link):
    """create a table for storing books"""
    try:
        query='''CREATE TABLE IF NOT EXISTS books (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,year INTEGER);'''
        executor=db_link.cursor()
        executor.execute(query)
        print("Table created successfully")
    except Error as e:
        print(e)
"""
C-Create
R-Read
U-Update
D-Delete
"""
#create
def insert_literature(db_link,literature):
    """Add a new book to the books table"""
    query='''INSERT INTO books(title,author,year)VALUES(?,?,?)'''
    excutor=db_link.cursor()
    excutor.execute(query,literature)
    db_link.commit()
    return excutor.lastrowid
#Read
def fetch_all_literature(db_link):
    """Query all rows in the book table"""
    executor=db_link.cursor()
    executor.execute("SELECT * FROM books")
    records=executor.fetchall()

    for record in records:
        print(record)
#update
def modify_literature(db_link, literature):
    query = '''
    UPDATE books
    SET title = ?, author = ?, year = ?
    WHERE id = ?
    '''
    executor = db_link.cursor()
    executor.execute(query, literature)
    db_link.commit()
#delete
def remove_literature(db_link,literature_id):
    """Delete a book by book id"""
    query='DELETE FROM books WHERE id=?'
    executor=db_link.cursor()
    executor.execute(query,(literature_id,))
    db_link.commit()
def execute_program():
    #Create a database connection
    db_link=establish_db_link()
    if db_link is not None:
        #create table
        generate_literacture_table(db_link)
        #Add books
        novel1=('The Great Gatsby','F. Scott Fitzgerald',1925)
        novel2=('To Kill a Mockingbord','Harper Lee',1960)
        novel_id1=insert_literature(db_link,novel1)
        novel_id2=insert_literature(db_link,novel2)
        print(f"Added books with IDs:{novel_id1},{novel_id2}")

        #View all books
        print("\nAll books:")
        fetch_all_literature(db_link)

        #update a book
        updated_novel = ('The Great Gatsby (Updated)', 'F. Scott Fitzgerald', 1925, novel_id1)

        modify_literature(db_link, updated_novel)

        print("\nAfter update:")
        fetch_all_literature(db_link)

        #Delete a book
        remove_literature(db_link,novel_id2)
        print("\nAfter deletion:")
        fetch_all_literature(db_link)

        #close the connection
        db_link.close()
    else:
        print("Error! Cannot create the database connection.")
if __name__=='__main__':
    execute_program()
