from tkinter import Tk, Text, Scrollbar, Button, Frame, messagebox
from tkinter.scrolledtext import ScrolledText
from interpreter import run
import threading

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quetzal Interpreter")
        self.root.geometry("600x400")

        # Frame for input area
        input_frame = Frame(self.root)
        input_frame.pack(side='top', fill='both', expand=True)

        # Text area for input
        self.input_area = ScrolledText(input_frame, wrap='word')
        self.input_area.pack(side='left', fill='both', expand=True)

        # Scrollbar for input area
        scrollbar_input = Scrollbar(input_frame, command=self.input_area.yview)
        scrollbar_input.pack(side='right', fill='y')
        self.input_area.config(yscrollcommand=scrollbar_input.set)

        # Frame for output area
        output_frame = Frame(self.root)
        output_frame.pack(side='bottom', fill='both', expand=True)

        # Text area for output
        self.output_area = Text(output_frame, wrap='word', state='disabled')
        self.output_area.pack(side='left', fill='both', expand=True)

        # Scrollbar for output area
        scrollbar_output = Scrollbar(output_frame, command=self.output_area.yview)
        scrollbar_output.pack(side='right', fill='y')
        self.output_area.config(yscrollcommand=scrollbar_output.set)

        # Run code button
        run_button = Button(self.root, text="Run Code", command=self.execute_code)
        run_button.pack()

    def execute_code(self):
        print("Executing code...")
        code = self.input_area.get('1.0', 'end')
        threading.Thread(target=self.run_interpreter, args=(code,), daemon=True).start()

    def run_interpreter(self, code):
        print(f"Running interpreter with code: {code}")
        try:
            output = run(code)
            print(f"Interpreter output: {output}")
            self.output_area.after(0, self.update_output_area, output)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.output_area.after(0, self.update_output_area, "Error occurred!")

    def update_output_area(self, output):
        """ Update the output area with provided text """
        self.output_area.config(state='normal')  # Enable the text widget
        self.output_area.insert('end', output + '\n')  # Insert output at the end
        self.output_area.config(state='disabled')  # Disable the text widget to prevent editing


if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()
