# pyright: reportUnknownVariableType=false
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
import random
from typing import Any, Self
import logging

class Word:
    text : str
    translations : set[Self]

    def __init__(self, text : str):
        self.text = text
        self.translations = set()

    def __str__(self) -> str:
        s = "Word '" + self.text + "' has translations: "

        for word in self.translations:
            s += "'" + word.text + "', "

        return s

class Language:
    name : str
    _words : list[Word]

    def __init__(self, name="unknown"):
        self.name = name
        self._words = list()

    def __str__(self) -> str:
        s = self.name + ":\n"
        for word in self._words:
            s += str(word) + "\n"
        return s

    def __contains__(self, key : str | Word) -> bool:
        if type(key) == Word:
            for word in self._words:
                return key in self._words

        if type(key) == str:
            for word in self._words:
                if key == word.text: return True

        return False

    def __getitem__(self, key : str) -> Word:
        for word in self._words:
            if word.text == key:
                return word

        raise KeyError("No such word exists in language!")

    def get_or_create(self, word : str) -> Word:
        if word in self:
            return self[word]

        created = Word(word)
        self._words.append(created)
        return created

class Dictionary:
    language_a : Language
    language_b : Language

    def __init__(self):
        self.language_a = Language("Language A")
        self.language_b = Language("Language B")

    def __str__(self) -> str:
        return str(self.language_a) + str(self.language_b)

class Tester:
    _dictionary : Dictionary | None
    _translate_word : Word | None

    def __init__(self):
        self._dictionary = None
        self._translate_word = None

    def open_dictionary_file(self) -> bool:
        filetypes = (
            ('Comma separated values', '*.csv'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(title="Open dictionary", initialdir="./", filetypes=filetypes)

        new_dictionary = None

        try:
            with open(filename, encoding="utf8") as csvfile:
                dictionary_file = csv.reader(csvfile)
                new_dictionary = self._parse_dictionary_file(dictionary_file)

        except IOError:
            logging.error("Could not open file!")
            return False

        if new_dictionary is None:
            logging.error("Could not parse file!")
            return False

        self._dictionary = new_dictionary
        return True

    def _parse_dictionary_file(self, dictionary_file) -> Dictionary | None:

        dictionary_list = list()

        for row in dictionary_file:
            dictionary_list.append(row)

        logging.info("Loaded: " + str(dictionary_list))

        if not self._validate_dictionary_list(dictionary_list):
            return None

        dictionary = Dictionary()

        for row in dictionary_list:

            word_a = dictionary.language_a.get_or_create(row[0])
            word_b = dictionary.language_b.get_or_create(row[1])

            word_a.translations.add(word_b)
            word_b.translations.add(word_a)

        logging.info("Dictionary:\n" + str(dictionary))

        return dictionary

    @staticmethod
    def _validate_dictionary_list(dictionary_list : list) -> bool:
        if len(dictionary_list) < 2:
            logging.error("File contains less than 2 rows!")
            return False

        for entry in dictionary_list:
            
            if len(entry) < 2:
                logging.error("File contains words without translations!")
                return False

            try:
                str(entry[0])
                str(entry[1])

            except ValueError:
                logging.error("Some content in file cannot be parsed as string!")
                return False

        return True


class UI:
    _root : tk.Tk
    _tester : Tester

    # Widgets:

    def __init__(self):
        self._tester = Tester()
        self._tester.open_dictionary_file()

        self._root = tk.Tk()
        self._init_ui()

        self._root.mainloop()

    def _init_ui(self):
        pass
"""
class Tester:
    _root : Tk
    _translate_word : Label
    _input_field : Text
    _feedback_label : Label
    _dictionary : list
    _current_word_index : int

    _check_button : Button
    _give_up_button : Button

    _loaded : bool

    def __init__(self):
        self._dictionary = list()
        self._current_word_index = None
        self._loaded = False

        self._root = Tk()
        self._root.bind("<Return>", self._enter_pressed)
        self._init_ui()
        self._root.mainloop()

    def _init_ui(self):
        source_frame = Frame(self._root)
        source_frame.pack()
        self._translate_word = Label(source_frame, text = "No dictionary yet.")
        self._translate_word.pack()
        
        translation_frame = Frame(self._root)
        translation_frame.pack()
        translation_label = Label(translation_frame, text = "Translation:")
        translation_label.grid(row=0, column=0)
        self._input_field = Entry(translation_frame)
        self._input_field.grid(row=0, column=1)
        self._check_button = Button(translation_frame, text="Check", command=self._check_word)
        self._check_button.grid(row=0, column=2)
        self._check_button["state"] = "disabled"
        self._give_up_button = Button(translation_frame, text="Give up", command=self._give_up)
        self._give_up_button.grid(row=0, column=3)
        self._give_up_button["state"] = "disabled"

        feedback_frame = Frame(self._root)
        feedback_frame.pack()
        self._feedback_label = Label(feedback_frame, text = "Open dictionary file first!")
        self._feedback_label.pack()

        file_frame = Frame(self._root)
        file_frame.pack()
        open_button = Button(file_frame, text = "Open .csv dictionary file...", command = self._open_dictionary_file)
        open_button.pack()

    def _open_dictionary_file(self) -> None:
        filetypes = (
            ('Comma separated values', '*.csv'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(title="Open dictionary", initialdir="./", filetypes=filetypes)
        
        try:
            with open(filename, encoding="utf8") as csvfile:
                dictionaryfile = csv.reader(csvfile)

                dictionary = list()
                for row in dictionaryfile:
                    dictionary.append(row)

                print("Loaded", dictionary)

                if not self.validate_dictionary(dictionary):
                    return

                self._dictionary = dictionary
                
            self._next_word()
            self._give_up_button["state"] = "normal"
            self._check_button["state"] = "normal"
            self._loaded = True

        except IOError:
            messagebox.showerror("Error", "Could not open file!")

    def _next_word(self) -> None:
        self._reset_feedback()
        self._input_field.delete(0, END)
        new_index = random.randint(0, len(self._dictionary) - 1)
        while self._current_word_index == new_index:
            new_index = random.randint(0, len(self._dictionary) - 1)
        self._current_word_index = new_index
        self._translate_word.configure(text=self._dictionary[self._current_word_index][0])

    def _check_word(self) -> None:
        translation = self._input_field.get()

        if translation == self._dictionary[self._current_word_index][1]:
            self._feedback_label.configure(text="Correct!")
            self._root.after(1000, self._next_word)

        else:
            self._feedback_label.configure(text="Wrong!")
            self._root.after(1000, self._reset_feedback)

    def _enter_pressed(self, event) -> None:
        if self._loaded: self._check_word()

    def _give_up(self) -> None:
        self._feedback_label.configure(text=("Correct is '" + self._dictionary[self._current_word_index][1] + "'"))
        self._root.after(3000, self._next_word)

    def validate_dictionary(self, dictionary : list) -> bool:
        if len(dictionary) < 2:
            messagebox.showerror("Error", "File contains less then 2 translations!")
            return False

        for entry in dictionary:
            
            if len(entry) < 2:
                messagebox.showerror("Error", "File contains words without translations!")
                return False

            try:
                str(entry[0])
                str(entry[1])

            except ValueError:
                messagebox.showerror("Error", "File cannot be parsed as string!")
                return False

        return True

    def _reset_feedback(self):
        self._feedback_label.configure(text="...")
"""

if __name__ == "__main__":
    logging.basicConfig(filename="log.log", encoding="utf-8", level=logging.DEBUG)
    ui = UI()