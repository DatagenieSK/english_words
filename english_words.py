import random
import json
import os
import nltk
from nltk.corpus import wordnet
import tkinter as tk
from tkinter import ttk

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

def create_gui():
    root = tk.Tk()
    root.title("Daily Words")
    root.geometry("600x400")
    root.configure(bg="#f0f2f5")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 11), background="#f0f2f5")

    title_label = ttk.Label(root, text="Your Daily Words", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=20)

    word_frame = tk.Frame(root, bg="#f0f2f5")
    word_frame.pack(pady=10, fill="both", expand=True)

    def display_words():
        for widget in word_frame.winfo_children():
            widget.destroy()
        daily_words = generate_daily_words()
        for word, meaning in daily_words.items():
            word_label = ttk.Label(
                word_frame, 
                text=f"{word.capitalize()}: {meaning}",
                wraplength=550, 
                justify="left",
                background="#ffffff",
                relief="solid",
                borderwidth=1,
                padding=10
            )
            word_label.pack(pady=5, padx=20, fill="x")

    generate_button = ttk.Button(root, text="Generate New Words", command=display_words, style="TButton")
    generate_button.pack(pady=20)

    display_words()
    root.mainloop()

if __name__ == "__main__":
    create_gui()