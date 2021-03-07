from datetime import datetime
import subprocess
import speech_recognition as sr
import playsound
import wikipedia
import webbrowser
import os

assistant_name = "jarvis"
activation_phrase = "Jarvis"
retry_limit = 3


def rep_listen():
    """
    To listen the user's command, retry_limit number of times.

    If unable to transcibe the user's command successfully,
    retry to take and transcribe the command, retry_limit number
    of time.

    Parameters: None

    Returns: string
        "retry" - if unsuccessful in transcribing the user's command, retry_limit
                number of times
        "error" - if unable to call api
        command - user's command transcription
    """
    for i in range(retry_limit):
        command = listen()
        if not(command == "retry"):
            break

    return command


def activate():
    """
    To activate the virtual assistant to take the command and perform the task.

    Parameters: None

    Returns: None
    """
    playsound.playsound("sounds/activation_sound.mp3")
    command = rep_listen()

    if (command == "retry") or (command == "error"):
        responce = "Unable to process your request at the moment. Try Again later."
        speak(responce)
        command = "error_is_generated"

    analyze_command(command)


def quit():
    """
    To close the program

    Parameters: None

    Returns: None
    """
    playsound.playsound("sounds/quitting_sound.mp3")
    exit()


def speak(text_input):
    """
    To make the system speak

    Parameters:
    text_input(string): Responce in text format, which the system has to speak.

    Returns: None
    """
    subprocess.call(["say", text_input])


def unable_to_recognize():
    """
    To inform the user about transcription issue

    Parameters: None

    Returns: None
    """
    playsound.playsound("sounds/error_sound.mp3")
    responce = "I am sorry, I didn't get that. Please Try Again."
    speak(responce)


def api_error():
    """
    To inform the user about network error issue.

    Parameters: None

    Returns: None
    """
    playsound.playsound("sounds/error_sound.mp3")
    responce = "Unable to process information. Network Error. Try Again After sometime."


def listen():
    """
    To listen to the user's command.

    Parameters: None

    Returns:
        string: user's command transcription in lowercase.
    """
    recog = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recog.adjust_for_ambient_noise(source)
            audio = recog.listen(source)

        transcription = recog.recognize_google(audio)
        playsound.playsound("sounds/input_taken.mp3")
    except sr.RequestError:
        api_error()
        transcription = "error"
    except sr.UnknownValueError:
        unable_to_recognize()
        transcription = "retry"

    return transcription.lower()


def passive_mode():
    """
    To get the user's input but to ignore everything, except the activation phrase.

    When the activation phrase is said, the assitant goes into active mode and reponds
    to user's command.

    Parameters: None

    Returns: None
    """
    while True:
        command = passive_listening()
        if(activation_phrase.lower() in command):
            activate()


def passive_listening():
    """
    To take the input from the microphone but doesn't respond to any errors,
    except the KeyboardInterrupt error(which is handled to exit the program).

    Parameters: None

    Returns:
    string - transcription of user's input
    """
    recog = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recog.adjust_for_ambient_noise(source)
            audio = recog.listen(source)

        transcription = recog.recognize_google(audio)
    except KeyboardInterrupt:
        quit()
    except:
        transcription = ""
        pass

    return transcription.lower()


def volume_options(command):
    """
    To return a value based on some predefined values

    Parameters:
    command(string): Filtered version of user's command, which contains
        the value or string which refers to the volume level

    Returns:
    int - This represents the volume level
    """
    if command == "low":
        return 25
    elif command == "high":
        return 75
    elif command == "full":
        return 100
    elif command == "medium":
        return 50
    elif command == "retry":
        responce = "Unable to process the information. Try Again Later."
        speak(responce)
        return -1
    else:
        command = int(command)
        if command > 100:
            command = 75

        if command < 0:
            command = 10

        return command


