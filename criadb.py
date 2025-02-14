import sqlite3

# Nome do banco de dados
DB_NAME = "rma_ptbr.db"

def criar_banco_dados():
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Criar tabela de Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            endereco TEXT
        );
    ''')

    # Criar tabela de Produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo_sku TEXT UNIQUE NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL
        );
    ''')

    # Criar tabela de Status do RMA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_rma (
            id_status INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_status TEXT UNIQUE NOT NULL
        );
    ''')

    # Criar tabela de Solicitações de RMA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_rma (
            id_rma INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            data_solicitacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            id_status INTEGER NOT NULL,
            motivo TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_status) REFERENCES status_rma(id_status)
        );
    ''')

    # Criar tabela de Itens dentro de um RMA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_rma (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_rma INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            descricao_problema TEXT,
            FOREIGN KEY (id_rma) REFERENCES solicitacoes_rma(id_rma),
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
        );
    ''')

    # Inserir dados básicos de status do RMA (se não existirem)
    status_rma = [
        (1, "Pendente"),
        (2, "Aprovado"),
        (3, "Rejeitado"),
        (4, "Processado")
    ]
    cursor.executemany("INSERT OR IGNORE INTO status_rma (id_status, nome_status) VALUES (?, ?);", status_rma)

    # Inserir dados fictícios em Clientes
    clientes = [
        ("João Silva", "joao@email.com", "11999998888", "Rua A, 123"),
        ("Maria Oliveira", "maria@email.com", "21988887777", "Av. B, 456")
    ]
    cursor.executemany("INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?);", clientes)

    # Inserir dados fictícios em Produtos
    produtos = [
        ("Celular XYZ", "XYZ123", "Celular de última geração", 2500.00),
        ("Notebook ABC", "ABC456", "Notebook para trabalho e estudos", 4500.00)
    ]
    cursor.executemany("INSERT INTO produtos (nome, codigo_sku, descricao, preco) VALUES (?, ?, ?, ?);", produtos)

    # Inserir dados fictícios em Solicitações de RMA
    solicitacoes_rma = [
        (1, "2024-02-12", 1, "Tela quebrada"),
        (2, "2024-02-11", 2, "Bateria não carrega")
    ]
    cursor.executemany("INSERT INTO solicitacoes_rma (id_cliente, data_solicitacao, id_status, motivo) VALUES (?, ?, ?, ?);", solicitacoes_rma)

    # Inserir dados fictícios em Itens de RMA
    itens_rma = [
        (1, 1, 1, "Tela rachada após queda"),
        (2, 2, 1, "Aparelho não liga")
    ]
    cursor.executemany("INSERT INTO itens_rma (id_rma, id_produto, quantidade, descricao_problema) VALUES (?, ?, ?, ?);", itens_rma)

    # Commitar e fechar conexão
    conn.commit()
    conn.close()
    print("Banco de dados criado e populado com sucesso! 🚀")

if __name__ == "__main__":
    criar_banco_dados()
