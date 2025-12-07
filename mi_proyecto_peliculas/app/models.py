from mongoengine import Document, StringField, IntField, FloatField, ReferenceField
from werkzeug.security import generate_password_hash, check_password_hash 

# === MODELO DE USUARIO ===
class User(Document):
    email = StringField(required=True, unique=True) 
    password_hash = StringField(required=True)
    role = StringField(default='cliente')
    meta = {'collection': 'users'}
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# === MODELO DE PELÍCULAS ===
class Movie(Document):
    title = StringField(required=True)
    genre = StringField()
    year = IntField()
    director = StringField()
    rating = FloatField()
    created_by = ReferenceField(User) 
    meta = {'collection': 'movies'}