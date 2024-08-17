import os
import sqlite3
import spacy


# Fonction pour indexer les fichiers dans un dossier donné
def index_files(base_path):
    # Connexion à la base de données SQLite (ou création si elle n'existe pas)
    conn = sqlite3.connect('file_index.db')
    c = conn.cursor()
    
    # Création de la table si elle n'existe pas déjà
    c.execute('''CREATE TABLE IF NOT EXISTS files 
                 (name TEXT, path TEXT, description TEXT)''')
    
    # Parcours de tous les fichiers dans le dossier spécifié
    for root, dirs, files in os.walk(base_path):
        for file in files:
            path = os.path.join(root, file)
            description = f"Un fichier trouvé dans {root}"
            c.execute("INSERT INTO files (name, path, description) VALUES (?, ?, ?)", 
                      (file, path, description))
    
    # Sauvegarde et fermeture de la connexion à la base de données
    conn.commit()
    conn.close()

# Appel de la fonction pour indexer un dossier spécifique
index_files('/Users/backoffice')  # Remplacez par le chemin du dossier à indexer





# Chargement du modèle NLP
nlp = spacy.load('en_core_web_sm')

# Fonction pour traiter la requête de l'utilisateur
def process_query(query):
    doc = nlp(query)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return tokens

# Fonction pour rechercher les fichiers dans la base de données
def search_files(query):
    tokens = process_query(query)
    conn = sqlite3.connect('file_index.db')
    c = conn.cursor()
    
    for token in tokens:
        c.execute("SELECT * FROM files WHERE name LIKE ? OR description LIKE ?", 
                  ('%' + token + '%', '%' + token + '%'))
        results = c.fetchall()
        if results:
            for result in results:
                print("Fichier trouvé:", result)
    
    conn.close()

# Prendre la requête de l'utilisateur
def take_input():
    query = input("Que cherchez-vous ? ")
    search_files(query)

# Lancer la recherche en prenant la requête utilisateur
take_input()
