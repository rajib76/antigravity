from library import Library

def print_menu():
    print("\n--- Library Management System ---")
    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. List All Books")
    print("6. List All Members")
    print("7. Exit")

def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            try:
                copies = int(input("Enter total copies (default 1): ") or 1)
            except ValueError:
                copies = 1
            library.add_book(title, author, isbn, copies)

        elif choice == '2':
            name = input("Enter member name: ")
            member_id = input("Enter member ID: ")
            library.register_member(name, member_id)

        elif choice == '3':
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            library.borrow_book(member_id, isbn)

        elif choice == '4':
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            library.return_book(member_id, isbn)

        elif choice == '5':
            library.list_books()

        elif choice == '6':
            library.list_members()

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
