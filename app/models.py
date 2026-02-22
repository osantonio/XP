from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, BigInteger

class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nit: str = Field(index=True, unique=True)
    nombre: str
    rup_habilitado: bool = False
    capacidad_financiera: str  # S (Suficiente), M (Media), T (Total) - p.ej.
    
    contratos: List["Contrato"] = Relationship(back_populates="empresa")
    contactos: List["Contacto"] = Relationship(back_populates="empresa")

class ContratoUNSPSC(SQLModel, table=True):
    contrato_id: int = Field(foreign_key="contrato.id", primary_key=True)
    unspsc_codigo: str = Field(foreign_key="unspsc.codigo", primary_key=True)


class UNSPSC(SQLModel, table=True):
    codigo: str = Field(primary_key=True, index=True)
    descripcion: Optional[str] = None

    contratos: List["Contrato"] = Relationship(
        back_populates="unspsc_codigos", link_model=ContratoUNSPSC
    )


class Contrato(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="empresa.id")
    numero_secop: str = Field(index=True)
    objeto: str
    valor: int = Field(  # Valor en pesos colombianos (COP)
        sa_column=Column(BigInteger)
    )
    fecha_adjudicacion: datetime
    fecha_ejecucion_fin: Optional[datetime] = None
    estado: str
    registrado_rup: bool = False

    empresa: Empresa = Relationship(back_populates="contratos")
    unspsc_codigos: List[UNSPSC] = Relationship(
        back_populates="contratos", link_model=ContratoUNSPSC
    )

class Contacto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    empresa_id: int = Field(foreign_key="empresa.id")
    nombre: str
    cargo: str
    email: str
    telefono: str

    empresa: Empresa = Relationship(back_populates="contactos")
