
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    course = db.relationship('Course', backref=db.backref('cart_items', lazy=True))

## Suivre les cours Modeles ---------------------------------------------------------------------------------------------------------- 
# Mise à jour de la méthode `update_progress` dans le modèle `PurchasedCourse`
class PurchasedCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    progress = db.Column(db.Float, default=0.0)  # Suivi de l'avancement, de 0.0 à 100.0

    user = db.relationship('User', backref=db.backref('purchased_courses', lazy=True))
    course = db.relationship('Course', backref=db.backref('purchased_courses', lazy=True))

    def update_progress(self):
        # Compter les chapitres complétés
        completed_chapters = CourseChapterProgress.query.filter_by(
            purchased_course_id=self.id, completed=True
        ).count()

        # Calculer la progression globale
        total_chapters = len(self.course.chapters)
        if total_chapters > 0:
            self.progress = (completed_chapters / total_chapters) * 100
        else:
            self.progress = 0.0

        db.session.commit()
        

    
class CourseChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)  # Chapitre 1, 2, etc.
    title = db.Column(db.String(150), nullable=False)  # Le titre du chapitre
    content = db.Column(db.Text, nullable=False)  # Le contenu du chapitre (peut être fictif)
    
    course = db.relationship('Course', backref=db.backref('chapters', lazy=True))

class CourseChapterProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchased_course_id = db.Column(db.Integer, db.ForeignKey('purchased_course.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('course_chapter.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    purchased_course = db.relationship('PurchasedCourse', backref=db.backref('chapter_progress', lazy=True))
    chapter = db.relationship('CourseChapter', backref=db.backref('progress', lazy=True))

# ----------------------------------------------------------------------------------------------------------