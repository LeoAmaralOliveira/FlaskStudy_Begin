from app import db


class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Name {self.name}>'
