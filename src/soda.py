import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
import tkinter.font

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
            "Welcome to Soda code editor 0.1.1!\n\nThis program is in development and can contain some or many errors.\n\nLet me know about any issue here:\n\nhttps://github.com/joelemiliano/soda/issues"
        )

        # Load background image
        self.bg_image = PhotoImage(file="icongrayscale.png")  # Your background image
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Fill the entire window

        # Create Text widget
        self.text_area = tk.Text(self.root, wrap="word", undo=True, highlightthickness=0, font='TkFixedFont')
        self.text_area.pack(expand=True, fill="both")

        # Create Menu Bar
        self.create_menu()

        # File and Undo/Redo operations
        self.file_chooser = None

        # Bind the Text widget to check for changes (e.g., when typing)
        self.text_area.bind("<KeyRelease>", self.check_empty)

        # Initial check to update background based on text area content
        self.check_empty()

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
        file_menu.add_command(label="New", command=self.new_file)
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

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def undo(self):
        self.text_area.edit_undo()

    def redo(self):
        self.text_area.edit_redo()

    def check_empty(self, event=None):
        """Check if the text area is empty and update the background image."""
        # Check if the Text widget is empty
        if not self.text_area.get("1.0", "end-1c").strip():  # Text widget is empty
            self.bg_label.place(relwidth=1, relheight=1)  # Show background image
        else:
            self.bg_label.place_forget()  # Remove the background image

    def exit_program(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    editor = SodaEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
