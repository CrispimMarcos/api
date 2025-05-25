from app.services.whatsapp import send_message_via_whatsapp
from app.models import Order, Client  # Exemplo, ajuste conforme seu models
from fastapi import HTTPException

def create_order(order_data, db_session):
    # Aqui você faz a lógica para criar o pedido, validar estoque, salvar no DB
    # Exemplo simplificado:
    novo_pedido = Order(**order_data)
    db_session.add(novo_pedido)
    db_session.commit()
    db_session.refresh(novo_pedido)

    # Notificar cliente via WhatsApp
    cliente = db_session.query(Client).filter(Client.id == novo_pedido.client_id).first()
    if cliente and cliente.phone_number:
        mensagem = f"Olá {cliente.name}, seu pedido #{novo_pedido.id} foi criado com sucesso!"
        try:
            send_message_via_whatsapp(cliente.phone_number, mensagem)
        except Exception as e:
            # Logue o erro, mas não interrompa o fluxo
            print(f"Erro notificando cliente no WhatsApp: {e}")

    return novo_pedido


def get_orders(db_session):
    # Aqui você faz a lógica para buscar os pedidos
    return db_session.query(Order).all()