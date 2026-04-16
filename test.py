# tests here are carried out here, it is out her so i  can host it on streamlit see if any changes are needed

# turn speech into text
import speech_recognition as sr
import streamlit as st

def main():
    # kickoff
    r = sr.Recognizer()

    # use the default mic as the source
    with sr.Microphone() as source:
        st.write("Setting up microphone...")
        r.adjust_for_ambient_noise(source, duration= 1)  # optional, but helps with noise, uncomment if you want speed.
        st.write("Listening..., say something!")
        audio = r.listen(source)


    try:
        # Audio to text using Google's free API
        text = r.recognize_google(audio)
        st.write(f"You said: {text}")
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from the speech recognition service; {e}")
    except Exception as e:
        st.write(f"An unexpected error occurred: {e}")

st.title("Speech to Text Demo")
if st.button("Start Listening"):
    main()
