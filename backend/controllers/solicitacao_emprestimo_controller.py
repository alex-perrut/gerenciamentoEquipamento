from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models.solicitacao_emprestimo_model import SolicitacaoEmprestimo
from entidades.models.equipamento_model import Equipamento
from entidades.models.usuario_model import Usuarios

def cadastrarSolicitacao(solicitacao_data: SolicitacaoEmprestimo, db: Session):
    try:
        usuario = db.get(Usuarios, solicitacao_data.usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        equipamento = db.get(Equipamento, solicitacao_data.equipamento_id)
        if not equipamento:
            raise ValueError("Equipamento não encontrado")

        db.add(solicitacao_data)
        db.commit()
        db.refresh(solicitacao_data)
        return solicitacao_data

    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados informados") from e

def listarSolicitacao(db: Session):
    try:
        solicitacao = db.exec(select(SolicitacaoEmprestimo)).all()
        
        if not solicitacao:
            raise HTTPException("Nenhuma solicitação foi encontrada")
    
        return solicitacao
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e

def editarSolicitacao(id: int, solicitacoes: SolicitacaoEmprestimo, db: Session):
    try:
        solicitacao = db.get(SolicitacaoEmprestimo, id)
        
        if not solicitacao: 
            raise HTTPException("Nenhuma solicitação encontrada")
        
        solicitacao.status_solicitacao = solicitacoes.status_solicitacao
        solicitacao.id_aprovador = solicitacoes.id_aprovador

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao
    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e
    except IntegrityError as e:
        raise ValueError("Erro de integridade nos dados informados") from e

def deletarSolicitacao(id: int, db: Session):
    try:
        solicitacao = db.exec(select(SolicitacaoEmprestimo).where(SolicitacaoEmprestimo.id_solicitacao_emprestimo == id)).first()
        
        if not solicitacao: 
            raise HTTPException("Nenhuma solicitação encontrada")

        db.delete(solicitacao)
        db.commit()

        return {
            "Solicitação deletada com sucesso"
        }    
    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o Banco de Dados") from e