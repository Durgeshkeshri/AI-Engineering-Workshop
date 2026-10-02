"""
Project 1 — Local Tools & Schemas
==================================
Consolidates all Python function tools, Gemini FunctionDeclaration schemas,
and TOOL_REGISTRY mapping into a single clean module.
"""

import ast
import json
import operator
from datetime import datetime
from pathlib import Path
from google.genai import types

DATA_DIR = Path(__file__).parent.parent / "data"
_faq = json.loads((DATA_DIR / "faq.json").read_text(encoding="utf-8"))


def get_current_datetime() -> dict:
    """Returns the current date and time in IST."""
    now = datetime.now()
    return {
        "date": now.strftime("%A, %d %B %Y"),
        "time": now.strftime("%I:%M %p"),
        "timezone": "IST (UTC+5:30)",
    }


_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _evaluate(node):
    """Evaluates a parsed expression, allowing only numbers and arithmetic operators."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Only numbers and + - * / // % ** ( ) are allowed.")


def calculate(expression: str) -> dict:
    """Safely evaluates a mathematical expression (no eval, arithmetic only)."""
    try:
        return {"result": _evaluate(ast.parse(expression.strip(), mode="eval"))}
    except Exception as exc:
        return {"error": str(exc)}


def search_faq(query: str) -> dict:
    """Searches the Bharati Vidyapeeth FAQ database for a query."""
    query_words = query.lower().split()
    for question, answer in _faq.items():
        if any(word in question.lower() for word in query_words):
            return {"question": question, "answer": answer}
    return {
        "answer": "No specific match found in FAQ. Please contact Bharati Vidyapeeth administration at principal@bharatividyapeeth.edu."
    }


FUNCTION_TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_current_datetime",
                description="Returns current date and time in IST. Use whenever user asks for current time or date.",
            )
        ]
    ),
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="calculate",
                description="Evaluates a mathematical expression and returns the result.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "expression": types.Schema(
                            type=types.Type.STRING,
                            description="Mathematical expression using numbers and +, -, *, /, (). Example: '(12 + 8) * 3'",
                        )
                    },
                    required=["expression"],
                ),
            )
        ]
    ),
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_faq",
                description="Searches Bharati Vidyapeeth FAQ database for admissions, fees, courses, placements, facilities, etc.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="Topic or question to search in college FAQ database.",
                        )
                    },
                    required=["query"],
                ),
            )
        ]
    ),
]

TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "calculate": calculate,
    "search_faq": search_faq,
}
