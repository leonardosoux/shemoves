from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configurações
app.secret_key = '12334'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://leonardo:1234@localhost/shemoves1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Diretório para salvar imagens
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Classe Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relaciona o post a um usuário
    user = db.relationship('User', backref='posts')  # Permite acessar o autor do post

# Classe Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='comments', lazy=True)
    post = db.relationship('Post', backref='comments', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cref = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


# Cria o banco de dados
with app.app_context():
    db.create_all()

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro-escolha")
def cadastro_escolha():
    return render_template("cadastro-escolha.html")

@app.route("/cadastro-profissional", methods=['GET', 'POST'])
def cadastro_profissional():
    if request.method == 'POST':
        # Coletar dados do formulário
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        cpf = request.form.get('cpf')
        cref = request.form.get('cref')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Verificar se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('cadastro-profissional.html')

        # Validar se já existe o CPF ou e-mail no banco
        if User.query.filter_by(cpf=cpf).first() or User.query.filter_by(email=email).first():
            flash('CPF ou e-mail já cadastrado.', 'error')
            return render_template('cadastro-profissional.html')

        # Hash da senha
        password_hash = generate_password_hash(password)

        # Criar e salvar o usuário no banco de dados
        professional = Professional(
            name=name,
            birthdate=birthdate,
            cpf=cpf,
            cref=cref,
            email=email,
            phone=phone,
            password_hash=password_hash
        )
        try:
            db.session.add(professional)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for("login"))
        except Exception as e:
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            return render_template("cadastro-profissional.html")

    return render_template("cadastro-profissional.html")

@app.route("/cadastro-cliente", methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        # Coletar dados do formulário
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Verificar se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('cadastro-cliente.html')

        # Validar se já existe o CPF ou e-mail no banco
        if User.query.filter_by(cpf=cpf).first() or User.query.filter_by(email=email).first():
            flash('CPF ou e-mail já cadastrado.', 'error')
            return render_template('cadastro-cliente.html')

        # Hash da senha
        password_hash = generate_password_hash(password)

        # Criar e salvar o usuário no banco de dados
        user = User(
            name=name,
            birthdate=birthdate,
            cpf=cpf,
            email=email,
            phone=phone,
            password_hash=password_hash
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for("login"))
        except Exception as e:
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            return render_template("cadastro-cliente.html")

    return render_template("cadastro-cliente.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Buscar o usuário no banco de dados
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id 
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/home")
def home():
    posts = Post.query.order_by(Post.id.desc()).all()  # Posts mais recentes primeiro
    user_id = session.get('user_id')  # Recupera o ID do usuário da sessão
    if not user_id:
        flash('Faça login para acessar esta página.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('login'))
    
    return render_template('home.html', posts=posts, user=user)

@app.route("/create", methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        flash('Faça login para criar uma publicação.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
     content = request.form.get('content')
     image = request.files.get('image')
     image_path = None

     if image and allowed_file(image.filename):
         filename = secure_filename(image.filename)
         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Cria o diretório, se necessário
         image.save(image_path)

     user_id = session['user_id']
     post = Post(content=content, image=image_path, user_id=user_id)
     db.session.add(post)
     db.session.commit()
     return redirect(url_for('home'))
    
    return render_template("criar.html")

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
       post.likes += 1
       db.session.commit()
       return jsonify({'likes': post.likes})
    
    return jsonify({'error': 'Post not found'}), 404


@app.route('/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    content = request.form.get('content')
    if not content:
        return jsonify({'error': 'Conteúdo do comentário vazio.'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado.'}), 404

    user = User.query.get(session.get('user_id'))
    if not user:
        return jsonify({'error': 'Usuário não autenticado.'}), 403

    comment = Comment(content=content, post_id=post_id, user_id=user.id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'comment': {'user': user.name, 'content': content}})


if __name__ == '__main__':
    app.run(debug=True)









