from entidades.models.categoria_model import CategoriaEquipamento
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, IntegrityError

def inserirCategoria(categoria: CategoriaEquipamento, db: Session):

    categoria_exixtente = db.exec(
        select(CategoriaEquipamento).where(
            CategoriaEquipamento.categoria_name == categoria.categoria_name
        )
    ).first()
    
    if categoria_exixtente:
        raise HTTPException(
            status_code=400,
            detail="Nome duplicado"
        )
        
    categoria_insert = CategoriaEquipamento.model_validate(categoria)
    db.add(categoria_insert)
    db.commit()
    db.refresh(categoria_insert)
    return categoria_insert

def listaCategoria(db: Session):
    try:
        categoria = db.exec(select(CategoriaEquipamento)).all()
        
        if not categoria: 
            raise HTTPException("Nenhuma categoria encontrada")
        
        return categoria
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e

def editarCategoria(id: int, categorias: CategoriaEquipamento, db: Session):
    try:
        categoria = db.get(CategoriaEquipamento, id)
        
        if not categoria: 
            raise HTTPException("Nenhuma categoria encontrada")
        
        categoria.categoria_name = categorias.categoria_name

        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        return categoria
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

def deletarCategoria(id: int, db: Session):
    try:
        categoria = db.exec(select(CategoriaEquipamento).where(CategoriaEquipamento.categoria_id == id)).first()
        
        if not categoria: 
            raise HTTPException("Nenhuma categoria encontrada")

        db.delete(categoria)
        db.commit()

        return {
            "Categoria deletada com sucesso"
        }    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Não e possivel excluir esta categoria, existe equipamentos vinculado a este Id"
        ) 