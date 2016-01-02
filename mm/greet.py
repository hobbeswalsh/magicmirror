import datetime
import random

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()
cache_time = 60 * 60 * 12  # 12 Hours
GREETINGS = [
    "Hello there, beautiful.",
    "Smile!",
    "You're looking great.",
    "What has two thumbs and is awesome?",
    "Go get 'er, champ!",
    "Ready to greet the day?",
    "I am beautiful. I am whole. I want a cheeseburger.",
    "Deep breath.",
    "Two guys and a turtle walk into a bar...",
    "Atticus loves you.",
    "You are loved.",
    "You are amazing.",
    "You have a loving family.",
    "Are you SURE you want to wear those pants with those shoes?",
]

def get_greeting():
    greeting = cache.get("greeting")
    if greeting is None:
        greeting = {"greeting": random.choice(GREETINGS)}
        cache.set("greeting", greeting, timeout=cache_time)
    return greeting

