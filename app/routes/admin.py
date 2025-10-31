from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from app import db
from app.models import Product, Category, Order, User, Coupon, StoreSettings, Slide
from datetime import datetime
import os
import secrets

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Estatísticas de estoque
    low_stock_products = Product.query.filter(Product.stock < 10).count()
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    
    # Estatísticas de pedidos
    pending_orders = Order.query.filter_by(status='Pendente').count()
    confirmed_orders = Order.query.filter_by(status='Confirmado').count()
    
    # Receita total (apenas pedidos confirmados)
    total_revenue = db.session.query(db.func.sum(Order.total)).filter(Order.status == 'Confirmado').scalar() or 0
    
    # Produtos mais vendidos (top 5) - apenas pedidos confirmados
    from app.models import OrderItem
    from sqlalchemy import func
    best_sellers = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).join(Order).filter(Order.status == 'Confirmado').group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products,
                         out_of_stock=out_of_stock,
                         pending_orders=pending_orders,
                         confirmed_orders=confirmed_orders,
                         total_revenue=total_revenue,
                         best_sellers=best_sellers)

@admin_bp.route('/produtos')
@login_required
@admin_required
def products():
    search = request.args.get('search', '')
    category_id = request.args.get('category', '')
    status = request.args.get('status', '')
    stock_alert = request.args.get('stock_alert', '')
    
    query = Product.query
    
    if search:
        query = query.filter(
            or_(
                Product.name.contains(search),
                Product.code.contains(search),
                Product.description.contains(search)
            )
        )
    
    if category_id and category_id.isdigit():
        query = query.filter_by(category_id=int(category_id))
    
    if status == 'active':
        query = query.filter_by(active=True)
    elif status == 'inactive':
        query = query.filter_by(active=False)
    
    if stock_alert == 'low':
        query = query.filter(Product.stock < 10)
    
    products = query.all()
    categories = Category.query.all()
    
    low_stock_count = Product.query.filter(Product.stock < 10).count()
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         low_stock_count=low_stock_count,
                         search=search,
                         category_id=category_id,
                         status=status,
                         stock_alert=stock_alert)

