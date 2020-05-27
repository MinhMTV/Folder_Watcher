from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import Handler as h
import threading

filename = ""


def background(func, args):
    th = threading.Thread(target=func, args=args)
    th.daemon = True
    th.start()

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
#    global folder_path
    global filename
    filename = filedialog.askdirectory()
#   folder_path.set(filename)
    h.watchDir(filename)

def button_action():
    global filename
    if len(filename) > 0:
        print(filename)
        print("Der Ordner wurde gespeichert")
    else:
        print(filename)
        print("Bitte einen Order zum Beobachten auswählen")


def action_get_info_dialog():
    m_text = "\
************************\n\
Autor: Minh Tuan Vuong \n\
Date: 27.05.2020\n\
Version: 1.00\n\
************************"
    messagebox.showinfo(message=m_text, title="Infos")

def minimize_win():
    global fenster
    Wm.iconify(fenster)

def main():
    global filename

    fenster = Tk()

    fenster.title("Folder Watcher")

    info_text = Label(fenster, text="Suche den Ordner aus, denn du beobachten möchtest!")
    info_text.grid(row=0, column=0, pady = 20)

    # Menüleiste erstellen
    menuleiste = Menu(fenster)

    lbl1 = Label(master=fenster, textvariable=filename)
    lbl1.grid(row=1, column=0)
    button2 = Button(text='Durchsuche', command= lambda : background(browse_button, ()))
    button2.grid(row=2, column=0, pady = 20)



    # Menü Datei und Help erstellen
    datei_menu = Menu(menuleiste, tearoff=0)
    help_menu = Menu(menuleiste, tearoff=0)

    # Beim Klick auf Datei oder auf Help sollen nun weitere Einträge erscheinen.
    # Diese werden also zu "datei_menu" und "help_menu" hinzugefügt
    datei_menu.add_command(label="Speichern", command=button_action)
    # datei_menu.add_separator()  # Fügt eine Trennlinie hinzu
    datei_menu.add_command(label="Minimiere", command=minimize_win)
    datei_menu.add_separator()  # Fügt eine Trennlinie hinzu
    datei_menu.add_command(label="Exit", command=fenster.quit)

    help_menu.add_command(label="Info!", command=action_get_info_dialog)

    # Nun fügen wir die Menüs (Datei und Help) der Menüleiste als
    # "Drop-Down-Menü" hinzu
    menuleiste.add_cascade(label="Datei", menu=datei_menu)
    menuleiste.add_cascade(label="Help", menu=help_menu)

    # Die Menüleiste mit den Menüeinrägen noch dem Fenster übergeben und fertig.
    fenster.config(menu=menuleiste)

    fenster.mainloop()

if __name__ == '__main__':
    stop_threads = False
    main()