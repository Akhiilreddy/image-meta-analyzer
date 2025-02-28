import os
from PIL import Image
from PIL.ExifTags import TAGS
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse  # Use urllib.parse instead of werkzeug.urls
from werkzeug.utils import secure_filename
from app import app, db
from forms import LoginForm, RegistrationForm, UploadForm
from models import User, ImageMetadata

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if not exif:
                return {}

            metadata = {}
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode(errors='ignore')
                metadata[tag] = str(data)

            return {
                'camera_model': metadata.get('Model', 'Unknown'),
                'exposure_time': metadata.get('ExposureTime', 'Unknown'),
                'f_number': metadata.get('FNumber', 'Unknown'),
                'iso': metadata.get('ISOSpeedRatings', 'Unknown'),
                'focal_length': metadata.get('FocalLength', 'Unknown'),
                'gps_coords': metadata.get('GPSInfo', 'Unknown'),
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode
            }
    except Exception as e:
        app.logger.error(f"Error extracting metadata: {str(e)}")
        return {}

@app.route('/')
@app.route('/index')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UploadForm()
    if form.validate_on_submit():
        if not form.image.data:
            flash('No file selected')
            return redirect(request.url)

        file = form.image.data
        if not allowed_file(file.filename):
            flash('Invalid file type')
            return redirect(request.url)

        try:
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Extract metadata
            metadata = extract_image_metadata(filepath)

            # Create database entry
            image_meta = ImageMetadata(
                filename=filename,
                user_id=current_user.id,
                **metadata
            )
            db.session.add(image_meta)
            db.session.commit()

            flash('Image analyzed successfully!')
            return redirect(url_for('dashboard'))

        except Exception as e:
            app.logger.error(f"Error processing image: {str(e)}")
            flash('Error processing image')
            return redirect(request.url)

    recent_images = ImageMetadata.query.filter_by(user_id=current_user.id).order_by(ImageMetadata.upload_date.desc()).limit(5)
    return render_template('dashboard.html', title='Dashboard', form=form, images=recent_images)

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    images = ImageMetadata.query.filter_by(user_id=current_user.id).order_by(
        ImageMetadata.upload_date.desc()).paginate(page=page, per_page=10)
    return render_template('history.html', title='History', images=images)