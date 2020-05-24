from __future__ import generators
import os
import sys

try:
    import queue
except ImportError:
    import Queue as queue
import threading
import time
import FileLib as f

import win32file
import win32con

global ext

ACTIONS = {
    1: "Created",
    2: "Deleted",
    3: "Updated",
    4: "Renamed to something",
    5: "Renamed from something"
}


def watchDir(path):
    PATH_TO_WATCH = path or "."
    print(f"Watching {PATH_TO_WATCH} at {time.asctime()}")
    os.chdir(path)
    files_changed = queue.Queue()

    Watcher(PATH_TO_WATCH, files_changed)

    while 1:
        try:
            file_type, filename, action = files_changed.get_nowait()
            print(file_type, filename, action)
            # if action == "Created":
            #     if file_type == 'file':
            #         ext = f.getFileExt(filename)
            #     print(ext)
            #     if os.path.exists(filename):
            #         folderpath = f.createFolder(os.curdir, ext)
            #         f.copyFile(f.getFileName(filename), folderpath)
            #         f.removeFile(filename)
        except queue.Empty:
            pass
        time.sleep(1)
        # list = f.getFileAndDirPath(path)
        # print(list)
        list = f.getListofFileswPath(path)
        for file in list:
            if os.path.exists(file):
                folderpath = f.createFolder(os.curdir, f.getFileExt(file))
                f.copyFile(f.getFileName(file), folderpath)
                f.removeFile(file)


def watch_path(path_to_watch, include_subdirectories=False):
    FILE_LIST_DIRECTORY = 0x0001
    hDir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    while 1:
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024,
            include_subdirectories,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )
        for action, file in results:
            full_filename = os.path.join(path_to_watch, file)
            if not os.path.exists(full_filename):
                file_type = "<deleted>"
            elif os.path.isdir(full_filename):
                file_type = 'folder'
            else:
                file_type = 'file'

            yield (file_type, full_filename, ACTIONS.get(action, "Unknown"))


class Watcher(threading.Thread):

    def __init__(self, path_to_watch, results_queue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self.path_to_watch = path_to_watch
        self.results_queue = results_queue
        self.start()

    def run(self):
        for result in watch_path(self.path_to_watch):
            self.results_queue.put(result)
