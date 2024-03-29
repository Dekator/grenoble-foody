from tkinter import *
from tkinter import ttk
import sqlite3



# Création de la fenetre
window = Tk()
window.title("Grenoble Foody")
window.geometry("1080x720")
window.resizable(False, False)
window.iconbitmap("ico.ico")
window.config(background='#000d1a')



menu_bar = Menu(window, bg='black', fg='white', activebackground='black', activeforeground='white')
window.config(menu=menu_bar)

titre = Label(window, text='Bons plans Grenoble', font=("Arial Black", 40), bg='#000d1a', fg='#E1CE7A')
titre.pack()

Restaux = Label(window, text='   Trier par : ', font=('Arial', 15), bg='#000d1a', anchor='w', fg='white')
Restaux.pack(fill='both')

# Création d'une liste de valeurs pour le menu déroulant
options = ["defaut", "favori", "prix", "note"]

# Création du menu déroulant
combo = ttk.Combobox(window, values=options, state="readonly")
combo.set("defaut") 
combo.place(anchor='nw', x=110,y=86)



# Récupération des données de la base de données
db = sqlite3.connect("ugaResto.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM restaux")
df = cursor.fetchall()
print(df)



# Configuration de la barre de scroll
scrollbar = Scrollbar(window)
scrollbar.place(anchor='ne')
canvas = Canvas(window, yscrollcommand=scrollbar.set, bg='#000d1a', highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)
