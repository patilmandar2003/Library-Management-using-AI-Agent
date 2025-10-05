import pymysql
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_USER_PASSWORD"),
    database="LIBRARY"
)

# Create a cursor object 
cursor = connection.cursor()

# Initialize LLM
model = OllamaLLM(
    model="mistral",  # Name of Ollama model to use
    temperature=0,      # Sampling temperatrue. Higher values make output more creative.
)

# State of Agent
class State(TypedDict):
    # User details
    role: Optional[str]     # Check whether user is staff member or subscriber
    user_id: Optional[str]  # ID of interacting individual

    # User queries
    intent: Optional[str]       # Action of user: search, borrow, return
    query: Optional[str]        # Query to search book or author
    book_id: Dict[str, Any]     # Book ID of the intended book
    book_name: Dict[str, Any]   # Book Name of the intended book
    book_author: Dict[str, Any] # Author of the intended book

    # Database queries
    search_action: Optional[str]
    available_books: List[str]  # Available books in the library
    borrowed_books: List[str]   # Borrowed books by the user
    returning_books: List[str]  # Books to be returned by the user
    no_copies: Optional[int]    # Number of copies available in the library

    # Track chat
    message: Optional[str]

def Query(state: State):
    """

    """

    print("="*100)
    query = str(input(">>"))
    print("_"*100)

    return {
        "query": query
    }

def SearchBook(state: State):
    return{}

def Author(state: State):
    return {}

def Book(state: State):
    return {}

def Summary(state: State):
    return {}

def Borrow(state: State):
    return {}

def UserStatus(state: State):
    return {}

def UpdateDB(state: State):
    return {}

def Subscription(state: State):
    return {}

# Routing Logic Functions 
def SearchAction(state: State) -> str:
    """
    LOGICAL FUNCTION:
    Determine what to search (author or book) based on user query.

    Returns:
    "author" or "book" based on condition
    """

    search_action_prompt = f"""
    You will be given a query from the user, analyze it and write a SQL query to fetch user information from the database.
    You will also be provided database schema to design SQL queries.
    Only provide requested information.

    Schema:

    Output should contain only the SQL query.
    """

    search_action_response = model.invoke(search_action_prompt)

    if search_action_prompt.lower == "book":
        return {
            "search_action": "book"
        }

    return {
        "search_action": "author"
    }

def BookAction(state: State) -> str:
    """
    LOGICAL FUNCTION:
    Determine whether user wants summary or wants to borrow a book.

    Returns:
    "summary" or "borrow" based on condition
    """
    return None

def BorrowAction(state: State) -> str:
    """
    LOGICAL FUNCTION:
    Determine whether user wants to borrow the book or not.

    Returns:
    "yes" or "no" based on condition
    """
    return None

# Create graph
library_graph = StateGraph(State)

# Add nodes
library_graph.add_node("Query", Query)
library_graph.add_node("Author", Author)
library_graph.add_node("Book", Book)
library_graph.add_node("Summary", Summary)
library_graph.add_node("Borrow", Borrow)
library_graph.add_node("UserStatus", UserStatus)
library_graph.add_node("UpdateDB", UpdateDB)
library_graph.add_node("Subscription", Subscription)

# Start the edges
library_graph.add_edge(START, "Query")

# Adding conditional branching from Query to author and book.
library_graph.add_conditional_edges(
    "Query",
    SearchAction,
    {
        "author": "Author",
        "book": "Book"
    }
)

library_graph.add_edge("Author", "Book")
# Adding conditional branching from Book to Summary and Borrow.
library_graph.add_conditional_edges(
    "Book",
    BookAction,
    {
        "summary": "Summary",
        "borrowAction": "BorrowAction"
    }
)

library_graph.add_conditional_edges(
    "Summary", 
    BorrowAction,
    {
        "yes": None,
        "no": None
    }
)

# Close cursor and connection
cursor.close()
connection.close()

