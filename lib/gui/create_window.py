import tkinter as tk
from tkinter import ttk, messagebox
import lib.songsdb as songsdb

def open_create_song_window(self, title="", author="", lyrics="", translation="", song=None):
    self.create_window = tk.Toplevel(self.master)
    self.create_window.title("Create Song")
    self.create_window.geometry("900x650")
    self.create_window.resizable(True, True)

    self.create_window.columnconfigure(1, weight=1)
    self.create_window.columnconfigure(0, weight=1)

    # Create subgrid 
    subgrid = ttk.Frame(self.create_window)
    subgrid.grid(row=0, column=0, columnspan=2, sticky="nsew")
    subgrid.columnconfigure(1, weight=1)

    ttk.Label(subgrid, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    self.title_entry = ttk.Entry(subgrid)
    self.title_entry.insert(tk.END, title)
    self.title_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(subgrid, text="Author:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    self.author_entry = ttk.Entry(subgrid)
    self.author_entry.insert(tk.END, author if author else "")
    self.author_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(self.create_window, text="Inserisci qui il testo e la traduzione (se presente). Separa i paragrafi con doppio a capo.\nIl numero di paragrafi della traduzione (se presente) deve essere uguale al numero di paragrafi del testo.").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    ttk.Label(self.create_window, text="Lyrics:").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    self.lyrics_text = tk.Text(self.create_window)
    self.lyrics_text.insert(tk.END, lyrics)
    self.lyrics_text.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    ttk.Label(self.create_window, text="Translation:").grid(row=3, column=1, padx=10, pady=5, sticky="nw")
    self.translation_text = tk.Text(self.create_window)
    self.translation_text.insert(tk.END, translation)
    self.translation_text.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")

    save_button = ttk.Button(self.create_window, text="Save", command= lambda: save_song(self, song))
    save_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")

def save_song(self, song):
    title = self.title_entry.get()
    author = self.author_entry.get()
    lyrics = self.lyrics_text.get("1.0", tk.END).strip()
    translation = self.translation_text.get("1.0", tk.END).strip()
    if title and author and lyrics:
        if song is not None:
            song.title = title
            song.author = author
            song.set_text(lyrics.split("\n\n"))
            song.set_translation(translation.split("\n\n"))
            song.isForeign = translation != ""
            if songsdb.update_song(song):
                messagebox.showinfo("Success", "Song created successfully!")
                self.create_window.destroy()
            else:
                messagebox.showerror("Error", "Il testo e la traduzione devono avere lo stesso numero di paragrafi.")
        else:
            new_song = songsdb.new_song(title, author, lyrics, translation)
            if(new_song):
                messagebox.showinfo("Success", "Song updated successfully!")
                self.create_window.destroy()
                self.selected_songs_listbox.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Il testo e la traduzione devono avere lo stesso numero di paragrafi.")
    else:
        messagebox.showwarning("Incomplete", "Please provide both title and author.")
    self.song_list = songsdb.get_songs()
    self.update_all_songs_list(self.song_list)