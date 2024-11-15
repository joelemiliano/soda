import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog

class SodaEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Soda")
        self.root.geometry("800x600")

        # Set window icon (make sure to have 'icon.png' file in your directory)
        icon = PhotoImage(file="icon.png")
        self.root.iconphoto(True, icon)

        # Welcome message
        messagebox.showinfo("Welcome", 
            "Welcome to Soda code editor 0.2!\n\nThis program is in development and can contain some or many errors.\n\nLet me know about any issue here:\n\nhttps://github.com/joelemiliano/soda/issues"
        )

        # Tab system
        self.tabs = {}  # Store tabs with content
        self.tab_buttons = {}  # Store tab button references
        self.current_tab = None

        # Create the Text widget (one text area for all tabs)
        self.text_area = tk.Text(self.root, wrap="word", undo=True, highlightthickness=0, font='TkFixedFont')
        self.text_area.pack(expand=True, fill="both")

        # Create the Tab Bar (a frame containing tab buttons)
        self.tab_bar = tk.Frame(self.root)
        self.tab_bar.pack(side="bottom", fill="x", anchor="w")

        # Create the first (default) tab
        self.create_new_tab()

        # Create Menu Bar
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Soda Menu
        soda_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Soda", menu=soda_menu)
        soda_menu.add_command(label="Exit", command=self.exit_program)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_new_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

        # Keyboard shortcuts for undo/redo
        self.text_area.bind("<Control-z>", lambda event: self.undo())
        self.text_area.bind("<Control-y>", lambda event: self.redo())

    def create_new_tab(self):
        # Create a new tab
        tab_name = f"Untitled-{len(self.tabs) + 1}"
        self.tabs[tab_name] = ""  # Create empty content for the tab

        # Create a tab button
        new_tab_button = tk.Button(self.tab_bar, text=tab_name, command=lambda: self.switch_tab(tab_name))
        new_tab_button.pack(side="left", padx=5)

        # Store the tab button in a dictionary
        self.tab_buttons[tab_name] = new_tab_button

        # If no tab is selected, select the new one
        if not self.current_tab:
            self.switch_tab(tab_name)

        # Hide the tab bar if there's only one tab
        self.update_tab_bar_visibility()

    def switch_tab(self, tab_name):
        # Save the current tab's content to its dictionary entry
        if self.current_tab:
            self.tabs[self.current_tab] = self.text_area.get(1.0, tk.END).strip()  # Save content of the previous tab

        # Update the content in the text area for the selected tab
        self.current_tab = tab_name
        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.text_area.insert(tk.END, self.tabs[tab_name])  # Load the content for the selected tab

        # Hide the tab bar if there's only one tab
        self.update_tab_bar_visibility()

    def update_tab_bar_visibility(self):
        # If there's more than one tab, show the tab bar
        if len(self.tabs) > 1:
            self.tab_bar.pack(side="bottom", fill="x", anchor="w")
        else:
            self.tab_bar.pack_forget()  # Hide the tab bar when there's only one tab

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.tabs[self.current_tab] = content  # Save content to current tab
                self.switch_tab(self.current_tab)  # Refresh the content in the text area

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # Save the content of the current tab to the file
            with open(file_path, "w") as file:
                file.write(self.tabs[self.current_tab])  # Save current tab content to file

            # Get the new tab name from the file name (without extension)
            new_tab_name = file_path.split("/")[-1].split(".")[0]  # Extract filename without extension
            
            # Save the content under the new tab name
            old_content = self.tabs.pop(self.current_tab)  # Pop the old tab content
            self.tabs[new_tab_name] = old_content  # Save content under the new tab name

            # Update the tab button reference
            self.tab_buttons[new_tab_name] = self.tab_buttons.pop(self.current_tab)  # Move button reference
            self.tab_buttons[new_tab_name].config(text=new_tab_name)  # Update the button text

            # Switch to the newly renamed tab
            self.switch_tab(new_tab_name)

            # Hide the tab bar if there's only one tab
            self.update_tab_bar_visibility()

    def undo(self):
        self.text_area.edit_undo()

    def redo(self):
        self.text_area.edit_redo()

    def exit_program(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    editor = SodaEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
