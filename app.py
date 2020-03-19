from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)


@app.route('/', methods=['GET'])
def index():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('index.html', posts=all_posts)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/allposts')
    else:
        return render_template('posts.html')


@app.route('/allposts', methods=['GET'])
def allposts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('allposts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/allposts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/allposts')
    else:
        return render_template('edit.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
