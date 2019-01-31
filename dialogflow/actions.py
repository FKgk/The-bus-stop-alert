import random
from django.template.loader import render_to_string
from .bus import get_bus, status_change, set_start_number


def bus_search(start, terminate, number, chat_id):
    return get_bus(start, terminate, number, chat_id)

def bus_cancel(telegram_chat_id):
    return status_change(telegram_chat_id)

def alarm_search(telegram_chat_id, terminate):
    return set_start_number(telegram_chat_id, terminate)