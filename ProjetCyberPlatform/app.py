from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, User, Cart, Course, CourseChapter, CourseChapterProgress, PurchasedCourse

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
migrate = Migrate(app, db)


## --------------------------------- DEBUT ROUTES INSCRIPTIONS LOGIN ---------------------------------
@app.route('/')
def home():
    if 'user_id' in session:
        courses = Course.query.all()
        return render_template('dashboard.html', courses=courses)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Vérifier que le mot de passe n'est pas vide
        if not password:
            flash('Password is required!', 'danger')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérification que les champs ne sont pas vides
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))

        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


## --------------------------------- FIN ROUTES INSCRIPTIONS LOGIN ---------------------------------


## --------------------------------- DEBUT ROUTES COURSE CARDS AND DETAIL ---------------------------------
# Détail d'un cours
@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

# Fonction pour ajouter des cours et les chapitre de chaque cours 
def add_initial_courses():
    # Liste des cours à ajouter
    courses = [
        {
            'title': "Introduction to Cybersecurity",
            'description': "Learn the basics of cybersecurity, including threat models, encryption, and network security.",
            'image_url': "https://bbb-main.blr1.digitaloceanspaces.com/uploads/course/introduction-to-cybersecurity-1720530832069.jpeg",
            'price': 49.99,
            'chapters': [
                {'chapter_number': 1, 'title': 'Introduction to Cybersecurity', 'content': 'Overview of Cybersecurity concepts.'},
                {'chapter_number': 2, 'title': 'Threat Models', 'content': 'Understanding different types of threats.'},
                {'chapter_number': 3, 'title': 'Encryption Basics', 'content': 'Introduction to encryption techniques.'}
            ]
        },
        {
            'title': "Advanced Web Security",
            'description': "Dive deep into advanced topics like XSS, SQL injection, and CSRF.",
            'image_url': "https://i0.wp.com/www.wattlecorp.com/wp-content/uploads/2024/04/web-application-vulnerabilities.webp?fit=1024%2C597&ssl=1",
            'price': 69.99,
            'chapters': [
                {'chapter_number': 1, 'title': 'Advanced XSS', 'content': 'Cross-Site Scripting vulnerabilities and mitigation.'},
                {'chapter_number': 2, 'title': 'SQL Injection Attacks', 'content': 'How SQL injection works and how to prevent it.'},
                {'chapter_number': 3, 'title': 'CSRF Attacks', 'content': 'Understanding Cross-Site Request Forgery.'}
            ]
        },
        {
            'title': "Cryptography Basics",
            'description': "An introduction to cryptography, including encryption, hashing, and digital signatures.",
            'image_url': "https://online.york.ac.uk/wp-content/uploads/2023/10/Cryptography.jpg",
            'price': 39.99,
            'chapters': [
                {'chapter_number': 1, 'title': 'Introduction to Cryptography', 'content': 'The basics of cryptography and its history.'},
                {'chapter_number': 2, 'title': 'Hashing and Encryption', 'content': 'Understanding the difference between hashing and encryption.'},
                {'chapter_number': 3, 'title': 'Digital Signatures', 'content': 'How digital signatures work and their use cases.'}
            ]
        },
        {
            'title': "Network Security Fundamentals",
            'description': "Understand the basics of securing computer networks, firewalls, and VPNs.",
            'image_url': "https://online.york.ac.uk/wp-content/uploads/2023/08/Netwrok-Security.jpg",
            'price': 59.99,
            'chapters': [
                {'chapter_number': 1, 'title': 'Network Security Basics', 'content': 'Introduction to securing networks.'},
                {'chapter_number': 2, 'title': 'Firewalls and VPNs', 'content': 'Setting up firewalls and using VPNs for security.'},
                {'chapter_number': 3, 'title': 'Intrusion Detection Systems', 'content': 'Monitoring and responding to intrusions.'}
            ]
        }
    ]

    # Ajouter les cours et leurs chapitres
    for course_data in courses:
        existing_course = Course.query.filter_by(title=course_data['title']).first()
        if not existing_course:
            course = Course(
                title=course_data['title'],
                description=course_data['description'],
                image_url=course_data['image_url'],
                price=course_data['price']
            )
            db.session.add(course)
            db.session.commit()  # Commit pour obtenir l'id du cours

            # Ajouter les chapitres pour ce cours
            for chapter_data in course_data['chapters']:
                chapter = CourseChapter(
                    course_id=course.id,
                    chapter_number=chapter_data['chapter_number'],
                    title=chapter_data['title'],
                    content=chapter_data['content']
                )
                db.session.add(chapter)

            db.session.commit()  # Commit après avoir ajouté les chapitres

    print("Initial courses and chapters added to the database.")
    
    
