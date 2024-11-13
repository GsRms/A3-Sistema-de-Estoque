from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        database='estoque',
        user='root',
        password=''
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastrar_categoria', methods=['GET', 'POST'])
def cadastrar_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO categorias (nome, descricao) VALUES (%s, %s)", (nome, descricao))
            connection.commit()
            flash("Categoria cadastrada com sucesso!", "success")
        except Exception as e:
            flash(f"Erro: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('cadastrar_categoria'))
    return render_template('cadastrar_categoria.html')

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = 1  # Ajustar conforme a lógica
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
        return redirect(url_for('cadastrar_produto'))
    return render_template('cadastrar_produto.html')

if __name__ == '__main__':
    app.run(debug=True)
