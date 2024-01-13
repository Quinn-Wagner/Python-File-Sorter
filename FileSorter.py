"""
File Sorter Application

This program allows you to organize files in a specified input directory based on their extensions.
You can choose which file types to sort and provide destination directories for each.

Developer: Quinn Wagner
"""

import os
import shutil
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.file_types = [
                            ".txt",
                            ".doc",
                            ".docx",
                            ".pdf",
                            ".jpg",
                            ".jpeg",
                            ".png",
                            ".gif",
                            ".mp3",
                            ".mp4",
                            ".avi",
                            ".mov",
                            ".zip",
                            ".rar",
                            ".tar",
                            ".gz",
                            ".xlsx",
                            ".pptx",
                            ".html",
                            ".css",
                            ".js",
                            ".py",
                            ".java",
                            ".cpp",
                            ".c",
                            ".json",
                            ".xml",
                            ".csv",
                            ".sql",
                            ".iso"
                        ]

        self.setup_gui()

    # Method for creating and placing entire user interface
    def setup_gui(self):
        self.root.title("File Sorter")

        # Creating and placing widget for source directory labels
        self.label_dir = ttk.Label(self.root, text="Input Directory to Sort:") 
        self.label_dir.grid(row=0, column=0, padx=10, pady=10)

        # Creating and placing widget for source directory input
        self.entry_source_dir = ttk.Entry(self.root, width=40)
        self.entry_source_dir.grid(row=0, column=1, padx=10, pady=10)

        # Creating and placing widget for source directory browse button
        self.browse_button = ttk.Button(self.root, text="Browse", command=self.browse_source_dir)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Creating and placing widget for file extension label
        self.label_extension = ttk.Label(self.root, text="File Extension:")
        self.label_extension.grid(row=1, column=0, padx=10, pady=10)

        # Initializing dictionary and counters to allow dynamic placing of extensions and associated widgets
        self.extension_widgets = {}
        self.row_counter = 2
        self.column_counter = 0

        # Iterates through list of stored extensions and places them in columns of a maximum of 10
        for index, extension in enumerate(self.file_types):
            if index % 10 == 0 and index != 0:
                self.column_counter += 2  # Increase column counter every 10 items
                self.row_counter = 2  # Reset row counter for a new column

            # Creating and placing checkboxes to associate with each extension
            checkbox_state = tk.BooleanVar() # Creates boolean attached to the checkbox specifying true or false
            checkbox = ttk.Checkbutton(self.root, text=extension, variable=checkbox_state)
            checkbox.grid(row=self.row_counter, column=self.column_counter, padx=5, pady=5)

            # Creating and placing widget for destination directory input
            dest_str = tk.StringVar()
            entry_dest_dir = ttk.Entry(self.root, textvariable=dest_str, width=30)
            entry_dest_dir.grid(row=self.row_counter, column=self.column_counter + 1, padx=5, pady=5)

            self.extension_widgets[extension] = (checkbox_state, entry_dest_dir) # Groups each extension with its associated widgets via dictionary
            self.row_counter += 1 # Place each individual extension on new row

        # Creating and placing widget to initailing the sorting sequence
        self.move_button = ttk.Button(self.root, text="Move Files", command=self.sort_files)
        self.move_button.grid(row=self.row_counter + 1, column=0, columnspan=self.column_counter + 2, pady=20)

        # Creating label widget that will tell the user how many files have been moved
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=self.row_counter + 2, column=0, columnspan=self.column_counter + 2)

    # Main logic method
    def sort_files(self):
        source_dir = self.entry_source_dir.get() # Applies the value from the source directory entry field to a variable
        source_dir = self.match_pattern(source_dir) # Removes any quotes around the value using a the match_pattern() function
        
        try:
            if not os.path.exists(source_dir):
                raise FileNotFoundError("Could not find specified directory") # Raises error if source directory cannot be found

            all_files = os.listdir(source_dir) # Tracks all files in source directory
            total_files_moved = 0 # For keeping track of how many files get moved per use

            for extension, (checkbox_state, entry_dest_dir) in self.extension_widgets.items(): # Iterates through dictionary containing all extenions and associated widgets
                if checkbox_state.get(): # Checks if the check box is set to true
                    matching_files = [file for file in all_files if file.endswith(extension)] # Finds all files in source directory with extensions match those of the checked boxes
                    if matching_files: # Detects if there were any matching files
                        # Iterates through the matching files and moves them to the specified destination directory
                        for file in matching_files: 
                            source_path = os.path.join(source_dir, file)
                            destination_dir = os.path.normpath(entry_dest_dir.get())

                            destination_dir = self.match_pattern(destination_dir)

                            shutil.move(source_path, destination_dir)
                            total_files_moved += 1
            
            self.result_label.config(text=f"{total_files_moved} file(s) moved to their specified directory") # Tells the user how many files have just been moved using the incremented counter
        
        # Provides the user with any errors in a messagebox
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Method for creating browse feature for source directory
    def browse_source_dir(self):
        source_dir = filedialog.askdirectory()
        self.entry_dir.delete(0, tk.END)
        self.entry_dir.insert(0, source_dir)

    # Method for pattern recognition
    def match_pattern(self, path):
        # Detects if the given value is wrapped in single or double quotes, if so, it will remove them and return the value
        if re.match(r'^["\'](.*)["\']$', path):
            path = re.match(r'^["\'](.*)["\']$', path).group(1)
        return path


def main():
    root = tk.Tk()
    App(root) # Create instance of App class
    root.mainloop() # Run the GUIs main loop

if __name__ == "__main__":
    main()