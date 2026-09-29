from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from dependencia.depenndencia import Database
from entidades.models.equipamento_model import Equipamento
from controllers.equipamento_controller import cadastrarEquipamento, listarEquipamento, editarEquipamento, deletarEquipamento
from entidades.models.equipamento_model import EquipamentoResponse

equipamento_router = APIRouter()

database = Database()

@equipamento_router.post("/salvaEquipamento",response_model=EquipamentoResponse)
def cadastrar_equipamento(equipamento: Equipamento, db: Session = Depends(database.get_session)):
    try:
        return cadastrarEquipamento(equipamento, db)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@equipamento_router.get("/listarEquipamento")
def buscar_equipamento(db: Session = Depends(database.get_session)):
    try:
        return listarEquipamento(db)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@equipamento_router.put("/editar_equipamento/{id}")
def editarEquipamentos(id:int, equipamento: Equipamento, db: Session = Depends(database.get_session)):
    try:
        return editarEquipamento(id, equipamento, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@equipamento_router.delete("/deletar_equipamento/{id}")
def deletar_Equipamento(id:int, db: Session = Depends(database.get_session)):
    try:
        deletarEquipamento(id, db)

        return{"Deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
