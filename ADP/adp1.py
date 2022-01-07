from peewee import *
import datetime
import sys
import os

DATABASE = 'library.db'

db = SqliteDatabase(DATABASE)


class Book(Model):
    title = CharField()
    author = CharField()
    publication = CharField()
    pub_year = IntegerField()
    isbn = CharField()
    num_of_books = IntegerField()

    class Meta:
        database = db


class Member(Model):
    user_id = CharField()
    name = CharField()
    phone_no = CharField()

    class Meta:
        database = db


class IssueHistory(Model):
    user_id = ForeignKeyField(Member, related_name='pets')
    isbn = ForeignKeyField(Book, related_name='library')
    issue_id = CharField()
    issue_date = DateField(default=datetime.datetime.now)
    return_date = DateField()
    current_status = TextField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Book, Member, IssueHistory])


def deinit():
    db.close()


def add_book():

    book_data = Book(
        title=input('Enter the book title: '),
        author=input('Enter the book author: '),
        publication=input('Enter the book publication: '),
        pub_year=input('Enter the year of publication of book: '),
        isbn=input('Enter the ISBN code of book: '),
        num_of_books=input("Enter the number of books having same ISBN: ")
    )
    book_data.save()
    os.system('clear')


def add_member():

    member_data = Member(
        user_id=input('Enter the user_id: '),
        name=input('Enter the member name: '),
        phone_no=input('Enter the phone number of the member: ')
    )
    member_data.save()
    os.system('clear')


def allocate():

    alloc_book_isbn = input('Enter book isbn to be allocated: ')
    if Book.get(Book.isbn == alloc_book_isbn):
        alloc_member_id = input('Enter member id: ')
        if Member.get(Member.user_id == alloc_member_id):
            return_date = input('Enter a date in YYYY-MM-DD format: ')
            year, month, day = map(int, return_date.split('-'))
            return_date = datetime.date(year, month, day)

            if datetime.datetime.now().date() > return_date:
                print('Issueing date cannot be after return date')

            else:
                issue_date = datetime.datetime.now().date()
                issue_id = str(issue_date) + alloc_member_id + str(return_date)
                current_status = 'issued'
                issue_data = IssueHistory(
                    user_id=alloc_member_id,
                    isbn=alloc_book_isbn,
                    issue_id=issue_id,
                    issue_date=issue_date,
                    return_date=return_date,
                    current_status=current_status
                )
                issue_data.save()
                print('This is your issue id: {0}'.format(issue_id))
                print('Your return date is: {0}'.format(return_date))

        else:
            print('user_id entered does not exist')

    else:
        print('ISBN entered is not present in the database')
    os.system('clear')


def de_allocate():

    de_alloc_user_id = input('Enter your user id: ')
    if IssueHistory.get(IssueHistory.user_id == de_alloc_user_id):
        issue_data = IssueHistory.get(IssueHistory.user_id == de_alloc_user_id)
        today_date = datetime.datetime.now().date()
        if today_date <= issue_data.return_date:
            print('Book received')
            current_status = 'returned'

        elif today_date > issue_data.return_date:
            overdue_days = issue_data.return_date - today_date
            fine = 5 * overdue_days
            print("Your fine is Rs.", fine)
            current_status = 'returned'

        else:
            print('This shouldn\'t be happening')
    os.system('clear')


def remove_book():

    book_isbn = input('Enter the ISBN code of the book you want to remove: ')

    book = Book.get(Book.isbn == book_isbn)
    book.delete_instance()

    print('The book with ISBN', book_isbn, 'has been deleted.')
    os.system('clear')


def remove_member():

    rem_member_id = input("Enter member's user id: ")
    member = Member.get(Member.user_id == rem_member_id)
    member.delete_instance()

    print('Member', rem_member_id, 'has been removed.')
    os.system('clear')


def main():
    print("""
            Welcome to Python Library System:
            (a) To add a book
            (b) To add a member
            (c) To allocate a book
            (d) To return a book
            (e) To remove a book from the collection
            (f) To remove a member from the library
    """)

    user_option = input('Enter your choice now: ')
    user_option = user_option.lower()

    if user_option == 'a':
        add_book()

    elif user_option == 'b':
        add_member()

    elif user_option == 'c':
        allocate()

    elif user_option == 'd':
        de_allocate()

    elif user_option == 'e':
        remove_book()

    elif user_option == 'f':
        remove_member()

    elif user_option == 'x':
        print('\nThank you for using Python Library System!')
        sys.exit()

    else:
        print("Invalid choice")

if __name__ == '__main__':
    try:
        create_tables()
        while (True):
            main()
    except KeyboardInterrupt:
        print('\nThank you for using Python Library System!')
        db.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)