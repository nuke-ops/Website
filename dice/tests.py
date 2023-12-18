from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from dice.consumers import DiceConsumer
import json


class DiceTestCase(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.valid_data = {
            "name": "TestName",
            "dice": 2,
            "sides": 8,
            "modifier": "str(+2)",
        }

    def setUp(self):
        self.client = Client()

    def test_insert_dice_roll_api(self):
        response = self.client.post("/api/insert_dice_roll/", data=self.valid_data)
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertEqual(response_data["message"], "Dice roll inserted successfully")
        print(f"\ninsert_dice: {response_data['message']}")

    def test_get_dice_rolls_api(self):
        self.client.post("/api/insert_dice_roll/", data=self.valid_data)
        response = self.client.get("/api/get_dice_rolls/")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        print(f"\nget_dice: {response_data}")
