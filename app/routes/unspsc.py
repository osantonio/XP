from quart import Blueprint, render_template, request, redirect, url_for
from sqlmodel import select
from app.models import UNSPSC, Contrato, ContratoUNSPSC
from app.database import AsyncSessionLocal


unspsc_bp = Blueprint("unspsc", __name__, url_prefix="/unspsc")


@unspsc_bp.route("/")
async def listar():
    async with AsyncSessionLocal() as session:
        statement = select(UNSPSC).order_by(UNSPSC.codigo)
        results = await session.execute(statement)
        codigos = results.scalars().all()
    return await render_template("unspsc/listar.html", codigos=codigos)


@unspsc_bp.route("/crear", methods=["GET", "POST"])
async def crear():
    if request.method == "POST":
        form = await request.form
        codigo = form.get("codigo", "").strip()
        descripcion = form.get("descripcion", "").strip() or None

        if codigo:
            async with AsyncSessionLocal() as session:
                stmt = select(UNSPSC).where(UNSPSC.codigo == codigo)
                result = await session.execute(stmt)
                existente = result.scalar_one_or_none()
                if not existente:
                    nuevo = UNSPSC(codigo=codigo, descripcion=descripcion)
                    session.add(nuevo)
                    await session.commit()
                else:
                    existente.descripcion = descripcion
                    session.add(existente)
                    await session.commit()

            return redirect(url_for("unspsc.listar"))

    return await render_template("unspsc/crear.html")


