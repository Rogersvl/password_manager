import tkinter
from tkinter import *
from tkinter import messagebox
from characters import letters, cap_let, numbers, special
import random
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.exc import IntegrityError


class Base(DeclarativeBase):
    pass


class PasswordEntrance(Base):
    __tablename__ = 'passwords'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(25), nullable=False)


engine = create_engine('sqlite:///passwords.db', echo=True)

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def add_values():
    app_email = email_entry.get()
    app_site = app_name_entry.get()
    app_password = password_entry.get()

    if len(app_email) == 0 or len(app_site) == 0 or len(app_password) == 0:
        messagebox.askokcancel(title='Warning!', message='Não deixe os campos vazios!')
    else:
        try:
            novos_dados = PasswordEntrance(site=app_site, email=app_email, password=app_password)
            session.add(novos_dados)
            session.commit()
        except IntegrityError:
            session.rollback()
            messagebox.showwarning(title='Erro', message=f'O site informado já está cadastrado no banco de dados. '
                                                         f'Use a funcionalidade "Search"')
        except Exception as e:
            session.rollback()
            messagebox.showerror(title='Erro inesperado', message=f"Ocorreu um erro: {e}")


def generate_password():
    g_pass = [letters, cap_let, numbers, special]
    psw = ''.join(
        random.choice(x) for x in g_pass for _ in range(2)
    )
    psw = ''.join(random.sample(psw, len(psw)))
    password_entry.insert(string=psw, index=0)


def search_info():
    user_entrada = app_name_entry.get().title()
    resultado = session.query(PasswordEntrance).filter_by(site=user_entrada).first()
    if resultado:
        messagebox.showinfo(title='Sucesso!', message=f'Email: {resultado.email} \n Senha: {resultado.password}')
    else:
        messagebox.showerror(title='Não encontrado', message='O site informado não está no banco de dados.')


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
