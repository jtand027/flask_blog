import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

# a secret key is required to use flash() messages (stored in the session cookie)
# for a real deployment, set this from an environment variable instead
app.config["SECRET_KEY"] = "dev-secret-key-change-me"



# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn


# Function to retrieve a single post from the database by its id
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    # if no post exists with that id, respond with a 404 Not Found page
    if post is None:
        abort(404)

    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # get a connection to the database
    conn = get_db_connection()

    # execute a query to read all posts from the posts table in the database
    posts = conn.execute('SELECT * FROM posts').fetchall()

    # close the connection
    conn.close()

    # send the posts to the index.html template to be displayed
    return render_template('index.html', posts=posts)


# route to view a single post
@app.route('/<int:post_id>/')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    # determine if the page is being requested with a POST or GET request
    if request.method == 'POST':
        # get the title and content that was submitted
        title = request.form['title']
        content = request.form['content']

        # display an error if title or content is not submitted
        # else make a database connection and insert the blog post content
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            # insert data into the database
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            flash('Post created successfully!')
            # redirect to the index page
            return redirect(url_for('index'))

    return render_template('create.html')


# route to edit a post
@app.route('/<int:post_id>/edit/', methods=('GET', 'POST'))
def edit(post_id):
    # get the existing post (404 if it does not exist)
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            # update the post with the new title and content
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            flash('Post updated successfully!')
            # redirect to the home page
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# route to delete a post (only accepts POST requests so a post can't be deleted by just visiting a URL)
@app.route('/<int:post_id>/delete/', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()