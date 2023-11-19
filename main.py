import tkinter as tk
from tkinter import filedialog
import os
import csv
from docx import Document
import subprocess

class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selector App")
        self.root.geometry("400x200")

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.input_button = tk.Button(self.frame, text="Input", command=self.select_input_file)
        self.input_button.pack(pady=10)

        self.output_extensions = ['.csv', '.docx', '.odt', '.pdf', '.rtf']
        self.selected_output_extension = tk.StringVar()
        self.selected_output_extension.set(self.output_extensions[0])

        self.output_dropdown = tk.OptionMenu(self.frame, self.selected_output_extension, *self.output_extensions)
        self.output_dropdown.pack(pady=10)

        self.output_label = tk.Label(self.frame, text="")
        self.output_label.pack(pady=10)

        self.selected_output_extension.trace_add('write', self.update_output_label)
        self.output_dropdown.bind('<Configure>', self.execute_selected_output)

        self.extension_functions = {
            '.csv': self.execute_csv_function,
            '.docx': self.execute_docx_function,
            '.odt': self.execute_odt_function,
            '.pdf': self.execute_pdf_function,
            '.rtf': self.execute_rtf_function
        }

    def select_input_file(self):
        file_object = filedialog.askopenfile()
        if file_object:
            self.selected_input_file = file_object.name
            self.selected_input_name, self.selected_input_extension = self.get_file_info(self.selected_input_file)
            self.output_label.config(text=f"Input file selected: {self.selected_input_name}")

    def update_output_label(self, *args):
        self.output_label.config(text=f"Selected output extension: {self.selected_output_extension.get()}")

    def execute_selected_output(self, event):
        selected_extension = self.selected_output_extension.get()
        if selected_extension in self.extension_functions:
            self.extension_functions[selected_extension]()

    def execute_csv_function(self):
        base_output_file = "output"
        output_file = f"{base_output_file}.csv"
        convert_to_csv(self.selected_input_file, output_file)
        print(f"Conversion to CSV successful. Output file: {output_file}")

    def execute_docx_function(self):
        base_output_file = "output"
        output_file = f"{base_output_file}.docx"
        convert_to_docx(self.selected_input_file, output_file)
        print(f"Conversion to DOCX successful. Output file: {output_file}")

    def execute_odt_function(self):
        base_output_file = "output"
        output_file = f"{base_output_file}.odt"
        convert_to_odt(self.selected_input_file, output_file)
        print(f"Conversion to ODT successful. Output file: {output_file}")

    def execute_pdf_function(self):
        base_output_file = "output"
        output_file = f"{base_output_file}.pdf"
        convert_to_pdf(self.selected_input_file, output_file)
        print(f"Conversion to PDF successful. Output file: {output_file}")

    def execute_rtf_function(self):
        base_output_file = "output"
        output_file = f"{base_output_file}.rtf"
        convert_to_rtf(self.selected_input_file, output_file)
        print(f"Conversion to RTF successful. Output file: {output_file}")

    @staticmethod
    def get_file_info(file_path):
        file_name = file_path.split("/")[-1]
        name, extension = file_name.rsplit(".", 1)
        return name, '.' + extension

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile)
        for row in reader:
            writer.writerow(row)

def convert_to_docx(input_file, output_file):
    document = Document()
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            document.add_paragraph(line.strip())
    document.save(output_file)

def convert_to_odt(input_file, output_file):
    try:
        subprocess.run(['unoconv', '--format', 'odt', '--output', output_file, input_file], check=True)
        print(f'Conversion to ODT successful. Output file: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Conversion to ODT failed. Error: {e}')

def convert_to_pdf(input_file, output_file):
    try:
        subprocess.run(['unoconv', '--format', 'pdf', '--output', output_file, input_file], check=True)
        print(f'Conversion to PDF successful. Output file: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Conversion to PDF failed. Error: {e}')

def convert_to_rtf(input_file, output_file):
    try:
        subprocess.run(['unoconv', '--format', 'rtf', '--output', output_file, input_file], check=True)
        print(f'Conversion to RTF successful. Output file: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Conversion to RTF failed. Error: {e}')

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()

