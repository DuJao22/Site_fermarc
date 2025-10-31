from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.cart import cart_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.reviews import reviews_bp
    from app.routes.payment import payment_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(payment_bp, url_prefix='/pagamento')
    
    @app.context_processor
    def inject_categories():
        from app.models import Category
        categories = Category.query.all()
        return dict(categories=categories)
    
    with app.app_context():
        db.create_all()
        from app.models import User, Category, Product
        
        if User.query.count() == 0:
            admin_password = os.environ.get('ADMIN_PASSWORD')
            if not admin_password:
                admin_password = 'TrocarSenha123!'
                print("WARNING: Using default admin password. Set ADMIN_PASSWORD environment variable for production!")
            
            admin = User(
                username='admin',
                email='admin@fermarc.com.br',
                is_admin=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created with email: admin@fermarc.com.br")
        
        if Category.query.count() == 0:
            categories = [
                Category(name='Arduino', description='Placas e módulos Arduino'),
                Category(name='Raspberry Pi', description='Computadores e acessórios Raspberry Pi'),
                Category(name='Sensores', description='Sensores diversos para projetos'),
                Category(name='Módulos', description='Módulos eletrônicos variados'),
                Category(name='Componentes', description='Componentes eletrônicos gerais'),
                Category(name='Kits Didáticos', description='Kits para aprendizado'),
                Category(name='Ferramentas', description='Ferramentas para eletrônica'),
                Category(name='Impressão 3D', description='Impressoras e filamentos 3D')
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("Categories created")
        
        if Product.query.count() == 0:
            arduino_cat = Category.query.filter_by(name='Arduino').first()
            sensor_cat = Category.query.filter_by(name='Sensores').first()
            kit_cat = Category.query.filter_by(name='Kits Didáticos').first()
            
            products = [
                Product(
                    name='Arduino Uno R3',
                    code='ARD-UNO-R3',
                    description='Placa Arduino Uno R3 original com ATmega328P',
                    price=89.90,
                    stock=50,
                    category_id=arduino_cat.id if arduino_cat else 1,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=Arduino+Uno'
                ),
                Product(
                    name='Sensor Ultrassônico HC-SR04',
                    code='SEN-HC-SR04',
                    description='Sensor de distância ultrassônico 2cm a 4m',
                    price=12.90,
                    stock=100,
                    category_id=sensor_cat.id if sensor_cat else 3,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=HC-SR04'
                ),
                Product(
                    name='Kit Iniciante Arduino',
                    code='KIT-INI-ARD',
                    description='Kit completo para iniciantes em Arduino com mais de 150 componentes',
                    price=189.90,
                    stock=30,
                    category_id=kit_cat.id if kit_cat else 6,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=Kit+Arduino'
                ),
                Product(
                    name='ESP32 DevKit',
                    code='ESP32-DEV',
                    description='Placa de desenvolvimento ESP32 com WiFi e Bluetooth',
                    price=45.90,
                    stock=75,
                    category_id=arduino_cat.id if arduino_cat else 1,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=ESP32'
                ),
                Product(
                    name='Sensor DHT22',
                    code='SEN-DHT22',
                    description='Sensor de temperatura e umidade digital',
                    price=28.90,
                    stock=60,
                    category_id=sensor_cat.id if sensor_cat else 3,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=DHT22'
                ),
                Product(
                    name='Arduino Nano',
                    code='ARD-NANO',
                    description='Placa Arduino Nano compacta',
                    price=35.90,
                    stock=80,
                    category_id=arduino_cat.id if arduino_cat else 1,
                    image_url='https://via.placeholder.com/300x300/DC143C/FFFFFF?text=Nano'
                )
            ]
            db.session.add_all(products)
            db.session.commit()
            print("Sample products created")
    
    return app
