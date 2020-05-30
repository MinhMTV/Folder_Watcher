from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from pystray import MenuItem as item
import os
# main_with_ini.py
import configparser
import pystray
from PIL import Image, ImageDraw
import Handler as h
import threading
import getpass

filename = ""
configfile_name = "config.ini"
icon_name = "icon.png"
mainwindow = Tk()
folder_path = StringVar()
USER_NAME = getpass.getuser()
CHECKBOX_STATE = 0
STARTUP_NAME = "open.bat"
STARTUP_PATH = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
STARTUP_KEY = "startup"


# print('sys.argv[0] =', sys.argv[0])
# pathname = os.path.dirname(sys.argv[0])
# print('path =', pathname)
# print('full path =', os.path.abspath(pathname))


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.realpath(__file__)
    with open(STARTUP_PATH + '\\' + STARTUP_NAME, "w+") as bat_file:
        bat_file.write(f'start "" "{file_path}"  "{STARTUP_KEY}"')


def remove_startup():
    try:
        os.remove(os.path.join(STARTUP_PATH, STARTUP_NAME))
    except OSError:
        pass


def createConfig(configfile_name, section, key, value):
    global filename
    config = os.path.join(os.path.dirname(sys.argv[0]), configfile_name)
    write_config = configparser.ConfigParser()
    write_config.read(config)
    if write_config.has_section(section):
        write_config.set(section, key, value)
        with open(config, 'w') as cgfile:
            write_config.write(cgfile)
    else:
        write_config.add_section(section)
        write_config.set(section, key, value)
        cfgfile = open(config, 'w')
        write_config.write(cfgfile)
        cfgfile.close()


# Check if there is already a configuration file
def checkConfig(configfile_name):
    config = os.path.join(os.path.dirname(sys.argv[0]), configfile_name)
    # Create the configuration file as it doesn't exist yet
    if os.path.isfile(config):
        read_config = configparser.ConfigParser()
        read_config.read(config)
        if read_config.has_section('Folder_WatchPath'):
            watchPath = read_config['Folder_WatchPath']['PATH']
            folder_path.set(watchPath)
            return watchPath

    else:
        print('no config file yet')


def checkSetting(configfile_name):
    config = os.path.join(os.path.dirname(sys.argv[0]), configfile_name)
    # Create the configuration file as it doesn't exist yet
    if os.path.isfile(config):
        read_config = configparser.ConfigParser()
        read_config.read(config)
        if read_config.has_section('SETTINGS'):
            autostart = read_config['SETTINGS']['AUTOSTART']
            return autostart

    else:
        print('No setting File')
        return False


def checkWatchfolder(watchPath):
    if watchPath:
        print("Watched Folder is " + watchPath)
        background(lambda: h.watchDir(watchPath), ())
    else:
        print("No Watched Folder defined yet")


# Systemtray
def quit_window(icon, item, window):
    icon.stop()
    window.destroy()


def show_window(icon, item, window):
    icon.stop()
    window.after(0, window.deiconify)


def setup(icon):
    icon.visible = True


def withdraw_window(window):
    window.withdraw()
    image = Image.open(os.path.join(os.path.dirname(sys.argv[0]), icon_name))
    menu = pystray.Menu(item('Show', lambda: show_window(icon, menu, window)),
                        item('Quit', lambda: quit_window(icon, menu, window)))

    icon = pystray.Icon("name", image, "FolderWatcher", menu)
    icon.run(setup)


def settings():
    settings = Toplevel()
    settings.title("Settings")
    positioning_win(settings)
    settings.grid_rowconfigure(0, weight=1)
    settings.grid_columnconfigure(0, weight=1)

    info_text = Label(settings, text="Start Script on Windows Startup")
    info_text.grid(row=0, column=0, pady=20)
    boolvar = BooleanVar()
    autostart = checkSetting(configfile_name)
    boolvar.set(autostart)

    Checkbutton(settings, text="Autostart", variable=boolvar).grid(row=0,
                                                                   sticky=W)
    btn_save_set = Button(settings, text='Save', command=lambda: saveSettings(settings, boolvar))
    btn_save_set.grid(row=2, column=0)
    settings.mainloop()


def saveSettings(window, checkbox):
    messagebox.showinfo(message="Settings were saved", title="Save")
    if checkbox.get():
        temp = "True"
        createConfig(configfile_name, "SETTINGS", "AUTOSTART", temp)
        add_to_startup()

    else:
        temp = "False"
        createConfig(configfile_name, "SETTINGS", "AUTOSTART", temp)
        remove_startup()
    window.destroy()


def background(func, args):
    th = threading.Thread(target=func, args=args)
    th.daemon = True
    th.start()


def changePath():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global filename
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    if len(filename) > 0:
        h.watchDir(filename)


def savePATH():
    global filename
    if len(filename) > 0:
        createConfig(configfile_name, "Folder_WatchPath", "PATH", filename)
        messagebox.showinfo(message="Folder were saved", title="Info")
    else:
        messagebox.showinfo(message="Please choose a folder to watch", title="Info")


def action_get_info_dialog():
    m_text = "\
************************\n\
Autor: Minh Tuan Vuong \n\
Date: 27.05.2020\n\
Version: 1.00\n\
Email: Minhtv@web.de\n\
************************"
    messagebox.showinfo(message=m_text, title="Infos")


def minimize_win(window):
    Wm.iconify(window)


def on_closing(window):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


def positioning_win(win):
    # Gets the requested values of the height and widht.
    windowWidth = win.winfo_reqwidth()
    windowHeight = win.winfo_reqheight()
    print("Width", windowWidth, "Height", windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(win.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(win.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    win.geometry("+{}+{}".format(positionRight, positionDown))


def main():
    mainwindow.title("Folder Watcher")
    positioning_win(mainwindow)
    mainwindow.grid_rowconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(0, weight=1)
    mainwindow.iconphoto(True, PhotoImage(file=os.path.join(os.path.dirname(sys.argv[0]), icon_name)))

    info_text = Label(mainwindow, text="Please choose the folder that you want to watch!")
    info_text.grid(row=0, column=0, pady=20)

    # create menu
    menubar = Menu(mainwindow)

    lbl1 = Label(master=mainwindow, textvariable=folder_path)
    lbl1.grid(row=1, column=0)
    button2 = Button(text='Select', command=lambda: background(changePath, ()))
    button2.grid(row=2, column=0, pady=20)

    # file menu and help menu to menu bar
    file_menu = Menu(menubar, tearoff=0)
    help_menu = Menu(menubar, tearoff=0)

    # click on file or help menu to open other menus
    file_menu.add_command(label="Save", command=savePATH)
    file_menu.add_command(label="Minimize", command=lambda: withdraw_window(mainwindow))
    file_menu.add_separator()  # Add a seperator
    file_menu.add_command(label="Settings", command=settings)
    file_menu.add_separator()  # Add a seperator
    file_menu.add_command(label="Exit", command=mainwindow.destroy)

    help_menu.add_command(label="Info!", command=action_get_info_dialog)

    # add menu to menu bar
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Help", menu=help_menu)

    # give menu to menu bar
    mainwindow.config(menu=menubar)

    mainwindow.protocol('WM_DELETE_WINDOW', lambda: on_closing(mainwindow))

    mainwindow.mainloop()


if __name__ == '__main__':
    filename = checkConfig(configfile_name)
    checkWatchfolder(filename)
    for arg in sys.argv:
        print('Argument: ', arg)
        if arg == STARTUP_KEY:
            withdraw_window(mainwindow)
    main()
