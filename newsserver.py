# Это код каждые 3 секунды отправляет новый POST-запрос на сервер "текстом" новости
import requests
import random
from threading import Timer

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

def sendRequest():
    index = random.randint(0, len(randomlist)-1)
    requests.post('http://localhost:8080/news', data={'text': randomlist[index]})
    return False

randomlist = ['Many interesting things have happened', 'Everything is allright', 'Who watches watchmen?', 'Good news, everyone!', 'We dont talk about Bruno', 'Poor unfortunate souls', 'Im a villain in my own story']

setInterval(3.0, sendRequest)
