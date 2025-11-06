import pytest

class TestAddBook:
    @pytest.mark.parametrize("book_name", ["Гарри Поттер", "Властелин колец"])
    def test_add_new_book_added_successfully(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()
        assert collector.get_book_genre(book_name) == ''

    def test_add_new_book_invalid_name_not_added(self, collector):
        collector.add_new_book("")
        collector.add_new_book("x" * 41)
        assert "" not in collector.get_books_genre()
        assert "x" * 41 not in collector.get_books_genre()

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Книга Дубль")
        collector.add_new_book("Книга Дубль")
        assert len(collector.get_books_genre()) == 1


class TestGenres:
    def test_set_book_genre_valid_genre_is_set(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_book_genre("Гарри Поттер") == "Фантастика"

    def test_set_book_genre_invalid_genre_not_set(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Роман")
        assert collector.get_book_genre("Книга") == ""

    def test_get_book_genre_returns_genre(self, collector):
        collector.add_new_book("Книга A")
        collector.set_book_genre("Книга A", "Комедии")
        genre = collector.get_book_genre("Книга A")
        assert genre == "Комедии"

    def test_get_books_with_specific_genre_returns_correct_list(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 1", "Комедии")
        collector.set_book_genre("Книга 2", "Фантастика")
        result = collector.get_books_with_specific_genre("Комедии")
        assert result == ["Книга 1"]

    def test_get_books_for_children_excludes_age_restricted(self, collector):
        collector.add_new_book("Оно")
        collector.add_new_book("Мадагаскар")
        collector.set_book_genre("Оно", "Ужасы")
        collector.set_book_genre("Мадагаскар", "Мультфильмы")
        children_books = collector.get_books_for_children()
        assert "Мадагаскар" in children_books
        assert "Оно" not in children_books


class TestFavorites:
    def test_add_book_in_favorites_adds_only_once(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert collector.get_list_of_favorites_books() == ["Гарри Поттер"]

    def test_add_book_in_favorites_does_not_add_unknown_book(self, collector):
        collector.add_book_in_favorites("Неизвестная книга")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book("Книга для избранного")
        collector.add_book_in_favorites("Книга для избранного")
        collector.delete_book_from_favorites("Книга для избранного")
        assert "Книга для избранного" not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_returns_correct_list(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        assert collector.get_list_of_favorites_books() == ["Книга 1", "Книга 2"]


class TestGetBooksGenre:
    def test_get_books_genre_returns_all_books(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        result = collector.get_books_genre()
        assert isinstance(result, dict)
        assert "Книга 1" in result
        assert "Книга 2" in result

