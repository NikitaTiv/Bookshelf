from webapp.db import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, index=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    author = db.Column(db.String, index=True, nullable=False)
    discription = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'<Book {self.name} загружена пользователем {self.user}>'