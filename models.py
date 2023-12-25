from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users' # specify table name

    # Define table columns
    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text())


    def __repr__(self):
        return f"<User {self.username}>"


    # take a plain-text password and hash it
    def set_password(self, password):
        self.password = generate_password_hash(password)


    # takes a plain-text password hashes it and checks if it matches the stored hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)


    # Retrieve user by name
    # Returns either the first user with the specified username or or None if user with that username is not found
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()







"""
1. Import db object an instance of SQLAlchemy. The object is used to interact with database and 
define database model.
2. import uuid4 function from uuid module. Used to generate random uuid
3. Define a user class that inherits from db.Model. This indicates that User is a SQLAlchemy model
representing a database table
4. Specfy table name
5. Define table columns
__repr__: used to define a string representation of an object. Use for debugging purposes
6. Overrride the __repr__.

"""