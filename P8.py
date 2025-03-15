import json
import os

class Book:
    """Class Book     
        Methods
        1. get_book_id
        2. get_title
        3. set_title
        4. get_author
        5. set_author
        6. get_total_copies
        7. set_total_copies
        8. get_available_copies
        9. set_available_copies
    """
    __next_id = 1
    
    def __init__(self, title, author, count, book_id=None):
        if book_id is not None:
            self.__book_id = book_id
            if book_id >= Book.__next_id:
                Book.__next_id = book_id + 1
        else:
            self.__book_id = Book.__next_id
            Book.__next_id += 1
            
        self.__title = title.title()
        self.__author = author.title()
        self.__total_copies = count 
        self.__available_copies = count  
        self.__in_stock = True  

    def get_book_id(self):
        return self.__book_id
    
    def get_title(self):
        return self.__title
    
    def set_title(self, title):
        self.__title = title.title()
    
    def get_author(self):
        return self.__author
    
    def set_author(self, author):
        self.__author = author.title()
    
    def get_total_copies(self):
        return self.__total_copies
    
    def set_total_copies(self, count):
        difference = count - self.__total_copies
        self.__total_copies = count
        self.__available_copies += difference
    
    def get_available_copies(self):
        return self.__available_copies
    
    def set_available_copies(self, count):
        self.__available_copies = count
        
    def to_dict(self):
        """Convert book object to dictionary for JSON serialization"""
        return {
            "book_id": self.__book_id,
            "title": self.__title,
            "author": self.__author,
            "total_copies": self.__total_copies,
            "available_copies": self.__available_copies
        }

class Library:
    """Class Library
        Methods
        1. add_book
        2. remove_book
        3. update_book
        4. display_book
        5. search_book
        6. save_data
        7. load_data
    """
    
    def __init__(self):
        self.__all_books = {}
        self.load_data()

    def add_book(self):
        try:
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            
            while True:
                try:
                    count = int(input("Enter number of copies: "))
                    if count <= 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            book = Book(title, author, count)
            self.__all_books[book.get_book_id()] = book
            print(f"{book.get_title()} by {book.get_author()} added with ID {book.get_book_id()}.")
            self.save_data()
        except Exception as e:
            print(f"Error adding book: {e}")

    def remove_book(self):
        try:
            while True:
                try:
                    book_id = int(input("Enter book ID to remove: "))
                    break
                except ValueError:
                    print("Please enter a valid book ID (number).")
            
            if book_id in self.__all_books:
                removed_book = self.__all_books.pop(book_id)
                print(f"Removed {removed_book.get_title()} by {removed_book.get_author()}.")
                self.save_data()
            else:
                print("Book ID not found.")
        except Exception as e:
            print(f"Error removing book: {e}")

    def update_book(self):
        try:
            while True:
                try:
                    book_id = int(input("Enter book ID to update: "))
                    break
                except ValueError:
                    print("Please enter a valid book ID (number).")
                    
            if book_id in self.__all_books:
                book = self.__all_books[book_id]
                print("What would you like to update? (T/t = title, A/a = author, C/c = copies): ")
                field = input().strip().lower()
                if field == "t":
                    book.set_title(input("Enter new title: "))
                elif field == "a":
                    book.set_author(input("Enter new author: "))
                elif field == "c":
                    while True:
                        try:
                            new_copies = int(input("Enter new total copies: "))
                            if new_copies <= 0:
                                print("Please enter a positive number.")
                                continue
                            break
                        except ValueError:
                            print("Please enter a valid number.")
                    book.set_total_copies(new_copies)
                else:
                    print("Invalid field.")
                self.save_data()
            else:
                print("Book ID not found.")
        except Exception as e:
            print(f"Error updating book: {e}")

    def display_books(self):
        try:
            if not self.__all_books:
                print("\nNo books in the library.")
                return
                
            print("\nAll Books:")
            for book in self.__all_books.values():
                print(f"ID: {book.get_book_id()} | {book.get_title()} by {book.get_author()} | Available: {book.get_available_copies()}/{book.get_total_copies()}")
        except Exception as e:
            print(f"Error displaying books: {e}")

    def search_book(self):
        try:
            search = input("Enter book title or ID to search: ").strip()
            try:
                book_id = int(search)
                book = self.__all_books.get(book_id, None)
                if book:
                    print(f"ID: {book.get_book_id()} | {book.get_title()} by {book.get_author()} | Available: {book.get_available_copies()}/{book.get_total_copies()}")
                else:
                    print("Book ID not found.")
            except ValueError:
                found = False
                for book in self.__all_books.values():
                    if search.lower() in book.get_title().lower():
                        print(f"ID: {book.get_book_id()} | {book.get_title()} by {book.get_author()} | Available: {book.get_available_copies()}/{book.get_total_copies()}")
                        found = True
                if not found:
                    print("Book not found.")
        except Exception as e:
            print(f"Error searching for book: {e}")
    
    def save_data(self):
        """Save library data to a JSON file"""
        try:
            books_data = {}
            for book_id, book in self.__all_books.items():
                books_data[book_id] = book.to_dict()
                
            with open("library_data.json", "w") as file:
                json.dump(books_data, file, indent=4)
            print("Library data saved successfully.")
        except Exception as e:
            print(f"Error saving library data: {e}")
    
    def load_data(self):
        """Load library data from JSON file"""
        try:
            if os.path.exists("library_data.json"):
                with open("library_data.json", "r") as file:
                    books_data = json.load(file)
                
                for book_id_str, book_data in books_data.items():
                    book_id = int(book_id_str)
                    book = Book(
                        book_data["title"], 
                        book_data["author"], 
                        book_data["total_copies"],
                        book_id
                    )
                    book.set_available_copies(book_data["available_copies"])
                    self.__all_books[book_id] = book
                print("Library data loaded successfully.")
            else:
                print("No saved library data found. Starting with empty library.")
        except Exception as e:
            print(f"Error loading library data: {e}")

    def get_book_by_id(self, book_id):
        """Get a book by its ID"""
        return self.__all_books.get(book_id)

