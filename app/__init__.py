from quart import Quart
from app.config import Config
from app.database import init_db

def create_app(config_class=Config):
    app = Quart(__name__)
    app.config.from_object(config_class)

    @app.before_serving
    async def startup():
        await init_db()

    # Register Blueprints
    from app.routes.base import base_bp
    from app.routes.empresas import empresas_bp
    from app.routes.contratos import contratos_bp
    from app.routes.simulador import simulador_bp
    from app.routes.unspsc import unspsc_bp

    app.register_blueprint(base_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(contratos_bp)
    app.register_blueprint(simulador_bp)
    app.register_blueprint(unspsc_bp)

    return app
