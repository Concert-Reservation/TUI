import re
from dataclasses import dataclass, InitVar, field
from typing import Any

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern

#content, genre,venue,rating,date,

@dataclass(frozen=True, order=True)
class Author:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate(
            'value',
            self.value,
            min_len=1,
            max_len=20,
            custom=pattern(r'[0-9A-Za-z\s/-]*')
        )

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[0-9A-Za-z\s/-]*'))

    def __str__(self):
        return self.value



@dataclass(frozen=True, order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'Funk,Rock,Metal,Pop,Hip Hop,Country,Blues,Jazz'))

    def __str__(self):
        return self.value



@dataclass(frozen=True, order=True)
class Venue:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z\s/-]*'))

    def __str__(self):
        return self.value

@dataclass(frozen=True, order=True)
class Rating:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=1, max_value=10)

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True, order=True)
class Review:
    author: Author
    title: Title
    content: str #da rivedere
    genre: Genre #da rivedere
    venue: Venue
    data_concert: str #da rivedere
    data_reviewed: str #da rivedere
    rating: Rating

    @staticmethod
    def of(author: str, title:str, content:str, genre:str, venue:str, data_concert:str, data_reviewed:str, rating:int) -> 'Review':
        return Review(Author(author),
                      Title(title),
                      content, Genre(genre), Venue(venue),
                      #Date(data_concert), Date(data_reviewed),
                      Rating(rating))

    def __str__(self):
        return f'{self.author} - {self.title} - {self.content} - {self.genre} - {self.venue} - {self.data_concert} - {self.data_reviewed} - {self.rating}'


@dataclass(frozen=True, order=True)
class ReviewArchive:
    __review: list[Review] = field(default_factory=list, init=False)

    @property
    def number_of_reviews(self) -> int:
        return len(self.__review)

    def review_at_index(self, index: int) -> Review:
        return self.__review[index]

    def review_by_author(self, author: Author) -> list[Review]:
        return list(filter(lambda x: x.author == author, self.__review))

    def add_review(self, review: Review) -> None:
        self.__review.append(review)

    def remove_review(self, review: Review) -> None:
        self.__review.remove(review)

    def sort_by_ascending_rating(self) -> None:
        self.__review.sort(key=lambda review: review.rating)


