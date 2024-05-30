import tkinter as tk
from tkinter import ttk, messagebox
import lib.songsdb as songsdb

def create_widgets(app):
    app.style = ttk.Style()
    app.style.theme_use("clam")
    app.style.configure("TButton", padding=5, relief="flat", font=("Arial", 10))
    app.style.configure("TLabel", font=("Arial", 10))
    app.style.configure("TEntry", padding=5, font=("Arial", 10))

    app.search_label = ttk.Label(app.master, text="Search:")
    app.search_entry = ttk.Entry(app.master)
    app.search_entry.bind("<KeyRelease>", lambda event: search(app, event))

    app.create_button = ttk.Button(app.master, text="Create", command=app.open_create_song_window)
    app.all_songs_label = ttk.Label(app.master, text="All Songs:")
    app.all_songs_listbox = tk.Listbox(app.master, selectmode=tk.SINGLE, font=("Arial", 10))
    app.all_songs_listbox.bind("<Double-1>", lambda event: toggle_select(app, event))
    # on right click, open context menu with options to play, add to playlist, etc.
    app.all_songs_listbox.bind("<Button-3>", lambda event: context_menu(app, event))


    app.selected_songs_label = ttk.Label(app.master, text="Selected Songs:")
    app.selected_songs_listbox = tk.Listbox(app.master, selectmode=tk.SINGLE, font=("Arial", 10))
    app.selected_songs_listbox.bind("<Double-1>", lambda event: toggle_select(app, event))

    app.select_button = ttk.Button(app.master, text="Next", command=app.next)

def context_menu(app, event):
    widget = event.widget
    index = widget.nearest(event.y)
    title = widget.get(index)
    song = next((s for s in app.song_list if str(s) == title), None)
    menu = tk.Menu(app.master, tearoff=0)
    menu.add_command(label="Edit", command=lambda: app.open_create_song_window(title=song.title, author=song.author, lyrics="\n\n".join(song.text), translation="\n\n".join(song.translation), song=song))
    menu.add_command(label="Delete", command=lambda: delete_song(app, song))
    menu.tk_popup(event.x_root, event.y_root)

def delete_song(app, song):
    app.song_list.remove(song)
    app.update_all_songs_list(app.song_list)
    songsdb.delete_song(song)

def setup_main_window(app):
    app.master.title("Song's group trasure")
    app.master.geometry("800x600")
    app.master.resizable(True, True)
    app.master.columnconfigure(1, weight=1)
    app.master.columnconfigure(2, weight=1)
    app.master.rowconfigure(2, weight=1)

    create_widgets(app)
    layout_widgets(app)

def layout_widgets(app):
    app.search_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    app.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    app.create_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    app.all_songs_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    app.all_songs_listbox.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

    app.selected_songs_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
    app.selected_songs_listbox.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")

    app.select_button.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky="e")


def update_all_songs_list(app, songs):
    app.all_songs_listbox.delete(0, tk.END)
    for song in songs:
        app.all_songs_listbox.insert(tk.END, song)

def search(app, event):
    query = str(app.search_entry.get()).lower()
    results = [song for song in app.song_list if query in str(song).lower()]
    app.update_all_songs_list(results)

def toggle_select(app, event):
    widget = event.widget
    index = widget.curselection()
    if index:
        song = widget.get(index)
        if widget == app.all_songs_listbox:
            if song not in app.selected_songs_listbox.get(0, tk.END):
                app.selected_songs_listbox.insert(tk.END, song)
        elif widget == app.selected_songs_listbox:
            app.selected_songs_listbox.delete(index)
    else:
        pass