## --------------------------------- FIN ROUTES COURSE CARDS AND DETAIL ---------------------------------



## --------------------------------- DEBUT ROUTES CART ---------------------------------
        
@app.route('/add_to_cart/<int:course_id>', methods=['POST'])
def add_to_cart(course_id):
    if 'user_id' not in session:
        flash('You need to be logged in to add courses to your cart.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    course = Course.query.get_or_404(course_id)

    # Vérifier si le cours est déjà dans le panier de l'utilisateur
    existing_cart_item = Cart.query.filter_by(user_id=user.id, course_id=course.id).first()
    if existing_cart_item:
        flash('This course is already in your cart.', 'warning')
    else:
        # Ajouter le cours au panier
        new_cart_item = Cart(user_id=user.id, course_id=course.id)
        db.session.add(new_cart_item)
        db.session.commit()
        flash('Course successfully added to your cart!', 'success')

    return redirect(url_for('course_detail', course_id=course.id))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('You need to be logged in to view your cart.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user is None:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    cart_items = Cart.query.filter_by(user_id=user.id).all()

    # Calcul du total en accédant au prix du cours via la relation
    total_price = sum(item.course.price for item in cart_items)  # Correction ici

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in session:
        flash('You need to be logged in to remove courses from your cart.', 'danger')
        return redirect(url_for('login'))

    # Trouve l'élément de panier correspondant à l'ID
    cart_item = Cart.query.get_or_404(cart_item_id)

    # Vérifie que l'utilisateur est bien celui qui a ajouté cet élément
    if cart_item.user_id != session['user_id']:
        flash('You cannot remove items from another user\'s cart.', 'danger')
        return redirect(url_for('cart'))

    # Supprime l'élément du panier
    db.session.delete(cart_item)
    db.session.commit()
    flash('Course removed from your cart!', 'success')

    return redirect(url_for('cart'))

## --------------------------------- FIN ROUTES CART ---------------------------------

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

## --------------------------------- DEBUT ROUTES POUR LES COURS ACHETÉS ---------------------------------

@app.route('/buy_courses', methods=['POST'])
def buy_courses():
    if 'user_id' not in session:
        flash('You need to be logged in to purchase courses.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    # Récupérer tous les cours dans le panier de l'utilisateur
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    for cart_item in cart_items:
        course = Course.query.get(cart_item.course_id)
        
        # Vérifier si le cours est déjà acheté
        purchased_course = PurchasedCourse.query.filter_by(user_id=user.id, course_id=course.id).first()
        if not purchased_course:
            # Ajouter le cours aux cours achetés
            new_purchased_course = PurchasedCourse(user_id=user.id, course_id=course.id)
            db.session.add(new_purchased_course)

        # Supprimer le cours du panier
        db.session.delete(cart_item)
    
    db.session.commit()

    flash('Courses successfully purchased!', 'success')
    return redirect(url_for('my_courses'))


@app.route('/my_courses')
def my_courses():
    if 'user_id' not in session:
        flash('You need to be logged in to view your purchased courses.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    purchased_courses = PurchasedCourse.query.filter_by(user_id=user.id).all()

    for purchased_course in purchased_courses:
        purchased_course.update_progress()  # Recalcule la progression
        db.session.refresh(purchased_course)  # Assure que les données sont à jour
        
        
    return render_template('my_courses.html', purchased_courses=purchased_courses)

@app.route('/generate_certificate/<int:purchased_course_id>', methods=['POST'])
def generate_certificate(purchased_course_id):
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        flash('You need to be logged in to generate a certificate.', 'danger')
        return redirect(url_for('login'))

    # Récupérer le cours acheté
    purchased_course = PurchasedCourse.query.get_or_404(purchased_course_id)

    # Vérifier que l'utilisateur est bien propriétaire du cours
    if purchased_course.user_id != session['user_id']:
        flash('You do not have access to this course.', 'danger')
        return redirect(url_for('my_courses'))

    # Vérifier si la progression est de 100%
    if purchased_course.progress < 100:
        flash('You need to complete the course 100% to download the certificate.', 'warning')
        return redirect(url_for('my_courses'))

    # Simuler le lien du certificat
    certificate_link = "https://example.com/certificate"
    flash(f'Here is your certificate link: {certificate_link}', 'success')
    return redirect(url_for('my_courses'))



@app.route('/course_progress/<int:purchased_course_id>/<int:chapter_number>')
def course_progress(purchased_course_id, chapter_number):
    if 'user_id' not in session:
        flash('You need to be logged in to access your course.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    purchased_course = PurchasedCourse.query.get_or_404(purchased_course_id)
    chapter = CourseChapter.query.filter_by(course_id=purchased_course.course_id, chapter_number=chapter_number).first_or_404()

    # Vérifier si le chapitre est déjà complété
    chapter_progress = CourseChapterProgress.query.filter_by(purchased_course_id=purchased_course.id, chapter_id=chapter.id).first()
    if not chapter_progress:
        chapter_progress = CourseChapterProgress(purchased_course_id=purchased_course.id, chapter_id=chapter.id)
        db.session.add(chapter_progress)

    # Afficher la page du chapitre
    return render_template('chapter.html', purchased_course=purchased_course, chapter=chapter, chapter_progress=chapter_progress)


@app.route('/mark_chapter_completed/<int:purchased_course_id>/<int:chapter_id>', methods=['POST'])
def mark_chapter_completed(purchased_course_id, chapter_id):
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        flash('You need to be logged in to mark chapters as completed.', 'danger')
        return redirect(url_for('login'))

    # Récupérer l'utilisateur à partir de la session
    user = User.query.get(session['user_id'])
    purchased_course = PurchasedCourse.query.get_or_404(purchased_course_id)
    chapter = CourseChapter.query.get_or_404(chapter_id)

    # Vérifier que l'utilisateur a bien acheté ce cours
    if purchased_course.user_id != user.id:
        flash('You do not have access to this course.', 'danger')
        return redirect(url_for('my_courses'))

    # Marquer le chapitre comme terminé
    chapter_progress = CourseChapterProgress.query.filter_by(
        purchased_course_id=purchased_course.id,
        chapter_id=chapter.id
    ).first()

    if not chapter_progress:
        # Ajouter un nouveau chapitre complété si inexistant
        chapter_progress = CourseChapterProgress(
            purchased_course_id=purchased_course.id,
            chapter_id=chapter.id,
            completed=True
        )
        db.session.add(chapter_progress)
    else:
        # Mettre à jour le statut si déjà existant
        chapter_progress.completed = True

    db.session.commit()

    # Mettre à jour la progression globale du cours
    purchased_course.update_progress()

    # Vérifier si c'est le dernier chapitre
    total_chapters = len(purchased_course.course.chapters)
    if chapter.chapter_number == total_chapters:
        flash('Congratulations! You have completed this course.', 'success')
        return redirect(url_for('my_courses'))  # Retourne à la liste des cours

    # Sinon, redirige vers le chapitre suivant
    return redirect(url_for('course_progress', purchased_course_id=purchased_course.id, chapter_number=chapter.chapter_number + 1))

## --------------------------------- DEBUT ROUTES POUR LES COURS ACHETÉS ---------------------------------


# Bootstrap integration in templates
@app.context_processor
def inject_bootstrap():
    return dict(bootstrap_css="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css")
        

# Appeler la fonction initialize_app() dans un endroit plus approprié
def initialize_app(app):
    with app.app_context():
        db.create_all()
        if Course.query.count() == 0:
            add_initial_courses()

initialize_app(app)

if __name__ == '__main__':
    app.run(debug=True)



    

