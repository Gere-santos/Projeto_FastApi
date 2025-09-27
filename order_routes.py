from fastapi import APIRouter, Depends, HTTPException
from dependency import pegar_funcao
from sqlalchemy.orm import Session
from dependency import pegar_funcao, verificar_token, Usuario
from schemas import PedidoSchema
from models import Pedido


order_router = APIRouter(prefix="/pedidos",tags=["pedidos"], dependencies=[Depends(verificar_token)] )

@order_router.get("/lista")
async def pedidos():
    """Essa é a rota de pedidos, todas as rotas precisam de autenticação"""
    return {"mensagem": "vc acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema:PedidoSchema, session: Session = Depends(pegar_funcao)):
    novo_pedido = Pedido(usuario= pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido Criado com Sucesso. ID do pedido:{novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_funcao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"Pedido número: {pedido.id} cancelado com sucesso!",
            "pedido": pedido}
 
