import os

BOOKS_FILE = "books.txt"
MEMBERS_FILE = "members.txt"


class Book:
    """Class representing a Book"""

    def __init__(self, book_id, title, author, total_copies, available_copies=None):
        self.book_id = book_id
        self.title = title.title()
        self.author = author.title()
        self.total_copies = total_copies
        self.available_copies = available_copies if available_copies is not None else total_copies

    def to_string(self):
        return f"{self.book_id},{self.title},{self.author},{self.total_copies},{self.available_copies}"

    @staticmethod
    def from_string(book_data):
        book_id, title, author, total_copies, available_copies = book_data.strip().split(",")
        return Book(int(book_id), title, author, int(total_copies), int(available_copies))


class Library:
    """Manages book collection and operations"""

    def __init__(self):
        self.books = {}
        self.load_books()

    def load_books(self):
        """Load books from file"""
        if not os.path.exists(BOOKS_FILE):
            return
        with open(BOOKS_FILE, "r") as f:
            for line in f:
                book = Book.from_string(line)
                self.books[book.book_id] = book

    def save_books(self):
        """Save books to file"""
        with open(BOOKS_FILE, "w") as f:
            for book in self.books.values():
                f.write(book.to_string() + "\n")

    def add_book(self):
        """Add a new book to the library"""
        try:
            book_id = max(self.books.keys(), default=0) + 1
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            copies = int(input("Enter number of copies: "))

            if copies <= 0:
                print("Number of copies must be positive.")
                return

            book = Book(book_id, title, author, copies)
            self.books[book_id] = book
            self.save_books()
            print(f"Book '{title}' added successfully.")
        except ValueError:
            print("Invalid input. Please enter a number for copies.")

    def remove_book(self):
        """Remove a book by its ID"""
        try:
            book_id = int(input("Enter book ID to remove: "))
            if book_id in self.books:
                del self.books[book_id]
                self.save_books()
                print("Book removed successfully.")
            else:
                print("Book ID not found.")
        except ValueError:
            print("Invalid book ID.")

    def update_book(self):
        """Update book details"""
        try:
            book_id = int(input("Enter book ID to update: "))
            if book_id not in self.books:
                print("Book ID not found.")
                return

            book = self.books[book_id]
            option = input("What to update? (T/t=Title, A/a=Author, C/c=Copies): ").strip().lower()

            if option == "t":
                book.title = input("Enter new title: ").strip().title()
            elif option == "a":
                book.author = input("Enter new author: ").strip().title()
            elif option == "c":
                new_copies = int(input("Enter new total copies: "))
                if new_copies < book.available_copies:
                    print("Total copies cannot be lower than available copies.")
                    return
                book.total_copies = new_copies
            else:
                print("Invalid option.")
                return

            self.save_books()
            print("Book updated successfully.")
        except ValueError:
            print("Invalid input.")

    def search_book(self):
        """Search for a book by title"""
        title = input("Enter book title to search: ").strip().title()
        found_books = [book for book in self.books.values() if title in book.title]

        if found_books:
            for book in found_books:
                print(f"{book.book_id}: {book.title} by {book.author} ({book.available_copies}/{book.total_copies} available)")
        else:
            print("No books found.")

    def display_books(self):
        """Display all books"""
        if not self.books:
            print("No books available.")
            return

        for book in self.books.values():
            print(f"{book.book_id}: {book.title} by {book.author} ({book.available_copies}/{book.total_copies} available)")


class Member:
    """Manages library members"""

    def __init__(self):
        self.members = {}
        self.load_members()

    def load_members(self):
        """Load members from file"""
        if not os.path.exists(MEMBERS_FILE):
            return
        with open(MEMBERS_FILE, "r") as f:
            for line in f:
                name, borrowed_books = line.strip().split(":")
                self.members[name] = [int(book_id) for book_id in borrowed_books.split(",") if book_id]

    def save_members(self):
        """Save members to file"""
        with open(MEMBERS_FILE, "w") as f:
            for name, books in self.members.items():
                f.write(f"{name}:{','.join(map(str, books))}\n")

    def add_member(self):
        """Add a new member"""
        name = input("Enter member name: ").strip()
        if not name:
            print("Member name cannot be empty.")
            return

        if name in self.members:
            print("Member already exists.")
        else:
            self.members[name] = []
            self.save_members()
            print(f"Member '{name}' added successfully.")

    def remove_member(self):
        """Remove a member"""
        name = input("Enter member name to remove: ").strip()
        if name in self.members:
            if self.members[name]:
                print("Member has borrowed books. Cannot remove.")
                return
            del self.members[name]
            self.save_members()
            print("Member removed successfully.")
        else:
            print("Member not found.")

    def issue_book(self, library):
        """Issue a book to a member"""
        name = input("Enter member name: ").strip()
        if name not in self.members:
            print("Member not found.")
            return

        try:
            book_id = int(input("Enter book ID to issue: "))
            if book_id in self.members[name]:
                print("Member already borrowed this book.")
                return

            if book_id in library.books:
                book = library.books[book_id]
                if book.available_copies > 0:
                    book.available_copies -= 1
                    self.members[name].append(book_id)
                    library.save_books()
                    self.save_members()
                    print(f"Book '{book.title}' issued to {name}.")
                else:
                    print("Book is out of stock.")
            else:
                print("Book not found.")
        except ValueError:
            print("Invalid book ID.")

    def return_book(self, library):
        """Return a borrowed book"""
        name = input("Enter member name: ").strip()
        if name not in self.members:
            print("Member not found.")
            return

        try:
            book_id = int(input("Enter book ID to return: "))
            if book_id in self.members[name]:
                book = library.books[book_id]
                book.available_copies += 1
                self.members[name].remove(book_id)
                library.save_books()
                self.save_members()
                print(f"Book '{book.title}' returned by {name}.")
            else:
                print("Member did not borrow this book.")
        except ValueError:
            print("Invalid book ID.")


def main():
    library = Library()
    members = Member()

    while True:
        choice = input("\n1. Add Book | 2. Remove Book | 3. Update Book | 4. Search Book | 5. Display Books | 6. Add Member | 7. Remove Member | 8. Issue Book | 9. Return Book | 0. Exit\nEnter choice: ")
        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.remove_book()
        elif choice == "3":
            library.update_book()
        elif choice == "4":
            library.search_book()
        elif choice == "5":
            library.display_books()
        elif choice == "6":
            members.add_member()
        elif choice == "7":
            members.remove_member()
        elif choice == "8":
            members.issue_book(library)
        elif choice == "9":
            members.return_book(library)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
