from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('storage.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        print(f"New Blog Post: Title - {title}, Author - {author}, Content - {content}")
        return "Blog post added successfully!"

    return render_template('add.html')


if __name__ == '__main__':
    app.run()