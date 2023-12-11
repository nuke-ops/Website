from django.urls import path
from .views import dice, dice_electron, get_dice_rolls, insert_dice_roll

urlpatterns = [
    path("dice/", dice, name="dice"),
    path("dice/electron", dice_electron, name="dice_electron"),
    path("api/get_dice_rolls/", get_dice_rolls, name="get_dice_rolls"),
    path("api/insert_dice_roll/", insert_dice_roll, name="insert_dice_roll"),
]
