from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.equipamento_model import Equipamento
from entidades.models.categoria_model import CategoriaEquipamento


def cadastrarEquipamento(equipamento_data: Equipamento, db: Session):
    try:
        categoria = db.get(CategoriaEquipamento, equipamento_data.equipamento_categoria_id)
        
        if not categoria:
            raise ValueError("Categoria informada não existe")
        
        equipamento = Equipamento(**equipamento_data.model_dump(exclude={"equipamento_id", "equipamento_categoria"}))
        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)
        return equipamento
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError("Verifique os dados") from e

def listarEquipamento(db: Session):
    try:
        equipamento = db.exec(select(Equipamento)).all()
        
        if not equipamento:
            raise HTTPException("Nenhum equipamento foi encontrado")
    
        return equipamento
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e

def editarEquipamento(id: int, equipamentos: Equipamento, db: Session):
    try:
        equipamento = db.get(Equipamento, id)
        
        if not equipamento: 
            raise HTTPException("Nenhum equipamento encontrado")
        
        equipamento.nome = equipamentos.nome
        equipamento.patrimonio = equipamentos.patrimonio
        equipamento.marca = equipamentos.marca
        equipamento.modelo = equipamentos.modelo
        equipamento.descricao = equipamentos.descricao
        equipamento.status_equipamento = equipamentos.status_equipamento
        equipamento.equipamento_categoria_id = equipamentos.equipamento_categoria_id

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

def deletarEquipamento(id: int, db: Session):
    try:
        equipamento = db.exec(select(Equipamento).where(Equipamento.equipamento_id == id)).first()
        
        if not equipamento: 
            raise HTTPException("Nenhum equipamento encontrado")

        db.delete(equipamento)
        db.commit()

        return {
            "Equipamento deletado com sucesso"
        }    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e