import uuid
from flask import Flask, render_template, redirect, request, url_for, jsonify
import requests
import json

app = Flask(__name__)


def generate_unique_id():
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Find the maximum post ID in the existing data
    max_id = max([post['id'] for post in data], default=0)

    # Increment the maximum ID by 1 to generate a unique ID
    new_id = max_id + 1

    return new_id


@app.route('/')
def index():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return render_template('index.html', posts=data)


# @app.route("/search")
# def search_books():
#     search_query = request.args.get("q")  # Get the search query from the request parameters
#
#     # Make the API request
#     response = requests.get(f"https://openlibrary.org/search.json?q={search_query}")
#
#     data = response.json()
#
#     # Extract the necessary book information from the response
#     books = []
#     for book in data.get("docs", []):
#         book_data = {
#             "cover": f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg",
#             "title": book.get("title", ""),
#             "author": book.get("author_name", ["Unknown"]),
#             "publication_date": book.get("first_publish_year", "N/A"),
#         }
#         books.append(book_data)
#
#     # Return the book data as JSON response
#     return jsonify(books)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Create a new blog post object
        new_post = {
            'id': generate_unique_id(),
            'title': title,
            'content': content,
            'likes': 0  # Initialize likes to 0
        }

        # Read the existing data from data.json
        with open('data.json', 'r') as file:
            data = json.load(file)

        # Append the new post to the existing data
        data.append(new_post)

        # Write the updated data back to data.json
        with open('data.json', 'w') as file:
            json.dump(data, file)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Read the existing data from data.json
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Find the index of the post with the given post_id
    index = None
    for i, post in enumerate(data):
        if post['id'] == post_id:
            index = i
            break

    # If the post is found, update it with new values
    if index is not None:
        if request.method == 'POST':
            new_value = request.form.get('new_value')
            data[index]['content'] = new_value

            # Write the updated data back to data.json
            with open('data.json', 'w') as file:
                json.dump(data, file)

            # Redirect to the index route after updating the post
            return redirect(url_for('index'))

        return render_template('update.html', post=data[index])

    # If the post is not found, return a 404 error
    return render_template('404.html'), 404


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    # Read the existing data from data.json
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Find the index of the post with the given post_id
    index = None
    for i, post in enumerate(data):
        if post['id'] == post_id:
            index = i
            break

    # If the post is found, delete it
    if index is not None:
        del data[index]  # Delete the post from the data list

        # Write the updated data back to data.json
        with open('data.json', 'w') as file:
            json.dump(data, file)

        # Redirect to the index route after deleting the post
        return redirect(url_for('index'))

    # If the post is not found, return a 404 error
    return render_template('404.html'), 404


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    # Read the existing data from data.json
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Find the post with the given post_id
    for post in data:
        if post['id'] == post_id:
            post['likes'] += 1  # Increment the likes count
            break

    # Write the updated data back to data.json
    with open('data.json', 'w') as file:
        json.dump(data, file)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('400.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
