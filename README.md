# 🧵 API - Lu Estilo

API RESTful desenvolvida com **FastAPI** para apoiar o time comercial da empresa Lu Estilo. A API centraliza o gerenciamento de clientes, produtos e pedidos, além de permitir o envio **automático de mensagens via WhatsApp** com a integração da plataforma [UltraMsg](https://ultramsg.com/).

---

## 📌 Descrição do Problema

A Lu Estilo é uma empresa de confecção que busca novas oportunidades de negócio. No entanto, seu time comercial não possui nenhuma ferramenta tecnológica para facilitar o processo de vendas ou a comunicação com os clientes.

---

## 💡 Solução

Desenvolvimento de uma API RESTful que:

- Gerencia **clientes**, **produtos** e **pedidos**.
- Realiza **autenticação e autorização via JWT**.
- Envia **mensagens automáticas via WhatsApp** para eventos como:
  - Criação de pedidos.
  - Envio de orçamentos.
  - Promoções.

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.11+
- ⚡ FastAPI
- 🧪 Pytest
- 🐘 PostgreSQL
- 🐳 Docker e Docker Compose
- 🔐 JWT Authentication
- 📦 Alembic (migrações)
- 📞 UltraMsg API (WhatsApp)

---

## 🔐 Autenticação e Autorização

- Registro (`POST /auth/register`)
- Login com JWT (`POST /auth/login`)
- Refresh Token (`POST /auth/refresh-token`)
- Níveis de acesso:
  - `admin`: acesso completo.
  - `user`: acesso restrito.

---

## 🔗 Endpoints Principais

### 📍 Autenticação
- `POST /auth/register` – Registro de usuário.
- `POST /auth/login` – Login com JWT.
- `POST /auth/refresh-token` – Renovação de token.

### 👤 Clientes
- `GET /clients` – Listar clientes (com paginação e filtro).
- `POST /clients` – Criar cliente (valida CPF e e-mail únicos).
- `GET /clients/{id}` – Buscar cliente.
- `PUT /clients/{id}` – Atualizar cliente.
- `DELETE /clients/{id}` – Remover cliente.

### 📦 Produtos
- `GET /products` – Listar produtos (filtros: categoria, preço, estoque).
- `POST /products` – Criar produto (com imagem, código de barras, validade etc).
- `GET /products/{id}` – Buscar produto.
- `PUT /products/{id}` – Atualizar produto.
- `DELETE /products/{id}` – Remover produto.

### 🧾 Pedidos
- `GET /orders` – Listar pedidos (filtros: cliente, status, período etc).
- `POST /orders` – Criar pedido (validação de estoque).
- `GET /orders/{id}` – Buscar pedido.
- `PUT /orders/{id}` – Atualizar pedido/status.
- `DELETE /orders/{id}` – Excluir pedido.

### 📲 WhatsApp (via UltraMsg)
- Envio automático de mensagens para o número do cliente ao criar um novo pedido.
- Integração via `requests` com token e instance ID seguros.

---

## 📤 Deploy com Docker

### Requisitos

- Docker
- Docker Compose

### Subir o projeto:

```bash
docker-compose up --build
