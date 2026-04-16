# turn speech into text
import speech_recognition as sr
import streamlit as st
import tempfile
import os

def main():
    # kickoff
    r = sr.Recognizer()

    # use the default mic as the source (preferred), but fall back to file upload if PyAudio/mic is unavailable
    audio = None
    using_mic = False
    try:
        with sr.Microphone() as source:
            st.write("Setting up microphone...")
            
            r.adjust_for_ambient_noise(source, duration=1)  # optional, but helps with noise, uncomment if you want speed.
            
            st.write("Listening..., say something!")
            # you ARE IN TIMEOUT
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            using_mic = True
    except AttributeError:
        # PyAudio not installed or not available on this environment
        st.warning("PyAudio is not installed or a microphone is not available on this host.\n"
                   "If you're running this locally, install PyAudio (Windows: use pipwin) and run locally.\n"
                   "As a fallback, upload an audio file below (wav, aiff, flac, mp3, m4a).")
    except OSError as e:
        # No default input device or permission error
        st.warning(f"Microphone not accessible: {e}.\nUpload an audio file below as a fallback.")
    except Exception as e:
        st.error(f"Unexpected error when accessing microphone: {e}")

    # Fallback: allow uploading an audio file from the browser
    if not using_mic and audio is None:
        uploaded = st.file_uploader("Upload an audio file (wav, aiff, flac, mp3, m4a)", type=["wav", "aiff", "flac", "mp3", "m4a"])
        if uploaded:
            # Save to a temporary file because speech_recognition.AudioFile expects a file path
            suffix = os.path.splitext(uploaded.name)[1] or ".wav"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded.getvalue())
                tmp_path = tmp.name
            try:
                with sr.AudioFile(tmp_path) as source:
                    audio = r.record(source)
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
        else:
            # nothing to do yet
            return

    try:
        # Audio to text using Google's free API
        if audio is None:
            st.write("No audio captured.")
            return
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
