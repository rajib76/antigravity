import json
import os
from models import Book, Member

DATA_FILE = "library_data.json"

class Library:
    def __init__(self):
        self.books = {}  # Map ISBN to Book object
        self.members = {}  # Map Member ID to Member object
        self.load_data()

    def add_book(self, title, author, isbn, total_copies=1):
        if isbn in self.books:
            self.books[isbn].total_copies += total_copies
            self.books[isbn].available_copies += total_copies
            print(f"Updated copies for '{title}'.")
        else:
            new_book = Book(title, author, isbn, total_copies)
            self.books[isbn] = new_book
            print(f"Added new book: '{title}'.")
        self.save_data()

    def register_member(self, name, member_id):
        if member_id in self.members:
            print(f"Member ID {member_id} already exists.")
            return
        new_member = Member(name, member_id)
        self.members[member_id] = new_member
        print(f"Registered member: {name}.")
        self.save_data()

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        book = self.books[isbn]
        member = self.members[member_id]

        if book.available_copies > 0:
            book.available_copies -= 1
            member.borrowed_books.append(isbn)
            print(f"Successfully borrowed '{book.title}'.")
            self.save_data()
        else:
            print("Book is currently unavailable.")

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        
        member = self.members[member_id]
        
        if isbn not in member.borrowed_books:
            print("This member has not borrowed this book.")
            return

        if isbn in self.books:
            book = self.books[isbn]
            book.available_copies += 1
            member.borrowed_books.remove(isbn)
            print(f"Successfully returned '{book.title}'.")
            self.save_data()
        else:
             # Edge case: Book removed from library but member still has it?
             # For now, just remove from member record.
             member.borrowed_books.remove(isbn)
             print("Returned book (not in library catalog).")
             self.save_data()

    def list_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books.values():
            print(book)

    def list_members(self):
        if not self.members:
            print("No registered members.")
            return
        for member in self.members.values():
            print(member)

    def save_data(self):
        data = {
            "books": [book.to_dict() for book in self.books.values()],
            "members": [member.to_dict() for member in self.members.values()]
        }
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for book_data in data.get("books", []):
                    book = Book.from_dict(book_data)
                    self.books[book.isbn] = book
                for member_data in data.get("members", []):
                    member = Member.from_dict(member_data)
                    self.members[member.member_id] = member
        except Exception as e:
            print(f"Error loading data: {e}")