@admin_bp.route('/produtos/adicionar', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        image_url = request.form.get('image_url')
        featured = request.form.get('featured') == 'on'
        
        product = Product(
            name=name,
            code=code,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image_url=image_url,
            featured=featured
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@admin_bp.route('/produtos/editar/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.code = request.form.get('code')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        product.image_url = request.form.get('image_url')
        product.featured = request.form.get('featured') == 'on'
        product.active = request.form.get('active') == 'on'
        
        db.session.commit()
        
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@admin_bp.route('/produtos/deletar/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('admin.products'))

@admin_bp.route('/categorias')
@login_required
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categorias/adicionar', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        
        # Processar upload de imagem
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                # Gerar nome seguro para o arquivo
                filename = secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Validar extensão
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
                if file_ext in allowed_extensions:
                    # Gerar nome único
                    unique_filename = f"category_{secrets.token_hex(8)}{file_ext}"
                    
                    # Salvar arquivo
                    upload_path = os.path.join('app', 'static', 'images', unique_filename)
                    file.save(upload_path)
                    
                    # Atualizar image_url com o caminho do arquivo
                    image_url = f'/static/images/{unique_filename}'
                else:
                    flash('Formato de imagem não permitido! Use JPG, PNG, GIF ou WEBP.', 'danger')
                    return redirect(url_for('admin.add_category'))
        
        category = Category(name=name, description=description, image_url=image_url)
        db.session.add(category)
        db.session.commit()
        
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/add_category.html')

@admin_bp.route('/categorias/editar/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        
        # Processar upload de nova imagem
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                # Gerar nome seguro para o arquivo
                filename = secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Validar extensão
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
                if file_ext in allowed_extensions:
                    # Gerar nome único
                    unique_filename = f"category_{secrets.token_hex(8)}{file_ext}"
                    
                    # Salvar arquivo
                    upload_path = os.path.join('app', 'static', 'images', unique_filename)
                    file.save(upload_path)
                    
                    # Atualizar image_url com o caminho do arquivo
                    category.image_url = f'/static/images/{unique_filename}'
                else:
                    flash('Formato de imagem não permitido! Use JPG, PNG, GIF ou WEBP.', 'danger')
                    return redirect(url_for('admin.edit_category', category_id=category_id))
        
        # Se não houver upload, verificar se há URL
        if not category.image_url or request.form.get('image_url'):
            image_url = request.form.get('image_url')
            if image_url:
                category.image_url = image_url
        
        db.session.commit()
        
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/edit_category.html', category=category)

@admin_bp.route('/categorias/deletar/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if category.products:
        flash('Não é possível deletar uma categoria com produtos.', 'danger')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Categoria deletada com sucesso!', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/pedidos')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/pedidos/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/pedidos/atualizar-status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    
    order.status = status
    db.session.commit()
    
    flash('Status do pedido atualizado!', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin_bp.route('/cupons')
@login_required
@admin_required
def coupons():
    coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
    return render_template('admin/coupons.html', coupons=coupons)

@admin_bp.route('/cupons/adicionar', methods=['GET', 'POST'])
@login_required
@admin_required
def add_coupon():
    if request.method == 'POST':
        code = request.form.get('code').strip().upper()
        discount_type = request.form.get('discount_type')
        discount_value = float(request.form.get('discount_value'))
        min_purchase = float(request.form.get('min_purchase', 0))
        max_uses = request.form.get('max_uses')
        valid_until = request.form.get('valid_until')
        
        if Coupon.query.filter_by(code=code).first():
            flash('Código de cupom já existe!', 'danger')
            return redirect(url_for('admin.add_coupon'))
        
        coupon = Coupon(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            min_purchase=min_purchase,
            max_uses=int(max_uses) if max_uses else None,
            valid_until=datetime.strptime(valid_until, '%Y-%m-%d') if valid_until else None
        )
        
        db.session.add(coupon)
        db.session.commit()
        
        flash('Cupom criado com sucesso!', 'success')
        return redirect(url_for('admin.coupons'))
    
    return render_template('admin/add_coupon.html')

@admin_bp.route('/cupons/editar/<int:coupon_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    
    if request.method == 'POST':
        coupon.discount_type = request.form.get('discount_type')
        coupon.discount_value = float(request.form.get('discount_value'))
        coupon.min_purchase = float(request.form.get('min_purchase', 0))
        max_uses = request.form.get('max_uses')
        coupon.max_uses = int(max_uses) if max_uses else None
        valid_until = request.form.get('valid_until')
        coupon.valid_until = datetime.strptime(valid_until, '%Y-%m-%d') if valid_until else None
        coupon.active = request.form.get('active') == 'on'
        
        db.session.commit()
        flash('Cupom atualizado com sucesso!', 'success')
        return redirect(url_for('admin.coupons'))
    
    return render_template('admin/edit_coupon.html', coupon=coupon)

@admin_bp.route('/cupons/deletar/<int:coupon_id>', methods=['POST'])
@login_required
@admin_required
def delete_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    
    flash('Cupom deletado com sucesso!', 'success')
    return redirect(url_for('admin.coupons'))

@admin_bp.route('/cupons/toggle/<int:coupon_id>', methods=['POST'])
@login_required
@admin_required
def toggle_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.active = not coupon.active
    db.session.commit()
    
    status = 'ativado' if coupon.active else 'desativado'
    flash(f'Cupom {status} com sucesso!', 'success')
    return redirect(url_for('admin.coupons'))

@admin_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
@admin_required
def store_settings():
    if request.method == 'POST':
        StoreSettings.set_setting('pickup_enabled', 'true' if request.form.get('pickup_enabled') else 'false')
        StoreSettings.set_setting('pickup_address', request.form.get('pickup_address', ''))
        StoreSettings.set_setting('delivery_enabled', 'true' if request.form.get('delivery_enabled') else 'false')
        StoreSettings.set_setting('free_shipping_min', request.form.get('free_shipping_min', '300'))
        StoreSettings.set_setting('shipping_cost', request.form.get('shipping_cost', '15'))
        
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.store_settings'))
    
    settings = {
        'pickup_enabled': StoreSettings.get_setting('pickup_enabled', 'true') == 'true',
        'pickup_address': StoreSettings.get_setting('pickup_address', ''),
        'delivery_enabled': StoreSettings.get_setting('delivery_enabled', 'true') == 'true',
        'free_shipping_min': float(StoreSettings.get_setting('free_shipping_min', '300')),
        'shipping_cost': float(StoreSettings.get_setting('shipping_cost', '15'))
    }
    
    return render_template('admin/store_settings.html', settings=settings)

@admin_bp.route('/slides')
@login_required
@admin_required
def slides():
    slides = Slide.query.order_by(Slide.order, Slide.created_at.desc()).all()
    return render_template('admin/slides.html', slides=slides)

@admin_bp.route('/slides/adicionar', methods=['GET', 'POST'])
@login_required
@admin_required
def add_slide():
    if request.method == 'POST':
        title = request.form.get('title')
        image_url = request.form.get('image_url')
        link = request.form.get('link')
        
        order_value = request.form.get('order', '0')
        try:
            order = int(order_value) if order_value and order_value.strip() else 0
        except ValueError:
            order = 0
        
        active = request.form.get('active') == 'on'
        
        slide = Slide(
            title=title,
            image_url=image_url,
            link=link,
            order=order,
            active=active
        )
        
        db.session.add(slide)
        db.session.commit()
        
        flash('Slide adicionado com sucesso!', 'success')
        return redirect(url_for('admin.slides'))
    
    return render_template('admin/add_slide.html')

@admin_bp.route('/slides/editar/<int:slide_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_slide(slide_id):
    slide = Slide.query.get_or_404(slide_id)
    
    if request.method == 'POST':
        slide.title = request.form.get('title')
        slide.image_url = request.form.get('image_url')
        slide.link = request.form.get('link')
        
        order_value = request.form.get('order', '0')
        try:
            slide.order = int(order_value) if order_value and order_value.strip() else 0
        except ValueError:
            slide.order = 0
        
        slide.active = request.form.get('active') == 'on'
        
        db.session.commit()
        
        flash('Slide atualizado com sucesso!', 'success')
        return redirect(url_for('admin.slides'))
    
    return render_template('admin/edit_slide.html', slide=slide)

@admin_bp.route('/slides/deletar/<int:slide_id>', methods=['POST'])
@login_required
@admin_required
def delete_slide(slide_id):
    slide = Slide.query.get_or_404(slide_id)
    db.session.delete(slide)
    db.session.commit()
    
    flash('Slide deletado com sucesso!', 'success')
    return redirect(url_for('admin.slides'))

@admin_bp.route('/slides/toggle/<int:slide_id>', methods=['POST'])
@login_required
@admin_required
def toggle_slide(slide_id):
    slide = Slide.query.get_or_404(slide_id)
    slide.active = not slide.active
    db.session.commit()
    
    status = 'ativado' if slide.active else 'desativado'
    flash(f'Slide {status} com sucesso!', 'success')
    return redirect(url_for('admin.slides'))
