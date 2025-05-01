import tkinter as tk
from tkinter import messagebox
import requests
import random
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO

# API Key
API_KEY = "8557bf2b"
BASE_URL = "http://www.omdbapi.com/?apikey=" + API_KEY

# Theme Colors
themes = {
    "Retro": {"bg": "#2C003E", "frame": "#9c6d9c", "text": "white", "button": "#FF6961", "hover": "#FF4747", "search_button": "#5da371", "sidebar": "#774caf"},
    "Dark": {"bg": "#1B1B2F", "frame": "#16213E", "text": "#FFD700", "button": "#964158", "hover": "#FF4747", "search_button": "#77DD77", "sidebar": "#374357"}
}

current_theme = "Retro"
search_history = []
history_visible = False

def apply_theme():
    theme = themes[current_theme]
    root.config(bg=theme["bg"])
    frame.config(bg=theme["frame"])
    title_label.config(bg=theme["frame"], fg=theme["text"])
    for button in buttons:
        button.config(bg=theme["button"], activebackground=theme["hover"], relief=tk.RAISED, bd=3)
    search_button.config(bg=theme["search_button"], activebackground=theme["hover"], relief=tk.RAISED, bd=3)
    history_frame.config(bg=theme["sidebar"])
    history_label.config(bg=theme["sidebar"], fg=theme["text"])
    history_listbox.config(bg=theme["sidebar"], fg=theme["text"])

def toggle_theme():
    global current_theme
    current_theme = "Dark" if current_theme == "Retro" else "Retro"
    apply_theme()

def fetch_movie(movie_name=None):
    if not movie_name:
        movie_name = search_entry.get().strip()
    if movie_name:
        response = requests.get(BASE_URL + "&t=" + movie_name)
        if response.status_code == 200:
            data = response.json()
            if data["Response"] == "True":
                display_movie(data)
                update_history(data["Title"])
            else:
                messagebox.showerror("Error", "Movie not found!")

def display_movie(data):
    details_text.config(state=tk.NORMAL)
    details_text.delete(1.0, tk.END)
    details_text.insert(tk.END, f"\n🎬 Title: {data['Title']}\n📅 Year: {data['Year']}\n🎭 Genre: {data['Genre']}\n🎬 Director: {data['Director']}\n⭐ IMDB Rating: {data['imdbRating']}\n\n📖 Plot: {data['Plot']}\n")
    details_text.config(state=tk.DISABLED)
    image_url = data.get("Poster")
    if image_url and image_url != "N/A":
        img_response = requests.get(image_url)
        img_data = Image.open(BytesIO(img_response.content)).resize((250, 350))
        movie_poster = ImageTk.PhotoImage(img_data)
        poster_label.config(image=movie_poster)
        poster_label.image = movie_poster

def update_history(movie_name):
    if movie_name and movie_name not in search_history:
        search_history.append(movie_name)
        history_listbox.insert(tk.END, movie_name)

def toggle_history():
    global history_visible
    if history_visible:
        history_frame.pack_forget()
    else:
        history_frame.pack(side=tk.RIGHT, fill=tk.Y)
    history_visible = not history_visible

root = tk.Tk()
root.title("Movie Info Fetcher")
root.geometry("950x700")

frame = tk.Frame(root, bg=themes[current_theme]["frame"], bd=5, relief=tk.RIDGE)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(frame, text="🎬 Movie Info Fetcher", font=("Arial", 18, "bold"), bg=themes[current_theme]["frame"], fg=themes[current_theme]["text"])
title_label.pack(pady=10)

# Search Entry
search_entry = tk.Entry(frame, font=("Arial", 12), width=45)
search_entry.insert(0, "Type Movie Name...")
search_entry.pack(pady=5)

# Button Frame
button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="🔍 Search", font=("Arial", 10, "bold"), command=fetch_movie)
search_button.pack(side=tk.LEFT, padx=5)

buttons = [
    tk.Button(button_frame, text="🎲 Random", font=("Arial", 10, "bold"), command=lambda: fetch_movie(random.choice(["Inception", "Interstellar", "Gladiator","How to Lose a Guy in 10 Days","Chaava"]))),
    tk.Button(button_frame, text="🎥 Trailer", font=("Arial", 10, "bold"), command=lambda: webbrowser.open(f"https://www.youtube.com/results?search_query={search_entry.get().strip()}+trailer")),
    tk.Button(button_frame, text="🎨 Theme", font=("Arial", 10, "bold"), command=toggle_theme),
    tk.Button(button_frame, text="📜 History", font=("Arial", 10, "bold"), command=toggle_history)
]

for button in buttons:
    button.pack(side=tk.LEFT, padx=5)

# Movie Details
frame_details = tk.Frame(frame)
frame_details.pack()

details_text = tk.Text(frame_details, font=("Arial", 10), height=6, width=60, state=tk.DISABLED, relief=tk.FLAT)
details_text.pack(pady=10)

poster_label = tk.Label(frame_details)
poster_label.pack()

# History Sidebar
history_frame = tk.Frame(root, bg=themes[current_theme]["sidebar"], bd=3, relief=tk.RIDGE)
history_label = tk.Label(history_frame, text="📜 Search History", font=("Arial", 12, "bold"), bg=themes[current_theme]["sidebar"], fg=themes[current_theme]["text"])
history_label.pack()

history_listbox = tk.Listbox(history_frame, font=("Arial", 10), height=10, width=35, relief=tk.FLAT)
history_listbox.pack(pady=5)

apply_theme()
root.mainloop()
