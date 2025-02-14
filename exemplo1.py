from langchain.chains import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
import warnings
warnings.filterwarnings("ignore")

db_path = "db/rma.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "Quais são os status dos rmas?"})
print(response)