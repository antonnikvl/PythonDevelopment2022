from textdistance import hamming, bag
from random import randint
import urllib.request
import sys

def bullscows(guess: str, secret: str):
    b = hamming.similarity(guess, secret)
    c = bag.similarity(guess, secret)
    return (b, c - b)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = words[randint(0, len(words) - 1)]
    finished = False
    tries = 0
    while not finished:
        guess = ask("Введите слово: ", words)
        tries += 1
        (b, c) = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(secret):
            return tries

def main():
    def ask(prompt: str, valid: list[str] = None):
        print(prompt)
        w = input()
        while (valid is not None) and (not (w in valid)):
            print(prompt)
            w = input()
        return w

    def inform(format_string: str, bulls: int, cows: int):
        print(format_string.format(bulls, cows))
   
    try:
      f = open(sys.argv[1], "r", encoding='utf8')
      data = [l.replace("\n", "") for l in f.readlines()]
    except IOError:
        f = urllib.request.urlopen(sys.argv[1])
        data = [l.decode("utf-8").replace("\n", "") for l in f]

    l = 5
    if len(sys.argv) > 2:
        l = int(sys.argv[2])
    data = [x for x in data if len(x) == l]
    
    print("Число попыток:", gameplay(ask, inform, data))