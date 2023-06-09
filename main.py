from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, simplify, sympify
from pydantic import BaseModel
from urllib.parse import unquote

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Allow requests from your frontend server's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


x = symbols("x")


class Expression(BaseModel):
    expression: str


@app.post("/simplify/")
async def simplify_expression(data: Expression):
    expression = data.expression
    try:
        # Use sympify to convert the string expression to a SymPy expression
        sympy_expression = sympify(expression)

        # Simplify the expression
        simplified_expression = simplify(sympy_expression)

        # Convert the result to a string and return it
        return {"simplified_expression": str(simplified_expression)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))