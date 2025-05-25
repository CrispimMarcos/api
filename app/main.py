from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth_routes, client_routes, product_routes, order_routes

app = FastAPI(
    title="API Lu Estilo",
    description="API RESTful para gestão comercial da Lu Estilo",
    version="1.0.0"
)

# Configuração de CORS (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique domínios front-end aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criação das tabelas (ou migrações com Alembic, recomendado)
Base.metadata.create_all(bind=engine)

# Incluindo router
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(client_routes.router, prefix="/clients", tags=["Clientes"])
app.include_router(product_routes.router, prefix="/products", tags=["Produtos"])
app.include_router(order_routes.router, prefix="/orders", tags=["Pedidos"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Lu Estilo!"}

