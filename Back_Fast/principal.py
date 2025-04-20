from fastapi import FastAPI, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

# Importar el router de autenticación
from routers import auth

app = FastAPI()

# --- Configuración CORS ---
# Permitir solicitudes desde el frontend de Vue (ajusta el origen si es necesario)
origins = [
    "http://localhost:5173", # Origen común para Vite dev server
    "http://127.0.0.1:5173",
    # Añade aquí otros orígenes si es necesario (ej. tu IP local)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permitir todos los headers
)
# --- Fin Configuración CORS ---


@app.get("/")
def escribir():
    return {"Hello": "World"}

# Incluir el router de autenticación
# Los endpoints /register y /login ahora están definidos en routers/auth.py
app.include_router(auth.router, prefix="/auth")