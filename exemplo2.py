from langchain.chains import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
import warnings
warnings.filterwarnings("ignore")

db_path = "db/rma.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

write_query = create_sql_query_chain(llm, db)

execute_query = QuerySQLDataBaseTool(db=db)

from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

print(chain.invoke({"question": "Quais são os status dos rmas?"}))
