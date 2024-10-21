import unittest
from pydantic import ValidationError
from main import UserCreate, Client, Move


class TestModels(unittest.TestCase):

    def test_user_create(self):
        # Testare creație utilizator valid
        user = UserCreate(username="testuser", password="securepassword")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "securepassword")

        # Testare validare utilizator invalid
        with self.assertRaises(ValidationError):
            UserCreate(username="testuser")  # lipsă de parolă
        with self.assertRaises(ValidationError):
            UserCreate(password="securepassword")  # lipsă de username

    def test_client(self):
        # Testare creație client valid
        client = Client(user_id=1, username="clientuser")
        self.assertEqual(client.user_id, 1)
        self.assertEqual(client.username, "clientuser")

        # Testare validare client invalid
        with self.assertRaises(ValidationError):
            Client(user_id="not_a_number", username="clientuser")  # user_id nu este int
        with self.assertRaises(ValidationError):
            Client(user_id=1)  # lipsă de username

    def test_move(self):
        # Testare creație mutare validă
        move = Move(row=1, col=2)
        self.assertEqual(move.row, 1)
        self.assertEqual(move.col, 2)

        # Testare validare mutare invalidă
        with self.assertRaises(ValidationError):
            Move(row="not_a_number", col=2)  # row nu este int
        with self.assertRaises(ValidationError):
            Move(row=1)  # lipsă de col


if __name__ == "__main__":
    unittest.main()
