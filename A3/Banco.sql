-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS estoque;
USE estoque;

-- Criação da tabela de categorias
CREATE TABLE IF NOT EXISTS categorias (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nome VARCHAR(100) NOT NULL UNIQUE,
 descricao TEXT
);

-- Criação da tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nome VARCHAR(100) NOT NULL,
 descricao TEXT,
 preco DECIMAL(10, 2) NOT NULL,
 quantidade INT DEFAULT 0,
 categoria_id INT,
 FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Criação da tabela de entradas de produtos
CREATE TABLE IF NOT EXISTS entradas (
 id INT AUTO_INCREMENT PRIMARY KEY,
 produto_id INT,
 quantidade INT NOT NULL,
 data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Criação da tabela de saídas de produtos
CREATE TABLE IF NOT EXISTS saidas (
 id INT AUTO_INCREMENT PRIMARY KEY,
 produto_id INT,
 quantidade INT NOT NULL,
 data_saida DATETIME DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
