import json
from json.decoder import JSONDecodeError

from flask import Flask, render_template, request, redirect, url_for


def load_data():
    """This functions reads the file data.json and returns its data as a string"""

    try:
        with open("data.json", "r", encoding="utf-8") as reader:
            data = json.load(reader)
            return data

    # Returning empty list in case of errors to prevent the route functions from crashing
    except FileNotFoundError:
        print("data.son file not found")
        return []
    except JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return []



def write_data():
    """This functions writes new data on the file data.json"""

    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')

    if not author or not title or not content:
        return False  # Signal missing data

    # Load existing posts
    with open('data.json', 'r') as reader:
        posts = json.load(reader)

    # Generate a new ID automatically
    new_post = {
        # iterating through all the posts, selecting the largest ID and adding 1 to it to assign to the new post.
        "id": max(post['id'] for post in posts) + 1 if posts else 1,
        "author": author,
        "title": title,
        "content": content
    }
    posts.append(new_post)

    # Save to file
    with open('data.json', 'w') as writer:
        json.dump(posts, writer,indent=4, sort_keys=True)
    return True

app = Flask(__name__)

@app.route('/')
def index():
    blog_posts = load_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """This method and route adds a new blog post"""
    if request.method == 'POST':
        # Try writing the data
        if not write_data():
            return "All fields are required!", 400  # Show an error if fields are missing
        return redirect(url_for('index'))  # Redirect only on success
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """This method and route deletes a blog post"""
    # Load existing posts
    posts = load_data()

    # Filter out the post to delete
    posts = [post for post in posts if post["id"] != post_id]

    # Save updated posts back to the file
    with open('data.json', 'w') as writer:
        json.dump(posts, writer, indent=4, sort_keys=True)

    # Redirect to home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """This method and route updates a blog post"""

    # Load existing posts
    posts = load_data()

    # Filter out the post to update
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated data from form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        if not author or not title or not content:
            return "All fields are required!", 400

        # Update fields
        post['author'] = author
        post['title'] = title
        post['content'] = content

        # Save changes to file
        with open('data.json', 'w') as writer:
            json.dump(posts, writer, indent=4, sort_keys=True)

        return redirect(url_for('index'))

    # For GET request, display the update form
    return render_template('update.html', post=post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)