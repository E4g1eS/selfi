from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv
import random

class Tester:
    _root : Tk
    _translate_label : Label
    _input_field : Text
    _feedback_label : Label
    _dictionary : list
    _current_word_index : int

    def __init__(self):
        self._dictionary = list()
        self._root = Tk()
        self._init_ui()
        self._root.mainloop()

    def _init_ui(self):
        source_frame = Frame(self._root)
        source_frame.pack()
        self._translate_label = Label(source_frame, text = "Open dictionary file first!")
        self._translate_label.pack()
        
        translation_frame = Frame(self._root)
        translation_frame.pack()
        translation_label = Label(translation_frame, text = "Translation:")
        translation_label.grid(row=0, column=0)
        self._input_field = Entry(translation_frame)
        self._input_field.grid(row=0, column=1)

        feedback_frame = Frame(self._root)
        feedback_frame.pack()
        self._feedback_label = Label(feedback_frame, text = "No dictionary yet.")
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
        with open(filename) as csvfile:
            dictionaryfile = csv.reader(csvfile)

            self._dictionary = list()
            for row in dictionaryfile:
                self._dictionary.append(row)

            print("Loaded", self._dictionary)

        self._next_word()

    def _next_word(self) -> None:
        self._current_word_index = random.randint(0, len(self._dictionary) - 1)
        self._translate_label.configure(text=self._dictionary[self._current_word_index][0])


def main():
    tester = Tester()

if __name__ == "__main__":
    main()