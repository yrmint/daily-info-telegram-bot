import requests
from bs4 import BeautifulSoup
import random

jokes = []
url = 'https://www.trees-and-lambdas.info/matushansky/stirlitz.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
elements = soup.find_all('p')
elements.pop(0)
elements.pop(44)
c = 233
for element in elements:
    f = open(f"app/jokes\{c}.txt", "w")
    f.write(element.text)
    f.close()
    c += 1

# c = 0

# for i in range(0, 5):
#     url = f"https://www.anekdot.ru/tags/%D0%A8%D1%82%D0%B8%D1%80%D0%BB%D0%B8%D1%86/{i}" if i != 0 else \
#         f"https://www.anekdot.ru/tags/%D0%A8%D1%82%D0%B8%D1%80%D0%BB%D0%B8%D1%86"
#     response = requests.get(url)
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#     elements = soup.find_all('div', class_='text')
#
#     for element in elements:
#         f = open(f"jokes\{c}.txt", "w")
#         f.write(element.text)
#         f.close()
#         jokes.append(element.text)
#         c += 1
#
# print(c, " jokes written.")


def get_joke() -> str:
    return jokes[random.randint(0, len(jokes) + 1)].text
