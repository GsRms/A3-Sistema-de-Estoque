from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'hjsewffdbasbdasewrewdsadkjlaskldsajkodnasjkdjk'
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'estoque'
}

# Configuração do banco de dados
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        database='estoque',
        user='root',
        password=''
    )

def generate_password_hash(password):
    return generate_password_hash(password)

def check_password_hash(hashed_password, password):
    return check_password_hash(hashed_password, password)

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Você precisa estar logado para acessar esta página.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def registrar_log(entidade, entidade_id, acao, descricao=""):
    """
    Registra logs de ações no sistema.

    :param entidade: Nome da entidade (ex: 'produto', 'categoria')
    :param entidade_id: ID da entidade associada ao log
    :param acao: Tipo da ação ('criação', 'edição', 'removido', 'entrada', 'saída')
    :param descricao: Mensagem descritiva opcional
    """
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO logs_estoque (entidade, entidade_id, acao, descricao) VALUES (%s, %s, %s, %s)",
            (entidade, entidade_id, acao, descricao)
        )
        connection.commit()
    except Exception as e:
        print(f"Erro ao registrar log: {e}")
    finally:
        cursor.close()
        connection.close()

@app.route('/logs')
def logs():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                id, 
                entidade, 
                entidade_id, 
                acao, 
                descricao, 
                data_hora 
            FROM logs_estoque
            ORDER BY data_hora DESC
        """)
        logs = cursor.fetchall()  # Retorna uma lista de tuplas
        print(f"Logs encontrados: {len(logs)}")  # Verifique o número de logs encontrados
    finally:
        cursor.close()
        connection.close()

    # Verifique se logs está vazio
    if not logs:
        print("Nenhum log encontrado.")
    
    # Organizar logs por tipo de ação
    logs_categorized = {
        'entrada': [log for log in logs if log[3] == 'entrada'],
        'saida': [log for log in logs if log[3] == 'saída'],
        'edicao': [log for log in logs if log[3] == 'edição'],
        'criacao': [log for log in logs if log[3] == 'criação'],
        'remocao': [log for log in logs if log[3] == 'remoção']
    }

    # Verifique os logs categorizados
    print("Logs categorizados:", logs_categorized)

    return render_template('logs.html', title="Histórico de Logs", logs=logs_categorized)


@app.route('/cadastro', methods=['GET'])
def cadastrar_usuario():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario_post():
    email = request.form.get('email')
    senha = request.form.get('password')

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Verifica se o email já está em uso
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email já está em uso. Tente outro.", "danger")
        else:
            # Insere o usuário na tabela sem hashing de senha
            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
                (email, senha)
            )
            connection.commit()
            flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('cadastrar_usuario'))
    except Exception as e:

        flash(f"Erro ao cadastrar usuário: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']
           #     session['user_name'] = user['nome']
                flash("Login realizado com sucesso!", "success")
                return render_template('index.html')
            else:
                flash("Credenciais inválidas. Tente novamente.", "danger")
        except Exception as e:
            flash(f"Erro ao processar login: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
    return render_template('login.html')

# Página de logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Você foi desconectado.", "info")
    return redirect(url_for('login'))

# Página inicial (exemplo de rota protegida)
@app.route('/')
@login_required
def home():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Busca os 10 logs mais recentes
        cursor.execute("SELECT entidade, entidade_id, acao, descricao, data_hora FROM logs_estoque ORDER BY data_hora DESC LIMIT 10")
        logs = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    # Renderiza a página inicial com os logs
    return render_template('index.html', title="Página Principal", logs=logs)
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        categoria_id = request.form['categoria_id']  
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, descricao, preco, quantidade, categoria_id) VALUES (%s, %s, %s, %s, %s)",
                (nome, descricao, preco, quantidade, categoria_id)
            )
            connection.commit()
            registrar_log(
                entidade='produto',
                entidade_id=cursor.lastrowid,  # ID do produto recém-criado
                acao='criação',
                descricao=f"Produto '{nome}' cadastrado com {quantidade} unidades e preço {preco}."
            )
            flash("Produto cadastrado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return render_template('sucesso_cadastro_produto.html')
    else:
        categorias = get_all_categorias()  
        return render_template('cadastrar_produto.html', categorias=categorias)




@app.route('/cadastrar_produto/sucesso', methods=['POST'])
@login_required
def sucesso_cadastro_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    quantidade = int(request.form['quantidade'])
    categoria_id = 1 
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, quantidade, categoria_id) VALUES (%s, %s, %s, %s, %s)",
            (nome, descricao, preco, quantidade, categoria_id)
        )
        connection.commit()
        flash("Produto cadastrado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro: {e}", "danger")
    finally:
        cursor.close()
        connection.close()
    return render_template('sucesso_cadastro_produto.html')

@app.route('/entradas')
@login_required
def entradas():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Filtrar logs de entradas
        cursor.execute("""
            SELECT 
                id, 
                descricao, 
                data_hora 
            FROM logs_estoque 
            WHERE acao = 'entrada'
            ORDER BY data_hora DESC
        """)
        entradas = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    # Renderiza o template de entradas com os dados
    return render_template('entradas.html', title="Entradas de Produtos", logs=entradas)

@app.route('/saidas')
@login_required
def saidas():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Filtrar logs de saídas
        cursor.execute("""
            SELECT 
                id, 
                descricao, 
                data_hora 
            FROM logs_estoque 
            WHERE acao = 'saída' 
            ORDER BY data_hora DESC
        """)
        saidas = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    # Renderiza o template de saídas com os dados
    return render_template('saidas.html', title="Saídas de Produtos", logs=saidas)



@app.route('/buscar_produtos', methods=['GET'])
@login_required
def buscar_produtos():
    query = request.args.get('query', '')
    produtos = buscar_produtos(query)
    return render_template('buscar_produtos.html', resultado=produtos, query=query)


def buscar_produtos(query):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = "%" + query.lower() + "%"
        cursor.execute("SELECT p.id, p.nome, p.descricao, p.preco, p.quantidade, c.id AS categoria_id, c.nome AS categoria_nome FROM produtos p JOIN categorias c ON p.categoria_id = c.id WHERE LOWER(p.nome) LIKE %s", (query,))
        produtos = cursor.fetchall()
        for produto in produtos:
            produto['preco_total'] = produto['preco'] * produto['quantidade']
        return produtos
    
    except Exception as e:
        app.logger.error(f"Erro ao buscar produtos: {e}")
        raise
    
    finally:
        cursor.close()
        connection.close()

def get_all_produtos(query=None):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if query:
            cursor.execute("SELECT p.id AS id, p.nome AS nome, p.descricao AS descricao, p.preco AS preco, p.quantidade AS quantidade, c.id AS categoria_id, c.nome AS categoria_nome FROM produtos p LEFT JOIN categorias c ON p.categoria_id = c.id WHERE p.nome LIKE %s", ('%' + query + '%',))
        else:
            cursor.execute("SELECT p.id AS id, p.nome AS nome, p.descricao AS descricao, p.preco AS preco, p.quantidade AS quantidade, c.id AS categoria_id, c.nome AS categoria_nome FROM produtos p LEFT JOIN categorias c ON p.categoria_id = c.id")
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        connection.close()

def get_all_categorias():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM categorias")
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        connection.close()

def update_quantidade(produto_id, quantidade):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s", (quantidade, produto_id))
        connection.commit()
        registrar_log(
            entidade='produto',
            entidade_id=produto_id,
            acao='entrada' if quantidade > 0 else 'saída',
            descricao=f"Alteração de quantidade: {quantidade} unidades."
        )
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        connection.close()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/cadastrar_categoria', methods=['GET', 'POST'])
@login_required
def cadastrar_categoria():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        if not nome:
            flash("O campo de nome é obrigatório!", "danger")
        else:
            query = "SELECT COUNT(*) FROM categorias WHERE nome = %s"
            cursor.execute(query, (nome,))
            result = cursor.fetchone()
            if result['COUNT(*)'] > 0:
                flash("A categoria já foi criada!", "danger")
            else:
                try:
                    query = "INSERT INTO categorias (nome, descricao) VALUES (%s, %s)"
                    cursor.execute(query, (nome, descricao))
                    conn.commit()
                    registrar_log(
                        entidade='categoria',
                        entidade_id=cursor.lastrowid,
                        acao='criação',
                        descricao=f"Categoria '{nome}' criada com descrição: {descricao}."
                    )
                    flash("Categoria cadastrada com sucesso!", "success")
                except Exception as e:
                    flash(f"Erro ao cadastrar a categoria: {e}", "danger")

    query = "SELECT * FROM categorias"
    cursor.execute(query)
    categorias = cursor.fetchall()

    conn.close() 
    return render_template('cadastrar_categoria.html', categorias=categorias)



@app.route('/remover_categoria/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def remover_categoria(categoria_id):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "UPDATE produtos SET categoria_id=NULL WHERE categoria_id=%s"
        cursor.execute(query, (categoria_id,))
        
        query = "DELETE FROM categorias WHERE id=%s"
        cursor.execute(query, (categoria_id,))
        
        conn.commit()
        registrar_log(
            entidade='categoria',
            entidade_id=categoria_id,
            acao='removido',
            descricao=f"Categoria ID={categoria_id} foi removida e desassociada dos produtos."
        )
        flash("Categoria desassociada com sucesso!", "success")
        conn.close()

        return redirect(url_for('cadastrar_categoria'))


@app.route('/editar_categoria/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(categoria_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        if not nome:
            flash("O campo de nome é obrigatório!", "danger")
            return redirect(url_for('editar_categoria', categoria_id=categoria_id))

        query = "SELECT COUNT(*) FROM categorias WHERE nome = %s AND id != %s"
        cursor.execute(query, (nome, categoria_id))
        result = cursor.fetchone()

        if result['COUNT(*)'] > 0:
            flash("A categoria já foi criada!", "danger")
        else:
            try:
                query = "UPDATE categorias SET nome=%s, descricao=%s WHERE id=%s"
                cursor.execute(query, (nome, descricao, categoria_id))
                conn.commit()
                flash("Categoria editada com sucesso!", "success")
                registrar_log(
                    entidade='categoria',
                    entidade_id=categoria_id,
                    acao='edição',
                    descricao=f"Categoria ID={categoria_id} editada. Novo Nome='{nome}', Descrição='{descricao}'."
                )
            except Exception as e:
                flash(f"Erro ao editar a categoria: {e}", "danger")

        conn.close() 
        return redirect(url_for('cadastrar_categoria'))

    query = "SELECT * FROM categorias WHERE id=%s"
    cursor.execute(query, (categoria_id,))
    categoria = cursor.fetchone()

    conn.close()
    return render_template('editar_categoria.html', categoria=categoria)

@app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        quantidade = int(request.form.get('quantidade'))
        categoria_id = int(request.form.get('categoria_id'))

        query = "UPDATE produtos SET nome=%s, descricao=%s, preco=%s, quantidade=%s, categoria_id=%s WHERE id=%s"
        cursor.execute(query, (nome, descricao, preco, quantidade, categoria_id, produto_id))
        connection.commit()
        registrar_log(
            entidade='produto',
            entidade_id=produto_id,
            acao='edição',
            descricao=f"Produto '{nome}' foi atualizado: Preço={preco}, Quantidade={quantidade}."
        )

        flash("Produto editado com sucesso!", "success")
        cursor.close()
        connection.close()

        return redirect(url_for('cadastrar_produto'))

    query = "SELECT * FROM produtos WHERE id=%s"
    cursor.execute(query, (produto_id,))
    produto = cursor.fetchone()

    categorias_query = "SELECT * FROM categorias"
    cursor.execute(categorias_query)
    categorias = cursor.fetchall()

    cursor.close()
    connection.close()

    if produto:
        return render_template('editar_produto.html', produto=produto, categorias=categorias)  # Passando categorias para a página
    else:
        flash("Produto não encontrado!", "danger")
        return redirect(url_for('cadastrar_produto'))


@app.route('/remover_produto/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def remover_produto(produto_id):
    if request.method == 'POST':
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            connection.commit()
            flash("Produto removido com sucesso!", "success")
            registrar_log(
                entidade='produto',
                entidade_id=produto_id,
                acao='removido',
                descricao=f"Produto ID={produto_id} foi removido."
            )

        except Exception as e:
            flash(f"Erro: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('buscar_produtos'))

    return render_template('remover_produto.html', produto_id=produto_id)



@app.route('/detalhes_produto/<int:produto_id>')
@login_required
def detalhes_produto(produto_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM produtos WHERE id = %s"
    cursor.execute(query, (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()

    if produto:
        return render_template('detalhes_produto.html', produto=produto)
    else:
        return redirect(url_for('buscar_produtos'))
@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/categoria/<int:categoria_id>', methods=['GET'])
def categoria(categoria_id):
    try:
        categoria = get_categoria(categoria_id)
        
        if not categoria:
            app.logger.error(f"Categoria com ID {categoria_id} não encontrada.")
            flash("Categoria não encontrada!", "danger")
            return redirect(url_for('cadastrar_categoria'))
        
        if 'produtos' not in categoria or not categoria['produtos']:
            categoria['produtos'] = []
        
        app.logger.info(f"Categoria encontrada com ID {categoria_id}: {categoria}")
        return render_template('categoria.html', categoria=categoria)
    
    except Exception as e:
        app.logger.error(f"Erro ao buscar categoria: {e}")
        flash("Ocorreu um erro ao buscar a categoria.", "danger")
        return redirect(url_for('cadastrar_categoria'))

def get_categoria(categoria_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM categorias WHERE id = %s", (categoria_id,))
        categoria = cursor.fetchone()

        if not categoria:
            app.logger.error(f"Categoria com ID {categoria_id} não encontrada no banco de dados.")
            return None

        cursor.execute("SELECT p.id AS produto_id, p.nome AS nome, p.descricao AS descricao, p.preco AS preco, p.quantidade AS quantidade FROM produtos p WHERE p.categoria_id = %s", (categoria_id,))
        produtos = cursor.fetchall()

        for produto in produtos:
            if not all(key in produto for key in ['produto_id', 'nome', 'descricao', 'preco', 'quantidade']):
                app.logger.error(f"Produto mal formatado: {produto}")
                raise ValueError("Formato de produto inválido")

        categoria['produtos'] = produtos

        return categoria
    
    except Exception as e:
        app.logger.error(f"Erro ao buscar categoria: {e}")
        raise
    
    finally:
        cursor.close()
        connection.close()

@app.route('/categoria/listar', methods=['GET'])
@login_required
def listar_categorias():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM categorias"
    cursor.execute(query)
    categorias = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('listar_categorias.html', categorias=categorias)


if __name__ == '__main__':
    app.run(debug=True)