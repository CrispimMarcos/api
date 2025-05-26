from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.database import engine, Base
from app.routers import auth_routes, client_routes, product_routes, order_routes
from app.core.config import settings

oauth2_scheme_docs = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="API Lu Estilo",
    description="API RESTful para gestão comercial da Lu Estilo",
    version="1.0.0",
    openapi_extra={
        "components": {
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Insira seu token JWT no formato 'Bearer SEU_TOKEN_AQUI' para acessar as rotas protegidas."
                }
            }
        },
        "security": [
            {"OAuth2PasswordBearer": []}
        ]
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(client_routes.router, prefix="/clients", tags=["Clientes"])
app.include_router(product_routes.router, prefix="/products", tags=["Produtos"])
app.include_router(order_routes.router, prefix="/orders", tags=["Pedidos"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Lu Estilo!"}
