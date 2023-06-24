from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sympy import symbols, simplify, sympify, Matrix
from pydantic import BaseModel
from urllib.parse import unquote
import json
from mangum import Mangum

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/", "https://lauvsnes1.github.io/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


handler = Mangum(app, api_gateway_base_path=None)


x = symbols("x")


class Expression(BaseModel):
    expression: str


class MatrixModel(BaseModel):
    matrix: List[List[float]]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/rref/")
async def get_rref(matrix: MatrixModel):
    print("matrix:", matrix)
    try:
        sympy_matrix = Matrix(matrix.matrix)
        rref_matrix = sympy_matrix.rref()[0]
        return JSONResponse(
            content={"rref_matrix": str(rref_matrix)}, media_type="application/json"
        )
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(
            status_code=400, detail="Invalid data. Please check your input."
        )
    except Exception as e:
        print(f"General error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@app.post("/simplify/")
async def simplify_expression(data: Expression):
    expression = data.expression
    try:
        # Use sympify to convert the string expression to a SymPy expression
        sympy_expression = sympify(expression)

        # Simplify the expression
        simplified_expression = simplify(sympy_expression)

        # Convert the result to a string and return it
        return JSONResponse(
            content={"simplified_expression": str(simplified_expression)},
            media_type="application/json",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
