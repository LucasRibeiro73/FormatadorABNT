import os
import stripe
from flask import Flask, request, render_template, send_file, redirect, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from formatador_abnt import formatador_abnt_profissional
from models import db, User

PACOTES_DE_CREDITOS = {
    5: {"nome": "Pacote Básico", "preco_centavos": 990, "creditos": 5},
    15: {"nome": "Pacote TCC", "preco_centavos": 2490, "creditos": 15},
    25: {"nome": "Pacote Pós-Graduação", "preco_centavos": 3490, "creditos": 25}
}

# --- CONFIGURAÇÃO INICIAL ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- CONFIGURAÇÃO DO STRIPE ---
stripe.api_key = 'chave-secreta' 
endpoint_secret = 'whsec_chave-secreta'

# Inicializa as extensões
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROTAS DE AUTENTICAÇÃO ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos. Tente novamente.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado. Tente fazer o login.', 'warning')
            return redirect(url_for('login'))
            
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_email=current_user.email, credits=current_user.credits)

@app.route('/pagamento-sucesso')
@login_required
def pagamento_sucesso():
    flash("Pagamento recebido! Seus créditos já estão disponíveis.", "success")
    return render_template('pagamento_sucesso.html')

@app.route('/download/template')
@login_required
def download_template():
    try:
        return send_from_directory('static/resources', 'Trabalho_ABNT_Template.docx', as_attachment=True)
    except FileNotFoundError:
        flash("O arquivo de template não foi encontrado no servidor. Por favor, avise o suporte.", "danger")
        return redirect(url_for('dashboard'))
    
# --- ROTA DE FORMATAÇÃO COM CONTROLE DE CRÉDITOS ---
@app.route('/formatar', methods=['POST'])
@login_required
def formatar_arquivo():
    if current_user.credits <= 0:
        flash("Você não tem créditos suficientes. Por favor, compre um pacote.", "warning")
        return redirect(url_for('dashboard'))
    
    arquivo = request.files.get('arquivo_usuario')
    if not arquivo or arquivo.filename == '':
        flash('Por favor, selecione um arquivo.', 'danger')
        return redirect(url_for('dashboard'))
        
    caminho_entrada = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
    arquivo.save(caminho_entrada)
    formatador_abnt_profissional(caminho_entrada)
    nome_arquivo_saida = arquivo.filename.replace('.docx', '_FORMATADO_PROFISSIONAL.docx')

    current_user.credits -= 1
    db.session.commit()

    from markupsafe import Markup
    link_download = url_for('download_arquivo', filename=nome_arquivo_saida)
    mensagem_sucesso = Markup(f"Sucesso! Seu arquivo foi formatado. <a class='download-link-button' href='{link_download}'>Clique aqui para baixar.</a>")
    
    flash(mensagem_sucesso, "success")
    
    return redirect(url_for('dashboard'))

@app.route('/download-file/<filename>')
@login_required
def download_arquivo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# --- ROTAS DE PAGAMENTO ---
@app.route('/criar-sessao-checkout/<int:pacote>', methods=['POST'])
@login_required
def criar_sessao_checkout(pacote):

    if pacote not in PACOTES_DE_CREDITOS:
        flash("Pacote inválido selecionado.", "danger")
        return redirect(url_for('dashboard'))

    pacote_info = PACOTES_DE_CREDITOS[pacote]

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'boleto'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {'name': pacote_info['nome']},
                    'unit_amount': pacote_info['preco_centavos'],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('pagamento_sucesso', _external=True),
            cancel_url=url_for('dashboard', _external=True),
            # CRUCIAL: Passamos a quantidade de créditos para o webhook
            metadata={
                'user_id': current_user.id,
                'creditos_comprados': pacote_info['creditos']
            }
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError: return 'Payload inválido', 400
    except stripe.error.SignatureVerificationError: return 'Assinatura inválida', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        user_id = session['metadata']['user_id']
        creditos_comprados = session['metadata']['creditos_comprados']
        
        user = User.query.get(user_id)
        if user:
            user.credits += int(creditos_comprados)
            db.session.commit()
            print(f"Usuário {user.email} comprou {creditos_comprados} créditos.")

    return 'OK', 200

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)