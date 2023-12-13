import json
import os
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dice.models import Dice
from nukeops.settings import MEDIA_ROOT


def dice(request):
    return render(request, "dice.html")


def dice_electron(request):
    return render(request, "dice_electron.html")


@csrf_exempt
def insert_dice_roll(request):
    if request.method == "POST":
        data = json.loads(request.body)
        dice_roll = Dice(
            name=data["name"],
            dice=data["dice"],
            sides=data["sides"],
            throws=data["throws"],
            sum=data["sum"],
            modifier=data["modifier"],
        )
        dice_roll.save()
        return JsonResponse({"message": "Dice roll inserted successfully"})
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)


def get_dice_rolls(request):
    dice_records = Dice.objects.all().order_by("-id")[:10].values()
    dice_records_dict = {record["id"]: record for record in dice_records}
    return JsonResponse(dice_records_dict)


def receive(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dice_roll_group",
        {
            "type": "update.dice_roll",
            "message": "A new dice roll has occurred!",
        },
    )


mbsTxt_path = os.path.join(MEDIA_ROOT, "mbs.txt")


@login_required
def mbs_input_page(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        with open(mbsTxt_path, "w") as file:
            file.write(content)

    with open(mbsTxt_path, "r") as file:
        notes = "".join(file.readlines()).replace("\n\n", "\n")

    return render(request, "mbs.html", {"notes": notes})


last_random_note = {}


def get_mbs(request):
    global last_random_note
    if "refresh" in request.GET:
        with open(mbsTxt_path, "r") as file:
            notes = "".join(file.readlines()).replace("\n\n", "\n").split("\n")
            notes_list = []
            for item in notes:
                parts = item.split(". ", 1)
                if len(parts) == 2:
                    key, value = parts
                    notes_list.append({"key": key, "value": value})
            last_random_note = random.choice(notes_list)
    return JsonResponse(last_random_note)
