from quart import Blueprint, render_template, request
from sqlmodel import select
from app.models import Empresa, Contrato, UNSPSC, ContratoUNSPSC
from app.database import AsyncSessionLocal
import itertools
from operator import itemgetter

simulador_bp = Blueprint("simulador", __name__)

@simulador_bp.route("/simular", methods=["GET", "POST"])
async def simular_consorcio():
    consorcios = []
    if request.method == "POST":
        form = await request.form
        raw_min_ex = form.get("min_ex", "0")
        normalized_min_ex = raw_min_ex.replace(".", "").replace(",", "")
        min_ex_millones = int(normalized_min_ex or 0)
        min_ex = min_ex_millones * 1_000_000
        max_contratos_per_empresa = max(1, int(form.get("max_contratos", 3)))
        unspsc_target = form.get("unspsc", "")
        
        async with AsyncSessionLocal() as session:
            statement = select(Contrato).where(Contrato.registrado_rup == True)
            results = await session.execute(statement)
            todos_contratos = results.scalars().all()
            
            empresas_calificadas = {}
            contrato_codigos = {}
            for c in todos_contratos:
                stmt_codigos = (
                    select(UNSPSC.codigo)
                    .join(
                        ContratoUNSPSC,
                        UNSPSC.codigo == ContratoUNSPSC.unspsc_codigo,
                    )
                    .where(ContratoUNSPSC.contrato_id == c.id)
                )
                res_codigos = await session.execute(stmt_codigos)
                tags = [row[0] for row in res_codigos.all()]
                if not tags:
                    continue
                if any(tag.startswith(unspsc_target) for tag in tags):
                    contrato_codigos[c.id] = set(tags)
                    if c.empresa_id not in empresas_calificadas:
                        empresas_calificadas[c.empresa_id] = []
                    empresas_calificadas[c.empresa_id].append(c)
            
            # 2. Para cada empresa, obtener el top X de contratos por valor
            perfil_empresas = []
            for emp_id, contratos in empresas_calificadas.items():
                stmt_emp = select(Empresa).where(Empresa.id == emp_id)
                emp_obj = (await session.execute(stmt_emp)).scalar_one()
                
                # Ordenar contratos por valor DESC y tomar los mejores X
                contratos_sorted = sorted(contratos, key=lambda x: x.valor, reverse=True)
                top_contratos = contratos_sorted[:max_contratos_per_empresa]
                suma_valor = sum(c.valor for c in top_contratos)
                
                codigos_sets = [contrato_codigos.get(c.id, set()) for c in top_contratos]
                codigos = set().union(*codigos_sets) if codigos_sets else set()

                perfil_empresas.append({
                    "empresa": emp_obj,
                    "valor_aportado": suma_valor,
                    "num_contratos": len(top_contratos),
                    "codigos": codigos
                })
            
            # 3. Generar combinaciones de 1 a 4 empresas
            posibles_consorcios = []
            for r in range(1, 5):
                for combo in itertools.combinations(perfil_empresas, r):
                    total_valor = sum(p["valor_aportado"] for p in combo)
                    total_contratos = sum(p["num_contratos"] for p in combo)
                    
                    if total_valor >= min_ex:
                        # Calcular cobertura UNSPSC (cuántos códigos únicos aportan)
                        cobertura = len(set().union(*(p["codigos"] for p in combo)))
                        
                        posibles_consorcios.append({
                            "miembros": combo,
                            "total_valor": total_valor,
                            "total_contratos": total_contratos,
                            "cobertura": cobertura,
                            "num_miembros": r
                        })
            
            # 4. Ordenar y seleccionar los mejores 3
            # Criterio: Menor # de miembros -> Mayor cobertura -> Mayor valor
            posibles_consorcios.sort(key=lambda x: (x["num_miembros"], -x["cobertura"], -x["total_valor"]))
            consorcios = posibles_consorcios[:3]

    return await render_template("simulador/listar.html", consorcios=consorcios)
