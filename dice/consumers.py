import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "dice_roll_group"
        await self.accept()
        await self.channel_layer.group_add("dice_roll_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dice_roll_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        message = list(json.loads(text_data).keys())[0]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "update_dice_roll", "message": message}
        )

    async def update_dice_roll(self, event):
        message = event["message"]
        await self.send(json.dumps({"message": message}))
