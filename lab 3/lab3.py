import sqlite3

import requests


def create_db():
    con = sqlite3.connect("lab3.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE posts(user_id INT, id INT, title VARCHAR, body VARCHAR)")
    con.close()

def get_request():
    request = requests.get("https://jsonplaceholder.typicode.com/posts")
    return request.json()

def insert_data(data):
    con = sqlite3.connect("lab3.db")
    cur = con.cursor()

    cur.execute("INSERT INTO posts (user_id, id, title, body) VALUES (?,?,?,?)",
                (data['userId'], data['id'], data['title'], data['body']),)

    con.commit()
    con.close()

def get_post(id):
    con = sqlite3.connect("lab3.db")
    cur = con.cursor()

    posts = cur.execute("SELECT * FROM posts WHERE user_id = ?", (id,),).fetchall()

    print(posts)

    con.close()

def main():
    create_db()
    data = get_request()
    for i in data:
        insert_data(i)
    get_post(2)

main()