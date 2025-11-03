import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


@pytest.mark.parametrize("book_name", ["Гарри Поттер", "Властелин колец"])
def test_add_new_book_added_successfully(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name in collector.get_books_genre()
    assert collector.get_book_genre(book_name) == ''


@pytest.mark.parametrize("invalid_name", ["", "А" * 41])
def test_add_new_book_invalid_name_not_added(collector, invalid_name):
    collector.add_new_book(invalid_name)
    assert invalid_name not in collector.get_books_genre()


def test_set_book_genre_valid_genre_is_set(collector):
    collector.add_new_book('Гарри Поттер')
    collector.set_book_genre('Гарри Поттер', 'Фантастика')
    assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'


def test_set_book_genre_invalid_genre_not_set(collector):
    collector.add_new_book('Книга 1')
    collector.set_book_genre('Книга 1', 'Драма')
    assert collector.get_book_genre('Книга 1') == ''


def test_get_books_with_specific_genre_returns_correct_list(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.set_book_genre('Книга 1', 'Комедии')
    collector.set_book_genre('Книга 2', 'Фантастика')
    result = collector.get_books_with_specific_genre('Комедии')
    assert result == ['Книга 1']


def test_get_books_genre_returns_full_dictionary(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    expected = {'Книга 1': '', 'Книга 2': ''}
    assert collector.get_books_genre() == expected


def test_get_books_for_children_excludes_age_restricted(collector):
    collector.add_new_book('Оно')
    collector.add_new_book('Шерлок Холмс')
    collector.add_new_book('Мадагаскар')
    collector.set_book_genre('Оно', 'Ужасы')
    collector.set_book_genre('Шерлок Холмс', 'Детективы')
    collector.set_book_genre('Мадагаскар', 'Мультфильмы')
    result = collector.get_books_for_children()
    assert result == ['Мадагаскар']


def test_add_book_in_favorites_adds_only_once(collector):
    collector.add_new_book('Гарри Поттер')
    collector.add_book_in_favorites('Гарри Поттер')
    collector.add_book_in_favorites('Гарри Поттер')
    assert collector.get_list_of_favorites_books() == ['Гарри Поттер']


def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book('Книга 1')
    collector.add_book_in_favorites('Книга 1')
    collector.delete_book_from_favorites('Книга 1')
    assert 'Книга 1' not in collector.get_list_of_favorites_books()


def test_get_list_of_favorites_books_returns_correct_list(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.add_book_in_favorites('Книга 1')
    result = collector.get_list_of_favorites_books()
    assert result == ['Книга 1']