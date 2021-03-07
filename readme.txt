Note: The script is written mainly for mac, to run on windows
or linux change the "system_command" in the code.

And to make the system speak, subprocess.call() method is used, if on windows
or linux, install the pyttsx3 module.
paste 
    engine = pyttsx3.init("nsss")

to change the voice of the assistant:
    voices = engine.getProperty("voices")
    # The above statement will get the list of all the voices available
    # You can select the one you like and set that as the voice of the 
    # assistant by the changing the index of the item with the voices variable
    # in the statement below
    engine.setProperty("voice", voices[7].id)
then replace the code in speak() method with:
    engine.say(text_input)
    engine.runandwait()

Additional Modules Required: 
    speechrecognition
    playsound
    PyObjC
    wikipedia
    pyaudio

The assistant is capable of :
    1. fetching information from wikipedia
    2. search for something on google and youtube
    3. opening sites like facebook.com, netflix.com, privevideo.com
    4. launch system applications
    5. closing system applications
    6. change the system volume
    7. muting and unmuting volume
    8. providing basic information like:
        a. time
        b. day
        c. date
        d. week number

Different sounds are played, when the assistant is listening actively i.e
when the assistant will respond to the given command, when the input is 
taken and its being processed and when the assistant is unable to understand
the given command.

Note: If the ambient mode is on, wait a sec before giving the command.

Unsupported tasks are logged in a file. 
