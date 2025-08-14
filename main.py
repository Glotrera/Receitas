import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    receitas = db.relationship('Receita', backref='autor', lazy=True)
    categorias = db.relationship('Categoria', backref='autor', lazy=True)
    
class categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    Instruções = db.Column(db.Text, nullable=False)
    Tempo = db.Column(db.String(50), nullable=False)
    
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categorias_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    Data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ingredientes = db.relationship('ingredientes_receita', backref='receita', lazy=True)
    
class ingredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
   
class ingredientes_receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), nullable=False)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    quantidade = db.Column(db.String(50), nullable=False)
    unidade = db.Column(db.String(50), nullable=False)