from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acessos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para armazenar o número de acessos
class Acesso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contador = db.Column(db.Integer, default=0)

# Rota principal
@app.route('/')
def index():
    # Verifica se já existe um registro no banco de dados
    acesso = Acesso.query.first()
    if not acesso:
        # Se não existir, cria um registro com contador = 1
        acesso = Acesso(contador=1)
        db.session.add(acesso)
    else:
        # Se já existir, incrementa o contador
        acesso.contador += 1
    db.session.commit()
    return render_template('index.html', contador=acesso.contador)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)