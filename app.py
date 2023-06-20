from flask import Flask, request, render_template, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Gets the form data submitted by the user, creates a new blog post dictionary addition, complete with
            generating a new unique id, appends this to the blog_posts list, and updates the storage.json file with
            the new blog post, before finally redirecting the user back to the home page.
            If it's a GET request, the add.html template is displayed with the form"""

    if request.method == 'POST':
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
        blog_posts = load_blog_posts()
        blog_posts.append(new_post)

        with open('storage.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<string:post_id>', methods=['POST'])
def delete(post_id):
    """Finds the blog post with the given id and removes it from the list, then redirects back to the home page"""

    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    with open('storage.json', 'w') as fileobj:
        json.dump(blog_posts, fileobj, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Fetches the blog posts from the JSON file, locates the post for the given post_id, will update the post in the
    JSON file, and saves the updated blog post list back in the JSON file, then redirects back to the index page.
    Else it's a GET request, so displays the updated html"""

    blog_posts = load_blog_posts()
    post = None
    for blog_post in blog_posts:
        if blog_post['id'] == post_id:
            post = blog_post
            break
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        with open('storage.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

        # Redirect back to the index page
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/')
def index():
    """Pass the blog_posts list to the index.html template"""
    stored_blog_posts = load_blog_posts()
    return render_template('index.html', posts=stored_blog_posts)


def load_blog_posts():
    """Loads the current blog posts from the JSON file"""
    with open('storage.json', 'r') as file:
        stored_blog_posts = json.load(file)
        return stored_blog_posts


if __name__ == '__main__':
    app.run()
