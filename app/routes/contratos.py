from quart import Blueprint, render_template, request, redirect, url_for
from sqlmodel import select
from app.models import Empresa, Contrato, UNSPSC
from app.database import AsyncSessionLocal
from datetime import datetime

contratos_bp = Blueprint("contratos", __name__)

@contratos_bp.route("/empresas/<int:id>/contrato/nuevo", methods=["GET", "POST"])
async def crear(id: int):
    async with AsyncSessionLocal() as session:
        if request.method == "POST":
            form = await request.form
            unspsc_str = form.get("unspsc", "")
            codigos = [code.strip() for code in unspsc_str.split(";") if code.strip()]

            nuevo = Contrato(
                empresa_id=id,
                numero_secop=form.get("numero_secop"),
                objeto=form.get("objeto"),
                valor=int(form.get("valor", 0)),
                fecha_adjudicacion=datetime.strptime(form.get("fecha_adjudicacion"), "%Y-%m-%d"),
                fecha_ejecucion_fin=datetime.strptime(form.get("fecha_ejecucion_fin"), "%Y-%m-%d") if form.get("fecha_ejecucion_fin") else None,
                estado=form.get("estado"),
                registrado_rup=form.get("registrado_rup") == "on"
            )

            for codigo in codigos:
                stmt = select(UNSPSC).where(UNSPSC.codigo == codigo)
                result = await session.execute(stmt)
                unspsc_obj = result.scalar_one_or_none()
                if not unspsc_obj:
                    unspsc_obj = UNSPSC(codigo=codigo)
                    session.add(unspsc_obj)
                nuevo.unspsc_codigos.append(unspsc_obj)

            session.add(nuevo)
            await session.commit()
            return redirect(url_for("empresas.ver", id=id))
            
        return await render_template("contratos/form.html", empresa_id=id)
