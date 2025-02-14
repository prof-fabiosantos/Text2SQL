from typing_extensions import Annotated, TypedDict
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
import warnings
from langchain import hub

warnings.filterwarnings("ignore")

# Configuração do banco de dados SQLite
db_path = "db/rma.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Configuração do modelo de linguagem
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

# Definição do estado para armazenar a consulta e resultados
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

# Carregar template para gerar consultas SQL
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

# Definição do formato de saída esperado
class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

# Função para gerar a consulta SQL automaticamente
def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )

    print("\n=== Prompt enviado ao LLM ===")
    print(prompt)

    structured_llm = llm.with_structured_output(QueryOutput)
    
    try:
        result = structured_llm.invoke(prompt)
        if result is None:
            raise ValueError("Erro: O modelo não retornou uma resposta válida para a consulta SQL.")
        
        if "query" not in result:
            raise ValueError(f"Erro: A resposta do modelo não contém 'query'. Resposta: {result}")

        return {"query": result["query"]}

    except Exception as e:
        print(f"Erro ao gerar a consulta SQL: {e}")
        return {"query": "SELECT 'Erro ao gerar consulta SQL'"}  # Consulta SQL padrão para evitar falha total


# Função para executar a consulta SQL
def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

# Função para interpretar os resultados e gerar uma resposta
def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

# Função principal para executar todo o fluxo
def main():
    # Criar o estado inicial com a pergunta desejada
    state = {"question": "Quais são os status de RMAs?"}
    
    # Gerar a consulta SQL
    state.update(write_query(state))
    print("Consulta SQL gerada:", state["query"])
    
    # Executar a consulta no banco de dados
    state.update(execute_query(state))
    print("Resultado da consulta:", state["result"])
    
    # Gerar a resposta final baseada na consulta
    state.update(generate_answer(state))
    print("Resposta:", state["answer"])

# Executar o código principal
if __name__ == "__main__":
    main()
