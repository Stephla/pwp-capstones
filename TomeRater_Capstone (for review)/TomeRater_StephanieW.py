class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    #Returns email associated with user
    def get_email(self):
        return self.email

    #Takes in new email and changes email accociated with user (and prints message saying email is updated)
    def change_email(self, address):
        self.email = address
        print("The email adress of {user} is updated to {email}.".format(user=self.name, email=self.email))
        
    #Returns string to print out user object in meaningful way
    def __repr__(self):
        return "Name: {name}, email: {email}, books read: {books}.".format(name=self.name, email=self.email, books=len(self.books))

    #Defines comparison between users (same name/email)
    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False

    #Adds key:value pair to self.books where the key is book and the value is rating
    def read_book(self, book, rating=None):
        self.books[book] = rating

    #get_average_rating method
    def get_average_rating(self):
        sum_ratings = 0
        number_of_ratings = 0
        for value in self.books.values():
            if value:
                sum_ratings += value
                number_of_ratings += 1
        average = sum_ratings / number_of_ratings
        return average

    #__hash__ to make user hashable
    def __hash__(self):
        return hash((self.name, self.email))

class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    #Returns title of the book
    def get_title(self):
        return self.title

    #Returns ISBN of the book
    def get_isbn(self):
        return self.isbn

    #Update ISBN and return message
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "The ISBN of \"{book}\" has been succesfully updated to {isbn}".format(book=self.title, isbn=self.isbn)

    #add rating to self.ratings if between 0-4
    def add_rating(self, rating):
        if rating:
            if (rating >= 0) and (rating <= 4):
                self.ratings.append(rating)
                return self.ratings
            else:
                print("Invalid Rating")

    #__eq__
    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    #get_average_rating
    def get_average_rating(self):
        sum_ratings = 0
        for rating in self.ratings:
            sum_ratings += rating
        try:
            average = sum_ratings / len(self.ratings)
        except ZeroDivisionError:
            print("There are no ratings yet")
        return average

    #__hash__ to make book hashable
    def __hash__(self):
        return hash((self.title, self.isbn))

#Fiction Subclass of Book (inherits from Book)
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    #Returns author
    def get_author(self):
        return self.author

    #__repr__
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

#Non-Fiction Subclass of Book (inherits from Book)
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    #Returns subject
    def get_subject(self):
        return self.subject

    #Returns level
    def get_level(self):
        return self.level

    #__repr__
    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)    

#Class TomeRater
class TomeRater:
    def __init__(self):
        #maps a user’s email to the corresponding User object
        self.users = {}
        #maps a Book object to the number of Users that have read it
        self.books = {}

    #creates a new book with that title and ISBN. Returns this Book object.
    def create_book(self, title, isbn):
        book = Book(title, isbn)
        return book

    #creates a new Fiction with that title, author and ISBN. Returns this Fiction object.
    def create_novel(self, title, author, isbn):
        novel = Fiction(title, author, isbn)
        return novel

    #creates a new Non_Fiction with that title, author and ISBN. Returns this Non_Fiction object.
    def create_non_fiction(self, title, subject, level, isbn):
        non_fiction = Non_Fiction(title, subject, level, isbn)
        return non_fiction

    #add_book_to_user
    def add_book_to_user(self, book, email, rating=None):
        #It should get the user in self.users with the key email
        user = self.users.get(email)
        if user:
            #Call read_book on this user, with book and rating
            user.read_book(book, rating)
            if book not in self.books:
                #add the key book to self.books with a value of 1 (because one user has read it)
                self.books[book] = 1
            else:
                #increase the value of it in self.books by 1, because one more user has read it.
                self.books[book] += 1 
            #Call add_rating on book, with rating
            book.add_rating(rating)
        else:
            print("No user with email {email}!".format(email=email))

    #add_user
    def add_user(self, name, email, user_books=None):
        new_user = User(name, email)
        self.users[email] = new_user
        #adds each book to the user (using theTomeRater method add_book_to_user)
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    #Iterates through all of the keys in self.books (which are Book objects), and prints them
    def print_catalog(self):
        for keys in self.books:
            print(keys)

    #Iterates through all of the values of self.users (which are the User objects), and prints them
    def print_users(self):
        for values in self.users.values():
            print(values)

    #Iterate through all of the books in self.books and return the book that has been read the most.
    def most_read_book(self):
        most_read = None
        max_number_reads = float("-inf")
        for book in self.books:
            read_count = self.books[book]
            if read_count > max_number_reads:
                max_number_reads = read_count
                most_read = book
        return most_read

    #Iterate through all of the books in self.books and return the book that has the highest average rating. 
    def highest_rated_book(self):
        highest_book = ""
        highest_rating = float("-inf")
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_book = book
        return highest_book

    #Iterate through all of the users in self.users and return the user that has the highest average rating. 
    def most_positive_user(self):
        positive_user = None
        highest_rating = float("-inf")
        for user in self.users.values():
            user_avg = user.get_average_rating()
            if user_avg > highest_rating:
                highest_rating = user_avg
                positive_user = user
        return positive_user

    ##Finally, add sophisticated method of choice:
    #Return the n books that have been read most, in descending order
    def get_n_most_read_books(self, n):
        most_read_books = {}
        for book in self.books:
            read_count = self.books[book]
            most_read_books[book] = read_count
        sorted_books_by_value = sorted(most_read_books.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_books_by_value[0:n]

    #Return the n readers that have read the most books, in descending order
    def get_n_most_prolific_readers(self, n):
        most_prolific = {}
        for user in self.users.values():
            book_count = len(user.books)
            most_prolific[user.name] = book_count
        sorted_readers_by_books = sorted(most_prolific.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_readers_by_books[0:n]
