# gui.py
import tkinter as tk
from tkinter import scrolledtext
from interpreter import run  # Importing the run function

class QuetzalGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quetzal Programming Environment")

        # Text editor for code input
        self.text_input = scrolledtext.ScrolledText(master, width=80, height=20)
        self.text_input.pack()

        # Button to execute the code
        self.run_button = tk.Button(master, text="Run", command=self.execute_code)
        self.run_button.pack()

        # Output area for displaying results or errors
        self.output_area = scrolledtext.ScrolledText(master, width=80, height=20, state='disabled')
        self.output_area.pack()

    def execute_code(self):
        code = self.text_input.get('1.0', tk.END)
        output = run(code)  # Using the interpreter's run function
        self.output_area.config(state='normal')
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert(tk.END, output)
        self.output_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = QuetzalGUI(root)
    root.mainloop()
