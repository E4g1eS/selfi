from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
import random

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


def main():
    tester = Tester()

if __name__ == "__main__":
    main()