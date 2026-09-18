import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Crée le dossier pour les images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clé GROQ lue depuis Render (pas écrite ici) - c'est ce qui bloquait GitHub
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

livres = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global livres
    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        auteur = request.form.get('auteur', '').strip()
        photo = request.files.get('photo')
        filename = None
        
        if photo and photo.filename != '':
            filename = photo.filename
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if titre:
            livres.append({"titre": titre, "auteur": auteur, "photo": filename})
        return redirect(url_for('index'))
    
    return render_template('index.html', livres=livres)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)