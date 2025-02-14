from langchain.chains import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
import warnings
warnings.filterwarnings("ignore")

db_path = "db/rma.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

from langchain_community.agent_toolkits import create_sql_agent

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

agent_executor.invoke(
    {
        "input": "Quais são os status dos rmas?"
    }
)

