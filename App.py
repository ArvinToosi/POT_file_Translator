import polib
from googletrans import Translator
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from termcolor import colored
po = polib.POFile()
po.metadata = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'you@example.com',
    'POT-Creation-Date': '2007-10-18 14:00+0100',
    'PO-Revision-Date': '2007-10-18 14:00+0100',
    'Last-Translator': 'you <you@example.com>',
    'Language-Team': 'English <yourteam@example.com>',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
}

def save_email():
    email = "arvintoosi01@gmail.com"  # Replace this with your email
    messagebox.showinfo("Email", f"You can reach me at: {email}")

def translate_pot_to_po(pot_file_path):
    pofile = polib.pofile(pot_file_path)

    list_1 = []
    list_2 = []

    translator = Translator()

    total_entries = len(pofile)
    progress_var.set(0)
    progress_bar.update()
    print(colored("File translation started!","red"))
    for i, entry in enumerate(pofile):
        input_text = str(entry.msgid)

        # Skip translation for items containing '%'
        if "%" in input_text:
            translated_text = ""
        else:
            while True:
                try:
                    print(colored("Item"+str(i+1),"green")+" has been translated successfully")
                    result = translator.translate(input_text, src="en", dest="fa")
                    translated_text = result.text
                    break  # Break out of the loop if the translation is successful
                except Exception as e:
                    print(f"An error occurred while translating: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)

        list_1.append(input_text)
        list_2.append(translated_text)

        # Update progress bar
        progress_var.set((i + 1) * 100 // total_entries)
        progress_bar.update()

    print(colored("File translation ends!","red"))

    # Writing the translations to the new .po file
    po_file_path = filedialog.asksaveasfilename(filetypes=[("PO Translation", "*.po")], defaultextension=".po")
    if po_file_path:
        for i in range(len(list_1)):
            entry = polib.POEntry(
                msgid=list_1[i],
                msgstr=list_2[i],
            )
            po.append(entry)
        po.save(po_file_path)
        messagebox.showinfo("Translation Complete", f"New PO file '{po_file_path}' has been created.")
        
        # Ask for the .mo file path
        mo_file_path = filedialog.asksaveasfilename(filetypes=[("Compiled Translation", "*.mo")], defaultextension=".mo")
        if mo_file_path:
            po.save_as_mofile(mo_file_path)
            messagebox.showinfo("Translation Complete", f"New MO file '{mo_file_path}' has been created.")

def browse_pot_file():
    file_path = filedialog.askopenfilename(filetypes=[("POT files", "*.pot")])
    pot_file_entry.delete(0, tk.END)
    pot_file_entry.insert(tk.END, file_path)

def translate_pot_to_po_gui():
    pot_file_path = pot_file_entry.get()

    if not pot_file_path.endswith(".pot"):
        messagebox.showerror("Error", "Please select a .POT file.")
        return

    translate_pot_to_po(pot_file_path)

# Create the main application window
app = tk.Tk()
app.title("POT to PO Translator")

# Create and place the GUI widgets
pot_file_label = tk.Label(app, text="Select .POT file:")
pot_file_label.pack(pady=5)

pot_file_entry = tk.Entry(app, width=50)
pot_file_entry.pack(pady=5)

pot_file_button = tk.Button(app, text="Browse", command=browse_pot_file)
pot_file_button.pack(pady=5)

translate_button = tk.Button(app, text="Translate", command=translate_pot_to_po_gui)
translate_button.pack(pady=10)

progress_var = tk.IntVar()
progress_bar = Progressbar(app, variable=progress_var, maximum=100)
progress_bar.pack(pady=5)

created_by_label = tk.Label(app, text="Created by Arvin Toosi")
created_by_label.pack(side="left", padx=5, pady=5, anchor="sw")

# Add the label for the email (Clickable)
email_label = tk.Label(app, text="Contact Me", fg="blue", cursor="hand2")
email_label.pack(side="right", padx=5, pady=5, anchor="se")
email_label.bind("<Button-1>", lambda event: save_email())

# Start the main loop
app.mainloop()
