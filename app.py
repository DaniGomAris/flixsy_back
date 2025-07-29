from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.users import users_bp
from routes.movies import movies_bp

app = Flask(__name__)
CORS(app)

# 🔐 Configurar clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # 🔒 Usa una variable de entorno en producción

# 🔐 Inicializar JWT
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(movies_bp, url_prefix="/movies")

if __name__ == "__main__":
    app.run(debug=True)
