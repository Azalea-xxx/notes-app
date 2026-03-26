from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='Другое')
    date = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', 'Другое')
        date = datetime.now().strftime('%Y-%m-%d')
        
        note = Note(title=title, content=content, category=category, date=date)
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get_or_404(id)
    
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.category = request.form.get('category', 'Другое')
        db.session.commit()
        return redirect('/')
    
    return render_template('edit.html', note=note)

@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)