def analyze_command(command):
    """
    To analyze the user's command and perform some action based on that.

    Parameters:
    command(string) - User's command in text form.

    Returns: None
    """
    if command == "error_is_generated":
        pass

    elif "introduce yourself" in command or "who are you" in command:
        responce = (
            "Hi, This is {name}. I am a virtual assistant, developed by "
            "Abhinav Kapoor, on 7 March 2021. "
            "I can perform some basic operations like: "
            "Searching web "
            "Opening and closing applications "
            "and some more. Refer to readme file for more information"
        ).format(name=assistant_name)
        speak(responce)

    elif "wikipedia" in command:
        command = command.replace("on wikipedia", "")
        command = command.replace("search for", "")
        command = command.strip()
        results = wikipedia.summary(command, sentences=2)
        speak("According to wikipedia, " + results)

    elif command == "quit" or command == "shut down" or command == "shutdown":
        quit()

    elif "search web" in command:
        responce = "What should i search for?"
        speak(responce)
        command = listen()
        if command.startswith("search"):
            command = command.replace("search", "")
        elif command.startswith("search for"):
            command = command.replace("search for", "")

        command = command.strip()
        word_list = command.split(" ")
        command = "+".join(word_list)
        responce = "Here's what i found on the web"
        speak(responce)
        url = f"https://www.google.com/search?q={command}"
        webbrowser.open(url=url)

    elif "search" in command or "find" in command:
        if command.startswith("search for"):
            command = command.replace("search for", "")
        elif command.startswith("find") or command.endswith("find"):
            command = command.replace("find", "")
        elif command.startswith("search") or command.endswith("search"):
            command = command.replace("search", "")

        if "on youtube" in command:
            command = command.replace("on youtube", "")
            command.strip()
            command = command.replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={command}"
        else:
            command = command.strip()
            command = command.replace(" ", "+")
            url = f"https://www.google.com/search?q={command}"

        webbrowser.open(url=url)

    elif "open youtube" in command:
        responce = "opening youtube"
        speak(responce)
        url = "https://www.youtube.com"
        webbrowser.open(url=url)

    elif "open facebook" in command:
        responce = "opening facebook"
        speak(responce)
        url = "https://www.facebook.com"
        webbrowser.open(url=url)

    elif "open amazon prime" in command:
        responce = "opening amazon prime"
        speak(responce)
        url = "https://www.primevideo.com"
        webbrowser.open(url=url)

    elif "open netflix" in command:
        responce = "opening netflix"
        speak(responce)
        url = "https://www.netflix.com"
        webbrowser.open(url=url)

    elif "launch" in command:
        command = command.replace("launch", "")
        command = command.strip()
        command = command.replace(" ", "\ ")
        system_command = f"open -a {command}"
        os.system(system_command)

    elif "close app" in command:
        command = command.replace("close app", "")
        command = command.strip()
        system_command = f"osascript -e 'quit app \"{command}\"'"
        result = os.system(system_command)

    elif "change volume" in command:
        command = command.replace("too", "to")
        if "to" in command:
            command = command.replace("change volume", "")
            command = command.replace("to", "")
            command = command.strip()
            try:
                command = volume_options(command)
            except:
                command = 30

        else:
            responce = "To how much?"
            speak(responce)
            command = rep_listen()
            try:
                command = volume_options(command)
                if command == -1:
                    pass
            except:
                command = 30
        if command != -1:
            system_command = f"osascript -e \"set volume output volume {command}\""
            result = os.system(system_command)
            responce = "Changed volumed to " + str(command)
            speak(responce)

    elif "mute audio" in command or "turn off audio" in command:
        responce = "muting audio"
        speak(responce)
        system_command = "osascript -e \"set volume output muted true\""
        os.system(system_command)

    elif "turn on audio" in command:
        system_command = "osascript -e \"set volume output muted false\""
        os.system(system_command)
        responce = "audio turned on"
        speak(responce)

    elif "time" in command:
        hour = datetime.now().strftime("%-I:%-M %p")
        responce = "Time is " + str(hour)
        speak(responce)

    elif "day" in command:
        day = datetime.now().strftime("%A")
        responce = f"It's {day} today"
        speak(responce)

    elif "date" in command:
        date = datetime.now().strftime("%-d %B %Y")
        responce = f"The date is {date}"
        speak(responce)

    elif "which week" in command:
        week = datetime.now().strftime("%U")
        responce = f"The current week number is {week}"
        speak(responce)

    else:
        responce = "That's beyond my abilities at the moment"
        speak(responce)
        with open("unsupported_tasks.txt", "a") as file:
            file.write(
                command + "\t" + datetime.now().strftime("%-d%B%Y, %H:%M:%S") + "\n")


if __name__ == "__main__":
    passive_mode()
