import os
import datetime

def get_user_mood():
    valid_moods = {
        "happy": 2,
        "relaxed": 1,
        "apathetic": 0,
        "sad": -1,
        "angry": -2
    }

    while True:
        mood = input("Enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if mood in valid_moods:
            return valid_moods[mood]
        else:
            print("Invalid mood. Please try again.")

def store_mood(mood):
    date_today = datetime.date.today().isoformat()
    with open('data/mood_diary.txt', 'a') as file:
        file.write(f"{date_today},{mood}\n")

def has_already_entered_today():
    date_today = datetime.date.today().isoformat()
    if os.path.exists('data/mood_diary.txt'):
        with open('data/mood_diary.txt', 'r') as file:
            for line in file:
                if line.startswith(date_today):
                    return True
    return False

def diagnose_mood():
    with open('data/mood_diary.txt', 'r') as file:
        lines = file.readlines()

    if len(lines) < 7:
        return None

    recent_moods = [int(line.split(',')[1]) for line in lines[-7:]]

    mood_count = {
        2: 0,
        1: 0,
        0: 0,
        -1: 0,
        -2: 0
    }

    for mood in recent_moods:
        mood_count[mood] += 1

    if mood_count[2] >= 5:
        return "manic"
    if mood_count[-1] >= 4:
        return "depressive"
    if mood_count[0] >= 6:
        return "schizoid"

    average_mood = round(sum(recent_moods) / 7)
    mood_names = {
        2: "happy",
        1: "relaxed",
        0: "apathetic",
        -1: "sad",
        -2: "angry"
    }
    return mood_names.get(average_mood, "unknown")

def assess_mood():
    if has_already_entered_today():
        print("Sorry, you have already entered your mood today.")
        return

    mood = get_user_mood()
    store_mood(mood)

    diagnosis = diagnose_mood()
    if diagnosis:
        print(f"Your diagnosis: {diagnosis}!")
