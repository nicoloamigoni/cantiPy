import tkinter as tk
from tkinter import ttk, messagebox
import lib.gui.main_window as main_window
import lib.gui.create_window as create_window
import lib.songsdb as songsdb
import lib.pdf_creator as pdf_creator

class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        self.song_list = songsdb.get_songs()
        self.setup_main_window()
        self.update_all_songs_list(self.song_list)

    def setup_main_window(self):
        main_window.setup_main_window(self)

    def update_all_songs_list(self, songs):
        main_window.update_all_songs_list(self, songs)


    def next(self):
        selected_titles = self.selected_songs_listbox.get(0, tk.END)
        selected_songs = [song for song in self.song_list if str(song) in selected_titles]
        if len(selected_songs) == 0:
            messagebox.showwarning("No songs selected", "Please select at least one song.")
            return
        if(not pdf_creator.create_pdf(selected_songs)):
            messagebox.showerror("Error", "Songs and translations have different number of paragraphs.")
        else:
            messagebox.showinfo("Success", "PDF created successfully!")

    def open_create_song_window(self, title="", author="", lyrics="", translation="", song=None):
        create_window.open_create_song_window(self, title, author, lyrics, translation, song)

import lib.songsdb as songsdb

def run():
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
