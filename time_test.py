from threading import Timer
from bs4 import BeautifulSoup
import requests

def printHello():
    print('----------------------------------------')
    print('hello world')
    t = Timer(2, printHello)
    t.start()


if __name__ == "__main__":
    printHello()
