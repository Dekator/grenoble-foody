# -*- coding: utf-8 -*-
"""
Programme principal,
Auteurs : elliot.lambert, evan.daniel, louafi.zerguine, nassim.zerouali, ahmed.zaafane.
Projet terminé.
"""

from tkinter import *
from tkinter import ttk
import sqlite3
import maps
import webbrowser
from init_window import *

# Ce code est inspiré de plusieurs vidéos youtube et de forums stackoverflow, 
# qui nous ont apportés les connaissances nécessaires pour manier les bilblilhoteques sqlite3 et tkinter.

def elem_select(event):
    '''
    Evenement déclenché lorsque un element du menu déroulant est pressé.
    '''
    canvas.yview_moveto( 0 )
    if(combo.get() == "defaut"):
        trier(True, 0)
    elif(combo.get() == "favori"):
        trier(False, 0)
    elif(combo.get() == "prix"):
        trier(True, 1)
    elif(combo.get() == "note"):
        trier(True, 2)

def scroll_souris(event):
    '''
    Permet de scroller avec la souris.
    '''
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def lien_url(url):
    webbrowser.open(url)


# Associe la fonction on_select et la fonction on_mousewheel aux elements de l'affichage concernés
combo.bind("<<ComboboxSelected>>", elem_select)

window.bind_all("<MouseWheel>", scroll_souris)

# Crée un menu déroulant pour afficher la map.
afficher_menu = Menu(menu_bar, tearoff=0, bg='black', fg='white')
menu_bar.add_cascade(label="Maps", menu=afficher_menu)
afficher_menu.add_command(label="Afficher la carte", command=lambda: maps.new_map(window,(45.1666700,5.7166700,"Grenoble")))

# Crée un menu déroulant pour les liens utiles.
afficher_menu = Menu(menu_bar, tearoff=0, bg='black', fg='white')
menu_bar.add_cascade(label="Lien utiles", menu=afficher_menu)
afficher_menu.add_command(label="Crous Grenoble", command=lambda: lien_url("https://www.crous-grenoble.fr/se-restaurer/"))
afficher_menu.add_command(label="Carte avantage étudiant", command=lambda: lien_url("https://www.emblemgrenoble.com/"))

def add_favori(id_button, trie):

    '''
    Prend en entrée l'id du bouton pressé, et un booleen pour savoir si la liste est triée par favori ou non.
    Ne renvoie rien en sortie.
    Ajoute le bon plan dans la base données favori lorsqu'un bouton est pressé.
    '''

    global id_favori

    cursor.execute("SELECT * FROM restaux WHERE id = (?)", (str(id_button)))
    b = cursor.fetchall()
    a = b[0]

    cursor.execute("SELECT * FROM favori")
    dffav = cursor.fetchall()
    id_favori = 1

    for e in dffav:
        if(id_button > e[0]):
            id_favori += 1

    if(favori_push[id_button - 1]):
        if not trie:
            cursor.execute("DELETE FROM favori WHERE id = (?)",(str(id_button)))
        else:
            cursor.execute("DELETE FROM favori WHERE id = (?)",(str(id_button)))

        favori_push[id_button - 1] = False
        favori_button[id_button - 1].config(bg='black', fg = 'white')
        id_favori -= 1

        if not trie:
            trier(False,0)
    else:
        cursor.execute("INSERT INTO favori VALUES(?, ?)",(str(id_button),str(id_favori)))

        favori_push[id_button - 1] = True
        favori_button[id_button - 1].config(bg='yellow', fg = 'black')

    db.commit()

def trier(default, type):
    '''
    Prend en entrée un booleen default pour savoir si l'affichage souhaité est celui par default ou non.
    Ne ressors rien en sortie.
    Trie les données pour l'affichage.
    '''

    # Supprime tout les elements du canvas (tout les elements de la base de donnée affichés à l'écran).
    for widget in canvas.winfo_children():
        widget.destroy()
        
    frame = Frame(canvas, bg='#000d1a')
    canvas.create_window(0, 0, anchor=NW, window=frame)

    if(not default):
        cursor.execute("SELECT restaux.* FROM restaux JOIN favori ON restaux.id = favori.id WHERE restaux.id = favori.id")
        dffav = cursor.fetchall()
        affiche(frame,dffav, default)
    elif(type == 0):
        affiche(frame,df, default)
    elif(type == 1):
        cursor.execute("SELECT * FROM restaux ORDER BY PrixMoyen ASC")
        dftype = cursor.fetchall()
        affiche(frame,dftype, default)
    else:
        cursor.execute("SELECT * FROM restaux ORDER BY Note DESC")
        dftype = cursor.fetchall()
        affiche(frame,dftype, default)
    

