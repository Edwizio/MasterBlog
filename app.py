import json
from flask import Flask, render_template, request

def load_data():
    """
    This functions takes a json file as parameter and returns its data as a string
    :return data:
    """
    with open("data.json", "r") as reader:
        data = json.loads(reader.read())

    return data

blog_posts = load_data()

app = Flask(__name__)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')



@app.route('/')
def index():

    blog_posts = load_data()

    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)