class Member:
    """Class Member
        Methods
            1. add_member
            2. remove_member
            3. issue_book
            4. return_book
            5. save_data
            6. load_data
    """
    
    def __init__(self):
        self.__members = {}
        self.__borrowed_books = {}
        self.load_data()

    def add_member(self):
        try:
            name = input("Enter member name: ").strip()
            if not name:
                print("Member name cannot be empty.")
                return
                
            if name not in self.__members:
                self.__members[name] = []
                print(f"Member {name} added.")
                self.save_data()
            else:
                print(f"Member {name} already exists.")
        except Exception as e:
            print(f"Error adding member: {e}")

    def remove_member(self):
        try:
            name = input("Enter member name: ").strip()
            if name in self.__members:
                if not self.__members[name]:
                    del self.__members[name]
                    print(f"Member {name} removed.")
                    self.save_data()
                else:
                    print(f"Member {name} has borrowed books. Please return all books before removing.")
            else:
                print("Member not found.")
        except Exception as e:
            print(f"Error removing member: {e}")

    def issue_book(self, library):
        try:
            member_name = input("Enter member name: ").strip()
            if member_name not in self.__members:
                print("Member not found.")
                return
                
            search_query = input("Enter book title or ID to issue: ").strip()
            book = None
            try:
                book_id = int(search_query)
                book = library.get_book_by_id(book_id)
            except ValueError:
                for b in library._Library__all_books.values():
                    if search_query.lower() in b.get_title().lower():
                        book = b
                        break
            
            if book and book.get_available_copies() > 0:
                book.set_available_copies(book.get_available_copies() - 1)
                self.__members[member_name].append(book.get_book_id())
                print(f"Issued {book.get_title()} to {member_name}.")
                self.save_data()
                library.save_data()
            elif book and book.get_available_copies() == 0:
                print("Book is currently out of stock.")
            else:
                print("Book not found.")
        except Exception as e:
            print(f"Error issuing book: {e}")

    def return_book(self, library):
        try:
            member_name = input("Enter member name: ").strip()
            if member_name not in self.__members or not self.__members[member_name]:
                print("No books to return or member not found.")
                return
                
            print(f"Books borrowed by {member_name}:")
            for book_id in self.__members[member_name]:
                book = library.get_book_by_id(book_id)
                if book:
                    print(f"ID: {book.get_book_id()} | {book.get_title()} by {book.get_author()}")
                
            search_query = input("Enter book ID to return: ").strip()
            try:
                book_id = int(search_query)
                if book_id in self.__members[member_name]:
                    book = library.get_book_by_id(book_id)
                    if book:
                        book.set_available_copies(book.get_available_copies() + 1)
                        self.__members[member_name].remove(book_id)
                        print(f"{member_name} returned {book.get_title()}.")
                        self.save_data()
                        library.save_data()
                    else:
                        print("Book not found in library.")
                else:
                    print("Book not found in member's borrowed list.")
            except ValueError:
                print("Please enter a valid book ID.")
        except Exception as e:
            print(f"Error returning book: {e}")
    
    def save_data(self):
        """Save member data to a JSON file"""
        try:
            with open("members_data.json", "w") as file:
                json.dump(self.__members, file, indent=4)
            print("Member data saved successfully.")
        except Exception as e:
            print(f"Error saving member data: {e}")
    
    def load_data(self):
        """Load member data from JSON file"""
        try:
            if os.path.exists("members_data.json"):
                with open("members_data.json", "r") as file:
                    self.__members = json.load(file)
                print("Member data loaded successfully.")
            else:
                print("No saved member data found. Starting with empty members list.")
        except Exception as e:
            print(f"Error loading member data: {e}")

def main():
    library = Library()
    members = Member()

    while True:
        try:
            print("\nLibrary Management System")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. Update Book")
            print("4. Display Books")
            print("5. Search Book")
            print("6. Add Member")
            print("7. Remove Member")
            print("8. Issue Book")
            print("9. Return Book")
            print("10. Save Data")
            print("0. Exit")
            choice = input("Enter choice: ")
            
            match choice:
                case "1":
                    library.add_book()
                case "2":
                    library.remove_book()
                case "3":
                    library.update_book()
                case "4":
                    library.display_books()
                case "5":
                    library.search_book()
                case "6":
                    members.add_member()
                case "7":
                    members.remove_member()
                case "8":
                    members.issue_book(library)
                case "9":
                    members.return_book(library)
                case "10":
                    library.save_data()
                    members.save_data()
                case "0":
                    print("Saving data before exit...")
                    library.save_data()
                    members.save_data()
                    print("Program exited.")
                    break
                case _:
                    print("Invalid choice, try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()