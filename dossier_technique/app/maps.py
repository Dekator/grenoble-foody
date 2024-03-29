from tkinter import *

imported = True
try:                          # Vérifie si le module peut être importé correctement.
    import tkintermapview      
except Exception as e:
    print(e)
    imported = False

# code inspiré de la page github suivante : https://github.com/TomSchimansky/TkinterMapView
# cette page est la page du créateur de la bilbilhoteque tkintermapview.

def new_map(tk, coord):
    '''
    Prend en entrée une fenetre tkinter et des coordonnées sous forme de tuple.
    Ne renvoie rien en sortie.
    La fonction crée une instance de la fenetre (crée une nouvelle petite fenetre enfant de la fenetre tk),
    et affiche si le module est bien installé la map avec un marqueur aux coordonnées coord.
    '''
    if(imported):
        x, y, a = coord
        map = Toplevel(tk) 
        map.title('map')
        map.geometry('500x350')
        map.resizable(False, False)
        map.iconbitmap("ico.ico")
        map.config(background='#000d1a')

        my_label = LabelFrame(map)
        my_label.pack()
        
        map_widget = tkintermapview.TkinterMapView(my_label, width= 800, height= 600, corner_radius= 0)



        #coordonnées
        map_widget.set_position(x, y)

        #markeur
        if(a != "Grenoble"):
            marker_ = map_widget.set_marker(x, y, text=a)
            
        #zoom
        map_widget.set_zoom(14)



        map_widget.pack()

        map.mainloop()
    else:
        map = Toplevel(tk) 
        map.title('map')
        map.geometry('500x350')
        map.resizable(False, False)
        map.iconbitmap("ico.ico")
        map.config(background='white')

        erreur = Label(map, text='Erreur lors de l\'importation', font=("Arial Black", 20), bg='white', fg='black')
        erreur.place(x=50,y=50)
        erreur2 = Label(map, text='du module tkintermapview', font=("Arial Black", 20), bg='white', fg='black')
        erreur2.place(x=50,y=100)
        
