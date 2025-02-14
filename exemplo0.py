from langchain.chains import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
import warnings
warnings.filterwarnings("ignore")

db_path = "db/rma.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM rma_status LIMIT 10;"))


