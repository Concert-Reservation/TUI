import pytest
from valid8 import ValidationError


from concert_reservation.domain import Author, Title, Genre, Venue, Rating, Review, Content, Date, ReviewArchive

#test Genre

def test_genre_valid():
    assert Genre('Rock').value == 'Rock'

def test_genre_invalid():
    with pytest.raises(ValidationError):
        Genre(value='Classicistik')

#test rating

def test_rating_valid():
    assert Rating(5).value == 5

def test_rating_invalid():
    with pytest.raises(ValidationError):
        Rating(value=11 or 0 or -1)



#test review

def test_review_factory_method_of():
    assert Review.of('Author', 'Title', 'Content', 'Hip Hop', 'Venue', '2024-12-01', '2024-12-05', 5).rating == Rating(5)

def test_review_archive_starts_with_empty_list():
    assert ReviewArchive().number_of_reviews() == 0


def test_review_archive_can_add_review():
    review_archive = ReviewArchive()
    assert review_archive.number_of_reviews() == 0
    review_archive.add_review(Review.of('Author', 'Title', 'Content', 'Rock', 'Venue', '2024-12-01', '2024-12-05', 5))
    assert review_archive.number_of_reviews() == 1


def test_review_archive_can_remove_review():
    review_archive = ReviewArchive()
    assert review_archive.number_of_reviews() == 0
    review_archive.add_review(Review.of('Author 1', 'Title', 'Content', 'Jazz', 'Venue', '2024-12-01', '2024-12-05', 5))
    assert review_archive.number_of_reviews() == 1
    review_archive.remove_review(review_archive.review_at_index(0))
    assert review_archive.number_of_reviews() == 0


def test_review_archive_can_access_review():
    review = Review.of('Author', 'Title', 'Content', 'Funk', 'Venue', '2024-12-01', '2024-12-05', 5)
    review_archive = ReviewArchive()
    review_archive.add_review(review)
    assert review_archive.review_at_index(0) == review


def test_review_archive_can_access_review_by_author():
    review_archive = ReviewArchive()
    review_archive.add_review(Review.of('Author 1', 'Title', 'Content', 'Hip Hop', 'Venue', '2024-12-01', '2024-12-05', 5))
    review_archive.add_review(Review.of('Author 2', 'Title', 'Content', 'Hip Hop', 'Venue', '2024-12-01', '2024-12-05', 5))
    review_archive.add_review(Review.of('Author 3', 'Title', 'Content', 'Blues', 'Venue', '2024-12-01', '2024-12-05', 5))
    assert {review.author.value for review in review_archive.review_by_author(Author('Author 1'))} == {'Author 1'}


def test_review_archive_review_of_author():
    review_archive = ReviewArchive()
    review_archive.add_review(Review.of('Author 1', 'Title', 'Content', 'Blues', 'Venue', '2024-12-01', '2024-12-05', 5))
    review_archive.add_review(Review.of('Author 2', 'Title', 'Content', 'Hip Hop', 'Venue', '2024-12-01', '2024-12-05', 5))
    review_archive.add_review(Review.of('Author 1', 'Title', 'Content', 'Metal', 'Venue', '2024-12-01', '2024-12-05', 5))
    assert len(review_archive.review_by_author(Author('Author 1'))) == 2
    assert len(review_archive.review_by_author(Author('Author 2'))) == 1


def test_review_archive_order_by_rating():
    review_archive = ReviewArchive()
    reviews = [
        Review.of('Author 2', 'Title 2', 'Content', 'Hip Hop', 'Venue', '2024-12-01', '2024-12-05', 4),
        Review.of('Author 1', 'Title 1', 'Content', 'Blues', 'Venue', '2024-12-01', '2024-12-05', 5),
        Review.of('Author 1', 'Title 3', 'Content', 'Jazz', 'Venue', '2024-12-01', '2024-12-05', 3),
    ]
    for review in reviews:
        review_archive.add_review(review)
    review_archive.sort_by_ascending_rating()
    assert review_archive.review_at_index(0) == reviews[1]
    assert review_archive.review_at_index(1) == reviews[0]
    assert review_archive.review_at_index(2) == reviews[2]



















