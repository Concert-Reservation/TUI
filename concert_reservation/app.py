import csv
import sys
import getpass

import requests
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from concert_reservation.domain import Author, Title, Genre, Venue, Rating, Review, ReviewArchive
from concert_reservation.menu import Menu, Description, Entry


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'
    _api_url = 'http://127.0.0.1:8000/api/v1'
    _key=None


    def __init__(self):
        self.__menu = Menu.Builder(Description('Concert Reviews 2024'), auto_select=lambda: None)\
            .with_entry(Entry.create('1', 'Show Reviews', on_selected=lambda: self.__show_reviews()))\
            .with_entry(Entry.create('2', 'Show By Rating', on_selected=lambda: self.__show_sorted_reviews()))\
            .with_entry(Entry.create('3', 'Sign-Up', on_selected=lambda: self.__register()))\
            .with_entry(Entry.create('4','Login',on_selected=lambda : self.__login()))\
            .with_entry(Entry.create('5','Logout',on_selected=lambda :self.__logout()))\
            .with_entry(Entry.create('6','Add Review',on_selected=lambda: self.__add_review()))\
            .with_entry(Entry.create('7','Remove Review',on_selected=lambda: self.__remove_review())) \
            .with_entry(Entry.create('0','Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

        self.__ReviewArchive = ReviewArchive()
        # init mutable state

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty dataset...')

        self.__menu.run()

    def run(self) -> None:
        self.__run()
        #except:
            #print('Panic error!', file=sys.stderr)

    def __load(self) -> None:
        try:
            # Endpoint dell'API per i concerti
            url = f"{self._api_url}/reviews/"
            response = requests.get(url)
            # Controllo dello stato della risposta
            if response.status_code == 200:
                # Converti la risposta JSON in una lista di concerti
                reviews_data = response.json()
                for review in reviews_data:
                    # Estrai e salva ogni campo
                    r = Review(Author(review['author']),
                               Title(review['title']), review['content'], review['genre'],
                               Venue(review['venue']), review['data_concert'], review['data_reviewed'],
                               Rating(review['rating']))
                    self.__ReviewArchive.add_review(r)

                print("Concerti caricati con successo!")
            else:
                print(f"Errore durante il caricamento dei concerti: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Errore di connessione: {e}")
        #if not Path(self.__filename).exists():
            #return

        #with open(self.__filename) as file:
            #reader = csv.reader(file, delimiter=self.__delimiter)
            #for row in reader:
            # validate('row length', row, length=5)
                #...


    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__ReviewArchive.number_of_reviews):
                review = self.__ReviewArchive.review_at_index(index)
                writer.writerow([review.author, review.title, review.content, review.genre, review.venue, review.data_concert, review.data_reviewed, review.rating])


    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    @staticmethod
    def __print_reviews_internal(reviews : list[Review]):
        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-10s %-30s %10s'
        print(fmt % ('#', 'TITLE', 'AUTHOR', 'CONTENT', 'GENRE', 'VENUE', 'DATE_CONCERT', 'DATE_REVIEWED', 'RATING'))
        print_sep()
        for index, review in enumerate(reviews):
            print(fmt % (index + 1, review.title, review.author, review.content, review.genre, review.venue, review.data_concert, review.data_reviewed, review.rating))
        print_sep()

    def __show_review(self):
        reviews = [self.__ReviewArchive.review_at_index(index) for index in range(self.__ReviewArchive.number_of_reviews)]
        self.__print_reviews_internal(reviews)

    def __show_sorted_reviews(self):
        reviews = self.__ReviewArchive.sort_by_ascending_rating
        self.__print_reviews_internal(reviews)

    #Da rivedere insieme a client
    def __add_review(self):
        author = self.__read('Author', Author)
        title = self.__read('Title', Title)
        content = self.__read('Content', Content)
        genre = self.__read('Genre', Genre)
        venue = self.__read('Venue', Venue)
        data_concert = self.__read('Date Concert', Date)
        data_reviewed = self.__read('Date Reviewed', Date)
        rating = self.__read('Rating', Rating)

        review = Review(author, title, content, genre, venue, data_concert, data_reviewed, rating)
        self.__ReviewArchive.add_review(review)
        self.__save()

    def __remove_review(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__ReviewArchive.number_of_reviews)
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        self.__ReviewArchive.remove_review(index - 1)
        self.__save()

    def __show_reviews(self):
        reviews = [self.__ReviewArchive.review_at_index(index) for index in
                    range(self.__ReviewArchive.number_of_reviews)]
        self.__print_reviews_internal(reviews)

    def __register(self):
        username = input("Name:")
        email = input("Email:")
        password1 = input('Password:')
        password2 = input('Password confirmation:')
        if password1 != password2:
            print("Passwords don't match! Retry")
            return
        res = requests.post(url=f'{self._api_url}/auth/registration/',
                            data={'username': username, 'email': email, 'password1': password1, 'password2': password2})
        if res.status_code != 201:
            print("Something went wrong. Retry")
            return
        print("Sign-up successful!!")


    def __login(self):
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        res = requests.post(url=f'{self._api_url}/auth/login/', data={'username': username, 'password': password})
        if res.status_code != 200:
            print("Something went wrong. Retry")
            return
        print("Login successful!")
        json = res.json()
        self._key = json['key']

    def __logout(self):
        res = requests.post(url=f'{self._api_url}/auth/logout/', headers={'Authorization': f'Token {self._key}'})
        if res.status_code == 200:
            print('Logged out!')
        else:
            print('Log out failed')
        self._key = None
        print()
