from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarys-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Title: {self.title}'


db.create_all()


@app.route('/')
def index():
    all_books = Books.query.all()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        new_book = Books(
            title=request.form['book_name'],
            author=request.form['author'],
            rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:book_id>', methods=["GET", "POST"])
def edit(book_id):
    book_edit = Books.query.get(book_id)
    if request.method == 'POST':
        book_edit.rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', book_edit=book_edit)


@app.route('/delete/<int:book_id>')
def delete(book_id):
    delete_book = Books.query.get(book_id)
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
