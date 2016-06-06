#coding utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

#Importo lo script .py dove ci sono le funzioni che servono
import calcoloVettoreMatrici

class Handler:
    """GUI (Graphical User Interface)"""
    def window1_destroy(self, *args):
        Gtk.main_quit(*args)

    #Procedura che permette di eseguire l'algoritmo di Viterbi sul testo inserito dall'utente
    def correggi_clicked(self, button):
        start_iter = builder.get_object("textview").get_buffer().get_start_iter()
        end_iter = builder.get_object("textview").get_buffer().get_end_iter()
        #print builder.get_object("textview").get_buffer().get_text(start_iter, end_iter, True)
        sequenza = calcolatore.inferenza(modello, builder.get_object("textview").get_buffer().get_text(start_iter, end_iter, True).lower())
        builder.get_object("textview2").get_buffer().set_text(sequenza)     
        
    def pulisci_clicked(self, button):
        builder.get_object("textview").get_buffer().set_text("")
        builder.get_object("textview2").get_buffer().set_text("")

    
#Chiamate alle procedure per calcolare il vettore pi, le matrici T e O e per creare il modello
calcolatore = calcoloVettoreMatrici.calcoloVettoreMatrici()
pi = calcolatore.calcolo_vettore_pi()
matrice_T = calcolatore.calcolo_matrice_transizioni()
matrice_O = calcolatore.calcolo_matrice_osservazioni()
modello = calcolatore.creazione_modello(matrice_T, matrice_O, pi)
#print calcolatore.test(modello)

#Settaggi della GUI (e.g. nome della finestra della GUI e la sua dimensione)
builder = Gtk.Builder()
builder.add_from_file("HMM.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
