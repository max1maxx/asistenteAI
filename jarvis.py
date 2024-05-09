import speech_recognition as sr
import pyttsx3
import pywhatkit

listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

name = 'alexa'

def listen(attempts=3):
    """
    Listens for user input, handles errors, and retries a limited number of times.

    Args:
        attempts (int, optional): The number of times to retry listening in case of errors. Defaults to 3.

    Returns:
        str: The recognized user input (lowercased and without the wake word). None if no speech is recognized after retries.
    """
    rec = None
    for i in range(attempts):
        try:
            print("Escuchando...")
            with sr.Microphone() as source:
                voice = listener.listen(source)
                rec = listener.recognize_google(voice)
                rec = rec.lower()
                if name in rec:
                    rec = rec.replace(name, '')
                print(rec)
                break  # Exit the loop if successful
        except Exception as e:
            print("Error al escuchar:", e)
            if i == attempts - 1:  # Only print retries message on the last attempt
                talk("Lo siento, no te entendí. ¿Puedes repetirlo?")

    return rec

def run():
    while True:
        rec = listen()
        if rec:
            if 'reproduce' in rec:  # Check for "reproduce" command
                music = rec.replace('reproduce', '').strip()
                talk('Reproduciendo ' + music)
                pywhatkit.playonyt(music)
            else:
                talk("Lo siento, no sé qué hacer con '" + rec + "'. ¿Intentas reproducir música?")
        else:
            break  # Exit the loop if nothing is recognized after retries

if __name__ == "__main__":
    run()
