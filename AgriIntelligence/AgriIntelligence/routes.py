import os
import json
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, request, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Product, Message, PlantDisease, CropRecommendation, IrrigationRecommendation
from utils import allowed_file, predict_disease, recommend_crops, recommend_irrigation

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        user_type = request.form.get('user_type')
        location = request.form.get('location')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists', 'danger')
            return render_template('register.html')
            
        # Create new user
        user = User(username=username, email=email, full_name=full_name, 
                    user_type=user_type, location=location)
        user.set_password(password)
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('profile.html', user=current_user, products=products)


@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    current_user.full_name = request.form.get('full_name')
    current_user.bio = request.form.get('bio')
    current_user.location = request.form.get('location')
    
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile'))


# Crop recommendation routes
@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    if request.method == 'POST':
        soil_type = request.form.get('soil_type')
        climate = request.form.get('climate')
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        rainfall = float(request.form.get('rainfall', 0))
        ph = float(request.form.get('ph', 0))
        
        # Get crop recommendations based on input
        recommended_crops = recommend_crops(soil_type, climate, temperature, humidity, rainfall, ph)
        
        # Save recommendation to database
        recommendation = CropRecommendation(
            user_id=current_user.id,
            soil_type=soil_type,
            climate=climate,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall,
            ph=ph,
            recommended_crops=json.dumps(recommended_crops)
        )
        db.session.add(recommendation)
        db.session.commit()
        
        return render_template('crop_recommendation.html', 
                              recommendation=recommendation, 
                              recommended_crops=recommended_crops)
        
    return render_template('crop_recommendation.html')


# Disease identification routes
@app.route('/disease-identification', methods=['GET', 'POST'])
@login_required
def disease_identification():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'plant_image' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['plant_image']
        plant_type = request.form.get('plant_type')
        
        # If user does not select file, browser submits empty file without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Predict disease from the image
            disease, confidence = predict_disease(file_path, plant_type)
            
            # Save record to database
            disease_record = PlantDisease(
                user_id=current_user.id,
                image_path=file_path,
                plant_type=plant_type,
                diagnosis=disease,
                confidence=confidence
            )
            db.session.add(disease_record)
            db.session.commit()
            
            return render_template('disease_identification.html', 
                                  disease=disease_record,
                                  image_name=filename)
    
    return render_template('disease_identification.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Marketplace routes
@app.route('/marketplace')
def marketplace():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    # Query products with filters
    query = Product.query
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    if category and category != 'all':
        query = query.filter_by(category=category)
        
    products = query.order_by(Product.created_date.desc()).all()
    
    # Get all categories for filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('marketplace.html', products=products, categories=categories)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/product/add', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
    category = request.form.get('category')
    location = request.form.get('location') or current_user.location
    
    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        category=category,
        location=location,
        seller_id=current_user.id
    )
    
    db.session.add(product)
    db.session.commit()
    
    flash('Product added successfully', 'success')
    return redirect(url_for('marketplace'))


@app.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if current user is the owner
    if product.seller_id != current_user.id:
        flash('You do not have permission to delete this product', 'danger')
        return redirect(url_for('marketplace'))
        
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully', 'success')
    return redirect(url_for('marketplace'))


# Messaging routes
@app.route('/messages')
@login_required
def messages():
    # Get all users that current user has conversations with
    sent_to_ids = db.session.query(Message.recipient_id).filter_by(sender_id=current_user.id).distinct().all()
    received_from_ids = db.session.query(Message.sender_id).filter_by(recipient_id=current_user.id).distinct().all()
    
    # Combine and remove duplicates
    contact_ids = set([id[0] for id in sent_to_ids + received_from_ids])
    contacts = User.query.filter(User.id.in_(contact_ids)).all()
    
    # Count unread messages
    unread_counts = {}
    for contact in contacts:
        count = Message.query.filter_by(
            sender_id=contact.id, 
            recipient_id=current_user.id,
            read=False
        ).count()
        unread_counts[contact.id] = count
    
    return render_template('messages.html', contacts=contacts, unread_counts=unread_counts)


@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    
    # If POST, handle message send
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            message = Message(
                sender_id=current_user.id,
                recipient_id=user_id,
                content=content
            )
            db.session.add(message)
            db.session.commit()
    
    # Get conversation between current user and other user
    sent_messages = Message.query.filter_by(sender_id=current_user.id, recipient_id=user_id).all()
    received_messages = Message.query.filter_by(sender_id=user_id, recipient_id=current_user.id).all()
    
    # Mark received messages as read
    for message in received_messages:
        if not message.read:
            message.read = True
    db.session.commit()
    
    # Combine and sort by timestamp
    messages = sorted(sent_messages + received_messages, key=lambda x: x.timestamp)
    
    return render_template('conversation.html', messages=messages, other_user=other_user)


# Irrigation recommendation routes
@app.route('/irrigation', methods=['GET', 'POST'])
@login_required
def irrigation():
    if request.method == 'POST':
        crop_type = request.form.get('crop_type')
        soil_type = request.form.get('soil_type')
        area_size = float(request.form.get('area_size'))
        climate = request.form.get('climate')
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        rainfall = float(request.form.get('rainfall', 0))
        
        # Get irrigation recommendations
        recommendation, water_req, schedule = recommend_irrigation(
            crop_type, soil_type, area_size, climate, temperature, humidity, rainfall
        )
        
        # Save to database
        irrigation_record = IrrigationRecommendation(
            user_id=current_user.id,
            crop_type=crop_type,
            soil_type=soil_type,
            area_size=area_size,
            climate=climate,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall,
            recommendation=recommendation,
            water_requirement=water_req,
            schedule=json.dumps(schedule)
        )
        db.session.add(irrigation_record)
        db.session.commit()
        
        return render_template('irrigation.html', 
                             irrigation=irrigation_record,
                             schedule=schedule)
                             
    return render_template('irrigation.html')


# API endpoints for AJAX requests
@app.route('/api/messages/unread')
@login_required
def unread_message_count():
    count = Message.query.filter_by(
        recipient_id=current_user.id,
        read=False
    ).count()
    return jsonify({'count': count})


@app.route('/api/search/experts')
@login_required
def search_experts():
    query = request.args.get('query', '')
    experts = User.query.filter(
        User.user_type == 'expert',
        User.username.contains(query) | User.full_name.contains(query)
    ).limit(10).all()
    
    results = [{'id': expert.id, 'name': expert.full_name or expert.username} for expert in experts]
    return jsonify(results)
