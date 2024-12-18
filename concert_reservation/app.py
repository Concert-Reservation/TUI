import csv
import sys
import getpass

import requests
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from concert_reservation.domain import Date,Client,Title,Concert,Reservation,Id
from concert_reservation.menu import Menu, Description, Entry


class App:
    #__filename = Path(__file__).parent.parent / 'default.csv'
    #__delimiter = '\t'
    _api_url = 'http://127.0.0.1:8000/api/v1'
    _key=None


    def __init__(self):
        self.__menu = Menu.Builder(Description('Concert Reservation'), auto_select=lambda: None)\
            .with_entry(Entry.create('1','Show Concerts',on_selected=lambda: self.__show_concerts()))\
            .with_entry(Entry.create('2', "Sign-Up", on_selected=lambda: self.__register()))\
            .with_entry(Entry.create('3','Login',on_selected=lambda : self.__login()))\
            .with_entry(Entry.create('4','Logout',on_selected=lambda :self.__logout()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .with_entry(Entry.create('2','Add Reservation',on_selected=lambda: self.__add_reservation()))\
            .with_entry(Entry.create('3','Remove Reservation',on_selected=lambda: self.__remove_reservation()))\
            .build()

        self.__concert=Concert()#Da cambiare
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
            url = f"{self._api_url}/concerts/"
            response = requests.get(url)
            # Controllo dello stato della risposta
            if response.status_code == 200:
                # Converti la risposta JSON in una lista di concerti
                concerts_data = response.json()
                for concert in concerts_data:
                    # Estrai e salva ogni campo
                    c=Concert(title=Title(concert['title']),id=Id(concert['id']),date=Date(concert['date']),client=Client(concert['client']))
                    self.__reservation.add_concert(c)

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


    #def __save(self) -> None:
        #with open(self.__filename, 'w') as file:
            #writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            # for index in range(self.__dealer.vehicles()):
            #     vehicle = self.__dealer.vehicle(index)
            #     writer.writerow([vehicle.type, vehicle.plate, vehicle.producer, vehicle.model, vehicle.price])

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
    def __print_reservations_internal(reservations):
        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-10s %-30s %10s'
        print(fmt % ('#', 'TITLE', 'DATE', 'CLIENT'))
        print_sep()
        for index, reservation in enumerate(reservations):
            print(fmt % (index + 1, reservation.title, reservation.date, reservation.client))
        print_sep()

    def __show_reservation(self):
        reservations = [self.__concert.reservation_at_index(index) for index in range(self.__concert.number_of_reservation)]
        self.__print_reservations_internal(reservations)

    #Da rivedere insieme a client
    def __add_reservation(self): #id, client, title, date
        client = self.__read('Client', Client)
        title = self.__read('Title', Title)
        date = self.__read('Date', Date)

        reservation = Reservation(client, title, date)
        self.__concert.add_reservation(reservation)
        self.__save()

    def __remove_reservation(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__concert.number_of_reservation)
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        self.__concert.remove_reservation(index - 1)
        self.__save()
