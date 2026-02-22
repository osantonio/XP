from quart import Blueprint, render_template, request, redirect, url_for, flash
from sqlmodel import select, func
from app.models import Empresa, Contrato, UNSPSC, ContratoUNSPSC
from app.database import AsyncSessionLocal
from app.config import Config

empresas_bp = Blueprint("empresas", __name__, url_prefix="/empresas")

@empresas_bp.route("/")
async def listar():
    page = request.args.get("page", 1, type=int)
    async with AsyncSessionLocal() as session:
        # Paginación
        statement = select(Empresa).offset((page - 1) * Config.ITEMS_PER_PAGE).limit(Config.ITEMS_PER_PAGE)
        results = await session.execute(statement)
        empresas = results.scalars().all()
        
        # Total para paginación
        count_statement = select(func.count()).select_from(Empresa)
        count_result = await session.execute(count_statement)
        total = count_result.scalar()
        
        pages = (total + Config.ITEMS_PER_PAGE - 1) // Config.ITEMS_PER_PAGE

    return await render_template("empresas/listar.html", empresas=empresas, page=page, pages=pages, total=total)

@empresas_bp.route("/crear", methods=["GET", "POST"])
async def crear():
    if request.method == "POST":
        form = await request.form
        async with AsyncSessionLocal() as session:
            nueva = Empresa(
                nit=form.get("nit"),
                nombre=form.get("nombre"),
                rup_habilitado=form.get("rup_habilitado") == "on",
                capacidad_financiera=form.get("capacidad_financiera")
            )
            session.add(nueva)
            await session.commit()
            return redirect(url_for("empresas.listar"))
            
    return await render_template("empresas/crear.html", action="Nueva")

@empresas_bp.route("/<int:id>")
async def ver(id: int):
    async with AsyncSessionLocal() as session:
        statement = select(Empresa).where(Empresa.id == id)
        result = await session.execute(statement)
        empresa = result.scalar_one_or_none()
        
        if not empresa:
            return "Empresa no encontrada", 404
            
        contratos_stmt = select(Contrato).where(Contrato.empresa_id == id)
        contratos_res = await session.execute(contratos_stmt)
        contratos = contratos_res.scalars().all()

        contratos_con_codigos = []
        for contrato in contratos:
            stmt_codigos = (
                select(UNSPSC.codigo)
                .join(
                    ContratoUNSPSC,
                    UNSPSC.codigo == ContratoUNSPSC.unspsc_codigo,
                )
                .where(ContratoUNSPSC.contrato_id == contrato.id)
            )
            res_codigos = await session.execute(stmt_codigos)
            codigos = [row[0] for row in res_codigos.all()]
            contratos_con_codigos.append(
                {"contrato": contrato, "codigos_unspsc": codigos}
            )

    return await render_template("empresas/ver.html", empresa=empresa, contratos=contratos_con_codigos)
