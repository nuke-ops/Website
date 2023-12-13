from django.urls import path
from .views import (
    dice,
    dice_electron,
    get_dice_rolls,
    insert_dice_roll,
    mbs_input_page,
    get_mbs,
)

urlpatterns = [
    path("dice/", dice, name="dice"),
    path("dice/electron", dice_electron, name="dice_electron"),
    path("dice/mbs", mbs_input_page, name="mbs_input"),
    path("api/get_dice_rolls/", get_dice_rolls, name="get_dice_rolls"),
    path("api/insert_dice_roll/", insert_dice_roll, name="insert_dice_roll"),
    path("api/get_mbs/", get_mbs, name="get_mbs"),
]
