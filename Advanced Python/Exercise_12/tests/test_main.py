import unittest
from database import session, Film
import requests


class TestMain(unittest.TestCase):
    """
    This class contains unit tests for direct database operations.
    It tests adding, updating, and deleting films in the database.
    """

    sample_film: Film

    def setUp(self) -> None:
        """
        Setup method to add a sample film entry to the database.
        This ensures each test starts with a consistent state.
        """
        self.sample_film = Film(title="Memento_Test", year_of_creation=1999)
        session.add(self.sample_film)
        session.commit()

    def tearDown(self) -> None:
        """
        Tear down method to clean up the database after each test.
        Deletes all entries from the Film table to reset the state.
        """
        session.query(Film).delete()
        session.commit()

    def test_add_film(self) -> None:
        """
        Test for adding a new film to the database.
        Asserts that the number of films in the database increases by one.
        """
        new_film: Film = Film(title="Insomnia", year_of_creation=2002)
        session.add(new_film)
        session.commit()
        self.assertEqual(session.query(Film).count(), 2)

    def test_update_film(self) -> None:
        """
        Test for updating a film in the database.
        Asserts that the title of the sample film is updated successfully.
        """
        self.sample_film.title = "Inception"
        session.commit()
        updated_film: Film | None = session.query(Film).filter_by(id=self.sample_film.id).first()
        if updated_film is not None:
            self.assertEqual(updated_film.title, "Inception")
        else:
            self.fail("Updated film not found")

        self.assertIsNotNone(updated_film)
        self.assertEqual(updated_film.title, "Inception")

    def test_delete_film(self) -> None:
        """
        Test for deleting a film from the database.
        Asserts that the number of films in the database decreases by one.
        """
        session.delete(self.sample_film)
        session.commit()
        self.assertEqual(session.query(Film).count(), 0)


API_URL: str = "http://127.0.0.1:5000"


class TestAPI(unittest.TestCase):
    """
    This class contains unit tests for API endpoints.
    It tests creating, reading, updating, and deleting films via the API.
    """

    sample_film_id: int

    def setUp(self) -> None:
        """
        Setup method to create a sample film entry using the API.
        Ensures each test starts with a consistent state.
        """
        payload: dict[str, int | str] = {"title": "Memento_Test_API", "year_of_creation": 1999}
        response: requests.Response = requests.post(f"{API_URL}/films", json=payload)

        self.sample_film_id = response.json().get("id", -1)
        self.assertNotEqual(self.sample_film_id, -1,
                            "Failed to create a sample film for API tests")

    def tearDown(self) -> None:
        """
        Tear down method to delete all films using the API.
        Ensures the API state is reset after each test.
        """
        response: requests.Response = requests.get(f"{API_URL}/films")
        films: list[dict[str, int | str]] = response.json()

        for film in films:
            requests.delete(f"{API_URL}/films/{film['id']}")

    def test_post_film(self) -> None:
        """
        Test for creating a new film using the API.
        Asserts that the response indicates successful creation.
        """
        payload: dict[str, int | str] = {"title": "Insomnia_API", "year_of_creation": 2002}
        response: requests.Response = requests.post(f"{API_URL}/films", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn("Film created successfully", response.json()["message"])

    def test_get_films(self) -> None:
        """
        Test for retrieving all films using the API.
        Asserts that the sample film is present in the response.
        """
        response: requests.Response = requests.get(f"{API_URL}/films")
        self.assertEqual(response.status_code, 200)

        films: list[dict[str, int | str]] = response.json()
        self.assertGreater(len(films), 0)
        self.assertTrue(
            any(film["id"] == self.sample_film_id for film in films))

    def test_update_film_api(self) -> None:
        """
        Test for updating a film using the API.
        Asserts that the response indicates successful update and
        the updated data is reflected in the database.
        """
        payload: dict[str, int | str] = {"title": "Inception", "year_of_creation": 2010}
        response_1: requests.Response = requests.put(
            f"{API_URL}/films/{self.sample_film_id}",
            json=payload)

        self.assertEqual(response_1.status_code, 200)
        self.assertIn("Film updated successfully", response_1.json()["message"])

        response_2: requests.Response = requests.get(f"{API_URL}/films/{self.sample_film_id}")
        updated_film: dict[str, int | str] = response_2.json()

        self.assertEqual(updated_film["title"], "Inception")
        self.assertEqual(updated_film["year_of_creation"], 2010)

    def test_delete_film_api(self) -> None:
        """
        Test for deleting a film using the API.
        Asserts that the response indicates successful deletion and
        the deleted film is no longer accessible.
        """
        delete_response : requests.Response = requests.delete(f"{API_URL}/films/{self.sample_film_id}")
        self.assertEqual(delete_response .status_code, 200)
        self.assertIn("Film deleted successfully", delete_response .json()["message"])

        get_response : requests.Response = requests.get(f"{API_URL}/films/{self.sample_film_id}")
        self.assertEqual(get_response .status_code, 404)


if __name__ == "__main__":
    unittest.main()


"""
unittest: python -m unittest discover -s tests 
"""