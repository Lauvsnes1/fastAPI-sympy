from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, simplify, sympify, Matrix
from pydantic import BaseModel
from urllib.parse import unquote
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://lauvsnes1.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

x = symbols("x")


class Expression(BaseModel):
    expression: str


class MatrixModel(BaseModel):
    matrix: List[List[float]]


@app.post("/rref/")
async def get_rref(matrix: MatrixModel):
    try:
        sympy_matrix = Matrix(matrix.matrix)
        rref_matrix = sympy_matrix.rref()[0]
        return {"rref_matrix": str(rref_matrix)}
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"General error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
