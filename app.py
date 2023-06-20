from flask import Flask, request, render_template, redirect, url_for
import json
import uuid

app = Flask(__name__)

blog_posts = []  # List to store the blog posts


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        """Gets the form data submitted by the user, creates a new blog post dictionary addition, complete with
        generating a new unique id, appends this to the blog_posts list, and updates the storage.json file with
        the new blog post, before finally redirecting the user back to the home page.
        If it's a GET request, the add.html template is displayed with the form"""

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        post_id = str(uuid.uuid4())

        new_post = {
            'id': post_id,
            'title': title,
            'author': author,
            'content': content
        }
        blog_posts.append(new_post)

        with open('storage.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Finds the blog post with the given id and removes it from the list, then redirects back to the home page"""
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    return redirect(url_for('index'))



@app.route('/')
def index():
    """Pass the blog_posts list to the index.html template"""
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    """Loads the current blog posts in the json file from storage.json"""
    with open('storage.json', 'r') as file:
        blog_posts = json.load(file)

    app.run()
