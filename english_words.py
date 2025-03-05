import random
import json
import os
import nltk
from nltk.corpus import wordnet
import streamlit as st

nltk.download('wordnet', quiet=True)

WORD_LIST_FILE = "word_list.txt"
STATE_FILE = "word_state.json"

def get_word_meaning(word):
    synsets = wordnet.synsets(word)
    return synsets[0].definition() if synsets else "No meaning found"

def read_word_list(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Word list file not found: {file_path}")
    with open(file_path, "r") as file:
        words = [line.strip() for line in file if line.strip()]
    return words

def load_or_initialize_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            state = json.load(file)
            return state["shuffled_list"], state["position"]
    else:
        word_list = read_word_list(WORD_LIST_FILE)
        random.shuffle(word_list)
        return word_list, 0

def save_state(shuffled_list, position):
    with open(STATE_FILE, "w") as file:
        json.dump({"shuffled_list": shuffled_list, "position": position}, file)

def generate_daily_words():
    shuffled_list, position = load_or_initialize_state()
    if position >= len(shuffled_list):
        word_list = read_word_list(WORD_LIST_FILE)
        random.shuffle(word_list)
        shuffled_list = word_list
        position = 0
    new_words = shuffled_list[position:position + 5]
    if len(new_words) < 5:
        remaining = 5 - len(new_words)
        word_list = read_word_list(WORD_LIST_FILE)
        random.shuffle(word_list)
        shuffled_list = word_list
        new_words += shuffled_list[:remaining]
        position = remaining
    else:
        position += 5
    save_state(shuffled_list, position)
    return {word: get_word_meaning(word) for word in new_words}

# Streamlit app
def main():
    st.title("Assalamu alaikum bhai")
    st.write("niche click kar naye words ke liye")

    # Button to generate words
    if st.button("Dabade yaar"):
        daily_words = generate_daily_words()
        # Store in session state to display
        st.session_state['words'] = daily_words

    # Display words if they exist in session state
    if 'words' in st.session_state:
        for word, meaning in st.session_state['words'].items():
            st.markdown(f"**{word.capitalize()}**: {meaning}")

if __name__ == "__main__":
    main()