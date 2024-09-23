import requests

def first_task(URL):
  r = requests.get(URL)
  j = r.json()
  for i in j:
    if (i['userId'] % 2 == 0):
      print(i)

def second_task(URL):
  r = requests.post(URL, json = {'title': 'Тестовый пост', 'body': 'Это тестовый пост для задания по скриптовым языкам программирования'})
  j = r.json()
  print(j)

def third_task(URL, num):
  r = requests.put(URL + '/'+ num, json = {'title': 'Обновлённый пост', 'body': 'Это обновлённый тестовый пост для задания по скриптовым языкам программирования'})
  j = r.json()
  print(j)

def main():
  URL = 'https://jsonplaceholder.typicode.com/posts'
  print('First Task:')
  first_task(URL)
  print('\n\nSecond Task:')
  second_task(URL)
  print('\n\nThird Task:')
  third_task(URL, '99')

main()