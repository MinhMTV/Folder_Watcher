import FileLib as f
import Handler as h
import time
import os


def takePath():
    while True:
        answer = input(
            "You want to enter specific path to watch all files?\nY/N\n")
        if answer.lower() == 'y':
            time.sleep(1)
            path = input("Enter specific path now\n")
            filepath = path.replace('"', "")
            if os.path.exists(filepath):
                print("Path exist")
                path = filepath
                return path
            else:
                print("Invalid Path. Please try again\n")

        elif answer.lower() == 'n':
            print("Path will be the same directory than the Script File")
            path = os.path.dirname(os.path.realpath(__file__))
            print(path)
            return path
        else:
            print("Invalid Input. Please Enter Y / N\n")


def main():
    path = takePath()
    h.watchDir(path)


if __name__ == '__main__':
    main()
