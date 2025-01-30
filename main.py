import tkinter
from tkinter import *
from tkinter import messagebox
from characters import letters, cap_let, numbers, special
import json
import random


def add_values():
    email_get = email_entry.get()
    site = app_name_entry.get().title()
    u_password = password_entry.get()
    add_json = {
        site: {
            "email": email_get,
            "password": u_password
        }
    }
    if len(email_get) == 0 and len(site) == 0 and len(u_password) == 0:
        messagebox.askokcancel(title="Warning!", message='dont leave nothing empty!')
    else:
        file_path = "file.json"

        try:
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                    if not isinstance(data, dict):
                        data = {}
                except json.JSONDecodeError:
                    data = {}
        except FileNotFoundError:
            data = {}

        data.update(add_json)

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)


def generate_password():
    g_pass = [letters, cap_let, numbers, special]
    psw = ''.join(
        random.choice(x) for x in g_pass for _ in range(2)
    )
    psw = ''.join(random.sample(psw, len(psw)))
    password_entry.insert(string=psw, index=0)


def search_info():
    user_info = app_name_entry.get().title()
    with open('file.json', 'r') as f:
        data = json.load(f)
        try:
            info = data[user_info]
            messagebox.showinfo(title='Info', message=f"Email: {info['email']}\nPassword: {info['password']}")
        except KeyError:
            messagebox.askokcancel(title='Warning!', message=f"{user_info} is not in the database.")


tk_window = tkinter.Tk()
tk_window.title("Password manager!")
tk_window.config(padx=20, pady=20)
canvas = Canvas(height=200, width=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)


app_name = Label(text='Site:')
app_name_entry = Entry(width=36)
email = Label(text='Email/Username:')
email_entry = Entry(width=36)
password = Label(text='Password:')
password_entry = Entry(width=21)
generate_password = Button(text='Generate Password', command=generate_password)
add_button = Button(width=36, text='add', command=add_values)
search_button = Button(text='Search', command=search_info)


app_name.grid(row=1, column=0)
app_name_entry.grid(row=1, column=1, columnspan=2, sticky='w')
email.grid(row=2, column=0)
email_entry.grid(row=2, column=1, columnspan=2, sticky='w')
password.grid(row=3, column=0)
password_entry.grid(row=3, column=1, sticky='w')
generate_password.grid(row=3, column=2, sticky='w')
add_button.grid(row=4, column=1, columnspan=2, sticky='w')
search_button.grid(row=1, column=2)


tk_window.mainloop()
