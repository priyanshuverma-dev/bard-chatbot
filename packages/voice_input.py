import speech_recognition as sr
import json


# Function to list available microphones
def list_microphones():
    print("Available Microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")


# Function to get user's choice of microphone
def get_user_microphone_choice():
    while True:
        try:
            choice = int(input("Enter the number of the microphone you want to use: "))
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to get the saved microphone choice from the configuration file
def get_saved_microphone_choice():
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config["selected_microphone_index"]
    except (FileNotFoundError, KeyError):
        return None


# Function to save the selected microphone choice to the configuration file
def save_microphone_choice(choice):
    try:
        with open("config.json", "w") as config_file:
            json.dump({"selected_microphone_index": choice}, config_file)
    except IOError:
        print("Error saving configuration.")


# Function to get user query
def get_user_query():
    # Check if a saved microphone choice exists in the configuration file
    saved_choice = get_saved_microphone_choice()

    if saved_choice is not None:
        print(
            f"Using saved microphone: {sr.Microphone.list_microphone_names()[saved_choice]}"
        )
        microphone_index = saved_choice
    else:
        # List available microphones if no saved choice
        list_microphones()

        # Get the user's choice of microphone
        microphone_index = get_user_microphone_choice()
        save_microphone_choice(microphone_index)

    # Initialize the recognizer with the selected microphone
    recognizer = sr.Recognizer()
    selected_microphone = sr.Microphone(device_index=microphone_index)

    with selected_microphone as source:
        print(
            f"Using microphone: {sr.Microphone.list_microphone_names()[microphone_index]}"
        )
        print("Speak something...")
        audio = recognizer.listen(source)

    try:
        # Recognize the speech
        user_query = recognizer.recognize_google(audio)
        return user_query
    except sr.UnknownValueError:
        print(f"")
        print(f"Sorry, I couldn't understand what you said.\n")
        print(f"\n")
        return f"error"
    except sr.RequestError as e:
        print(f"")
        print(f"Sorry, there was an error with the speech recognition service: {e}\n")
        print(f"\n")
        return f"error"
