# import streamlit as st
# from googletrans import Translator, LANGUAGES
# import pyttsx3
# import threading

# # Initialize translator
# translator = Translator()

# # Function to run text-to-speech safely in a separate thread
# def speak_text(text, lang_code):
#     def tts():
#         try:
#             engine = pyttsx3.init()
#             engine.setProperty('rate', 150)  # Set speech speed
#             engine.setProperty('voice', lang_code)  # Set language (if supported)
#             engine.say(text)
#             engine.runAndWait()
#             engine.stop()
#         except Exception as e:
#             st.error(f"Speech Error: {str(e)}")

#     # Run TTS in a separate thread
#     threading.Thread(target=tts, daemon=True).start()

# # Session state variables
# if "translated_text" not in st.session_state:
#     st.session_state.translated_text = ""

# if "detected_language" not in st.session_state:
#     st.session_state.detected_language = "Unknown"

# if "detected_lang_code" not in st.session_state:
#     st.session_state.detected_lang_code = "en"

# def main():
#     st.title("🌐 Language Translator App")

#     # Layout: Detected Language & Target Language Side-by-Side
#     col1, col2 = st.columns([1, 1])

#     with col1:
#         st.subheader("Detected Language")
#         st.info(f"**{st.session_state.detected_language}**")

#     with col2:
#         st.subheader("Select Target Language")
#         target_language = st.selectbox("Choose language:", list(LANGUAGES.values()))

#     col3, col4, col5 = st.columns([3, 1, 3])

#     with col3:
#         st.subheader("Enter Text")
#         text = st.text_area("Type or paste text here:", height=150)

#         # Speak Input Button
#         if st.button("🔊 Speak Input", key="speak_input"):
#             if text.strip():
#                 # Detect language before speaking
#                 detection = translator.detect(text)
#                 detected_lang_code = detection.lang
#                 detected_lang_name = LANGUAGES.get(detected_lang_code, "Unknown").capitalize()

#                 # Update detected language in session state
#                 st.session_state.detected_language = detected_lang_name
#                 st.session_state.detected_lang_code = detected_lang_code

#                 # Speak detected language
#                 speak_text(text, detected_lang_code)
#             else:
#                 st.warning("Please enter text before using speech.")

#     with col4:
#         st.write("")  # Empty space for alignment
#         st.write("")
#         st.write("")
#         st.write("")

#         # Translate Button with Icon
#         if st.button("🔄", key="translate_btn", help="Click to Translate", use_container_width=True):
#             if text.strip():
#                 try:
#                     # Detect Language FIRST
#                     detection = translator.detect(text)
#                     detected_lang_code = detection.lang
#                     detected_lang_name = LANGUAGES.get(detected_lang_code, "Unknown").capitalize()

#                     # Update detected language in session state
#                     st.session_state.detected_language = detected_lang_name
#                     st.session_state.detected_lang_code = detected_lang_code

#                     # Get target language code
#                     lang_code = [k for k, v in LANGUAGES.items() if v == target_language][0]

#                     # Translate text
#                     translated = translator.translate(text, dest=lang_code)
#                     st.session_state.translated_text = translated.text
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")
#             else:
#                 st.warning("Please enter text before translating.")

#     with col5:
#         st.subheader("Translation Output")
#         translated_text = st.text_area("Translation:", st.session_state.translated_text, height=150)

#         # Speak Translation Button
#         if st.button("🔊 Speak Translation", key="speak_trans"):
#             if st.session_state.translated_text.strip():
#                 speak_text(st.session_state.translated_text, st.session_state.detected_lang_code)
#             else:
#                 st.warning("No translation available to speak.")

# if __name__ == "__main__":
#     main()



import streamlit as st
from googletrans import Translator, LANGUAGES
import gtts
import threading
import tempfile
import os
import pygame

# Initialize translator
translator = Translator()

# Initialize pygame mixer for audio
pygame.mixer.init()

# Function to perform text-to-speech safely
def speak_text(text, lang_code):
    def tts():
        try:
            # Generate speech
            tts = gtts.gTTS(text, lang=lang_code)

            # Save to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_filename = temp_audio.name
                tts.save(temp_filename)

            # Play the generated speech using pygame
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()

            # Wait for the speech to finish before deleting the file
            while pygame.mixer.music.get_busy():
                continue

            # Clean up temporary file
            os.remove(temp_filename)

        except Exception as e:
            st.error(f"Speech Error: {str(e)}")

    # Run TTS in a separate thread
    threading.Thread(target=tts, daemon=True).start()

# Session state variables
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "detected_language" not in st.session_state:
    st.session_state.detected_language = "Detect Language"

if "detected_lang_code" not in st.session_state:
    st.session_state.detected_lang_code = "en"

def main():
    st.title("🌐 Language Translator App")

    # Layout: Detected Language & Target Language Side-by-Side
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Detected Language")
        st.info(f"**{st.session_state.detected_language}**")

    with col2:
        st.subheader("Select Target Language")
        target_language = st.selectbox("Choose language:", list(LANGUAGES.values()))

    col3, col4, col5 = st.columns([3, 1, 3])

    with col3:
        st.subheader("Enter Text")
        text = st.text_area("Type or paste text here:", height=150)

        # Speak Input Button
        if st.button("🔊 Speak", key="speak_input"):
            if text.strip():
                # Detect language before speaking
                detection = translator.detect(text)
                detected_lang_code = detection.lang
                detected_lang_name = LANGUAGES.get(detected_lang_code, "Unknown").capitalize()

                # Update detected language in session state
                st.session_state.detected_language = detected_lang_name
                st.session_state.detected_lang_code = detected_lang_code

                # Speak detected language
                speak_text(text, detected_lang_code)
            else:
                st.warning("Please enter text before using speech.")

    with col4:
        st.write("")  # Empty space for alignment
        st.write("")
        st.write("")
        st.write("")

        # Translate Button with Icon
        if st.button("🔄", key="translate_btn", help="Click to Translate", use_container_width=True):
            if text.strip():
                try:
                    # Detect Language FIRST
                    detection = translator.detect(text)
                    detected_lang_code = detection.lang
                    detected_lang_name = LANGUAGES.get(detected_lang_code, "Unknown").capitalize()

                    # Update detected language in session state
                    st.session_state.detected_language = detected_lang_name
                    st.session_state.detected_lang_code = detected_lang_code

                    # Get target language code
                    lang_code = [k for k, v in LANGUAGES.items() if v == target_language][0]

                    # Translate text
                    translated = translator.translate(text, dest=lang_code)
                    st.session_state.translated_text = translated.text
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter text before translating.")

    with col5:
        st.subheader("Translation Output")
        translated_text = st.text_area("Translation:", st.session_state.translated_text, height=150)

        # Speak Translation Button
        if st.button("🔊 Speak", key="speak_trans"):
            if st.session_state.translated_text.strip():
                # Use the target language for speech
                target_lang_code = [k for k, v in LANGUAGES.items() if v == target_language][0]
                speak_text(st.session_state.translated_text, target_lang_code)
            else:
                st.warning("No translation available to speak.")

if __name__ == "__main__":
    main()