def affiche(frame, data, defaut):
    '''
    Prend en entrée une frame, c'est à dire une partie de l'écran ou l'on va afficher les données.
    Prend également une liste data qui contient les elements de la base de données,
    et un booleen qui permet de savoir si l'affichage souhaité est celui par défaut.
    Ne renvoie rien en sortie.
    La fonction affiche à l'écran les données.
    '''

    favori_push.clear()
    favori_button.clear()
    cursor.execute("SELECT * FROM favori")
    dffav = cursor.fetchall()
    for e in df:
        favori_push.append(False)
        favori_button.append(False)
    for e in dffav:
        favori_push[e[0] - 1] = True

    center = Label(frame, text="", font=('Arial', 1), bg='#000d1a', fg='white') # element qui permet de centrer tout les elements
    center.pack(side=TOP, pady=0, padx=540)
        
    for element in data: # Affiche chaque element un par un.
        nom = str(element[0])
        note = element[1]
        regime = element[2]
        type = element[3]
        prix_moyen = element[4]
        coordx = element[5]
        coordy = element[6]
        source_img = element[7]
        id = element[8] - 1

        new = Label(frame, text=nom, font=('Gobold', 20), bg='#000d1a', anchor='w', cursor="hand2", fg='white', highlightcolor='blue')
        new.pack(side=TOP, pady=3)
        new.bind("<Button-1>", lambda e, coord=(coordx, coordy, nom): maps.new_map(window,coord))
        new.bind("<Enter>", afficher_texte)
        new.bind("<Leave>", lambda e, :supprimer_texte())

        notelabel = Label(frame, text=type +", Note : " + note + ", Prix moyen pour un repas : " + str(prix_moyen) + " Euros.", font=('Gobold', 12), bg='#000d1a', fg='white')
        notelabel.pack(side=TOP, pady=3)

        colorbg = ""
        colorfg = ""

        if(favori_push[id] == True): 
            colorbg = "yellow"
            colorfg = "black"
        else:
            colorbg = "black"
            colorfg = "white"

        favori_button[id] = Button(frame, text="Favori", command=lambda u=id+1: add_favori(u, defaut), bg=colorbg, fg=colorfg)
        favori_button[id].pack(side=TOP)
        
        img = PhotoImage(file = source_img)
        img_label = Label(frame, image=img, bg='#000d1a')
        img_label.image = img
        img_label.pack(side=TOP, pady=5, padx=200)

        text_label = Label(frame, text="Régime : " + regime, font=('Arial', 12), bg='#000d1a', fg='white')
        text_label.pack(side=TOP, pady=5, padx=300) 
        
    
    scrollbar.config(command=canvas.yview) # Attache le canvas à la barre de scroll
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def afficher_texte(event):
    '''
    Evenement qui se déclenche lorsque la souris passe sur un nom de restaurant.
    Il affiche un texte a la position de la souris.
    '''
    global text_map
    text_map = Label(window, text="Affiche les coordonnées sur la map", font=('Arial', 8), bg='grey', fg='white')
    text_map.place(x=event.x_root - window.winfo_rootx() + 10, y=event.y_root - window.winfo_rooty() - 10)

def supprimer_texte():
    '''
    Cet evenement supprime le texte créé auparavant quand la souris quitte le nom de restaurant.
    '''
    text_map.destroy()

# Gère la base de donnée s'occupant des favoris
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS favori (id INTEGER, idfavori INTEGER NOT NULL)")

# Initialise les listes nécessaires au bon déroulement du programme.
favori_push = []
favori_button = []

# Lance un premier affichage par default.
trier(True, 0)

# Boucle d'affichage
window.mainloop()


