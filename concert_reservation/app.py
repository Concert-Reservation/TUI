import csv
import sys
import requests
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from concert_reservation.domain import Date,Client,Title,Concert,Reservation,Id
from concert_reservation.menu import Menu, Description, Entry


class App:
    #__filename = Path(__file__).parent.parent / 'default.csv'
    #__delimiter = '\t'
    api_url = 'http://127.0.0.1:8000/api/v1'


    def __init__(self):
        self.__menu = Menu.Builder(Description('Concert Reservation'), auto_select=lambda: None)\
            .with_entry(Entry.create('1','Show Concerts',on_selected=lambda: self.__show_concerts()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .build()
        self.__reservation=Reservation()
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
            url = f"{self.api_url}/concerts/"
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


    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
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
    def __print_concerts_internal(concerts):
        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-10s %-30s %10s'
        print(fmt % ('#', 'TITLE', 'DATE', 'CLIENT'))
        print_sep()
        for index, concert in enumerate(concerts):
            print(fmt % (index + 1, concert.title, concert.date, concert.client))
        print_sep()

    def __show_concerts(self):
        concerts = [self.__reservation.concert_at_index(index) for index in range(self.__reservation.number_of_concerts)]
        self.__print_concerts_internal(concerts)