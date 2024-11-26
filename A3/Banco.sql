-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.32-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para estoque
CREATE DATABASE IF NOT EXISTS `estoque` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `estoque`;

-- Copiando estrutura para tabela estoque.categorias
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.categorias: ~5 rows (aproximadamente)
INSERT IGNORE INTO `categorias` (`id`, `nome`, `descricao`) VALUES
	(1, 'Panela', 'De aço'),
	(2, 'Carros', 'pra andar'),
	(3, 'Roupas', 'Roupas em geral'),
	(4, 'TESTE', 'testes'),
	(5, 'Ferramentas', 'Ferramentas de Construção');

-- Copiando estrutura para tabela estoque.entradas
CREATE TABLE IF NOT EXISTS `entradas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `produto_id` int(11) DEFAULT NULL,
  `quantidade` int(11) NOT NULL,
  `data_entrada` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `entradas_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.entradas: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela estoque.logs_estoque
CREATE TABLE IF NOT EXISTS `logs_estoque` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entidade` varchar(50) NOT NULL,
  `entidade_id` int(11) NOT NULL,
  `acao` varchar(50) NOT NULL,
  `descricao` text DEFAULT NULL,
  `data_hora` timestamp NOT NULL DEFAULT current_timestamp(),
  `usuario` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.logs_estoque: ~8 rows (aproximadamente)
INSERT IGNORE INTO `logs_estoque` (`id`, `entidade`, `entidade_id`, `acao`, `descricao`, `data_hora`, `usuario`) VALUES
	(1, 'categoria', 1, 'edição', 'Categoria ID=1 editada. Novo Nome=\'Panela\', Descrição=\'De aço\'.', '2024-11-22 16:24:21', 'Desconhecido'),
	(2, 'categoria', 4, 'criação', 'Categoria \'TESTE\' criada com descrição: testes.', '2024-11-22 16:37:29', 'Desconhecido'),
	(3, 'produto', 6, 'criação', 'Produto \'testa\' cadastrado com 123 unidades e preço 123.0.', '2024-11-22 16:37:39', 'Desconhecido'),
	(4, 'produto', 1, 'edição', 'Produto \'TRAMONTINA\' foi atualizado: Preço=150.0, Quantidade=2.', '2024-11-22 16:47:22', 'Desconhecido'),
	(5, 'produto', 3, 'removido', 'Produto ID=3 foi removido.', '2024-11-22 16:47:55', 'Desconhecido'),
	(6, 'categoria', 1, 'edição', 'Categoria ID=1 editada. Novo Nome=\'Panela\', Descrição=\'De ferro\'.', '2024-11-23 14:16:46', '1'),
	(7, 'produto', 4, 'removido', 'Produto ID=4 foi removido.', '2024-11-23 16:05:35', '1'),
	(8, 'categoria', 5, 'criação', 'Categoria \'Ferramentas\' criada com descrição: Ferramentas de Construção.', '2024-11-23 19:04:05', '1'),
	(9, 'categoria', 1, 'edição', 'Categoria ID=1 editada. Novo Nome=\'Panela\', Descrição=\'De aço\'.', '2024-11-23 19:35:17', '1');

-- Copiando estrutura para tabela estoque.produtos
CREATE TABLE IF NOT EXISTS `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `preco` decimal(10,2) NOT NULL,
  `quantidade` int(11) DEFAULT 0,
  `categoria_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `produtos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.produtos: ~5 rows (aproximadamente)
INSERT IGNORE INTO `produtos` (`id`, `nome`, `descricao`, `preco`, `quantidade`, `categoria_id`) VALUES
	(1, 'TRAMONTINA', 'PANELA TRAMONTINA', 150.00, 2, 1),
	(2, 'Panela Redonda', 'é redonda', 250.00, 1, 1),
	(5, 'Moletom', 'Moletom Nike', 250.00, 123, 3),
	(6, 'testa', 'teste', 123.00, 123, 4);

-- Copiando estrutura para tabela estoque.saidas
CREATE TABLE IF NOT EXISTS `saidas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `produto_id` int(11) DEFAULT NULL,
  `quantidade` int(11) NOT NULL,
  `data_saida` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  CONSTRAINT `saidas_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.saidas: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela estoque.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'padrao',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela estoque.usuarios: ~1 rows (aproximadamente)
INSERT IGNORE INTO `usuarios` (`id`, `email`, `senha`, `role`) VALUES
	(1, '1403.gustavo.ramos@gmail.com', '12345678', 'admin'),
	(2, 'ibirapueraroleplay@gmail.com', 'jaqueline1234', 'viewer');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
