import tkinter as tk
from tkinter import ttk
import requests  

class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Movies Rating App")
        
        bg_color = "#2E2E2E"
        fg_color = "white"
        button_color = "#3E3E3E"
        font_style = ("Arial", 12)

        self.root.config(bg=bg_color)

        self.mylabel = tk.Label(self.root, text="Enter movie title:", font=font_style, bg=bg_color, fg=fg_color)
        self.mylabel.pack(pady=10)

        self.menu_var = tk.StringVar(self.root)
        self.menu_var.set("Movies")
        self.menu = ttk.Combobox(self.root, textvariable=self.menu_var, values=["Movies", "Actors", "Reviews"])
        self.menu.config(font=font_style, background=button_color, foreground=fg_color, width=15)
        self.menu.pack(pady=10)

        self.myentry = tk.Entry(self.root, font=font_style, bg=button_color, fg=fg_color)
        self.myentry.pack(pady=10)

        self.submit = tk.Button(self.root, text="Search", font=font_style, command=self.get_entry_text, bg=button_color, fg=fg_color)
        self.submit.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=font_style, bg=bg_color, fg=fg_color)
        self.result_label.pack(pady=10)

        self.root.mainloop()

    def get_entry_text(self):
        entry_text = self.myentry.get().lower()
        selected_option = self.menu_var.get().lower()
        self.myentry.delete(0, tk.END)
        response = requests.get(f"http://127.0.0.1:5000/{selected_option}/{entry_text}")
        if response.status_code == 200:
            data = response.json()
            if selected_option == "movies":
                formatted_data = '\n'.join([f"{key} : {value}" for key, value in data.items()])
                print(formatted_data)
            elif selected_option == "actors":
                movies_data = ''.join(a for a in data)
                formatted_data = "Known for :\n\n" + movies_data
                print(formatted_data)
            else:
                name = f"Movie name: {data[1]}\n"
                quotes_data = '\n'.join([f'{key} : "{value}"' for key, value in data[0].items()])
                formatted_data = name + quotes_data
                print(formatted_data)
            self.update_label(formatted_data)

    def update_label(self, data):
        self.result_label.config(text=data)
        
MyGui()