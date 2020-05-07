import json
import sys
import pyttsx3
import time
from pydub import AudioSegment
from pydub.playback import play


def play_part(start, duration, m):
    play(m)


def pause(seconds):
    print(f'PAUSE for {seconds} seconds')
    time.sleep(seconds)


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)


def speak(text):
    print(f'SPEAK {text}')
    engine.say(text)
    engine.runAndWait()


def process_plan(p):
    title = p['title']
    music = p['music']
    set_interval = p['set-interval']
    sets = p['sets']
    m = AudioSegment.from_mp3(music)
    play(m)

    speak(f'Stand by for {title}, starting in {set_interval} seconds')

    for s in sets:
        exercises = s['exercises']
        duration = s['duration']
        interval = s['interval']
        repeat = s['repeat']

        speak(f'Exercises will be {exercises}')
        pause(set_interval)

        for i in range(repeat):
            for _ in exercises:
                speak(f'START  {exercises}')
                pause(duration)
                speak(f'Rest for {interval} seconds')
                pause(interval)
            speak(f'End of set, rest for {set_interval} seconds')
            if i < repeat -1:
                pause(set_interval)

    speak(f'Completed {title}')


if __name__ == '__main__':
    plan_name = 'default'
    if len(sys.argv) == 2:
        plan_name = sys.argv[1]

    print(f'Running plan "{plan_name}"')

    with open('plans.json') as fp:
        d = json.load(fp)
        plan = d[plan_name]

    process_plan(plan)

