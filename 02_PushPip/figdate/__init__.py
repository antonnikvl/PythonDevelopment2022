import locale
import sys

from pyfiglet import Figlet
import time

def date(format="%Y %d %b, %A", font="graceful"):
    f = Figlet(font=font)
    return f.renderText(time.strftime(format))

def main():
    locale.setlocale(locale.LC_ALL, 'RU_ru')
    if len(sys.argv) > 2:
        print(date(sys.argv[1], sys.argv[2]))
    elif len(sys.argv) > 1:
        print(date(sys.argv[1]))
    else:
        print(date())