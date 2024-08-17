import os
import spacy
import tkinter as tk
from tkinter import ttk
import threading
import webbrowser

# Chargement du modèle NLP
nlp = spacy.load('en_core_web_sm')

# Fonction pour traiter la requête de l'utilisateur
def process_query(query):
    doc = nlp(query)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return tokens

# Fonction pour rechercher les fichiers et dossiers sur la machine
def search_files(query, base_path):
    tokens = process_query(query)
    results = []
    for root, dirs, files in os.walk(base_path):
        for name in dirs + files:
            for token in tokens:
                if token.lower() in name.lower():
                    path = os.path.join(root, name)
                    description = f"Un {'dossier' if os.path.isdir(path) else 'fichier'} trouvé dans {root}"
                    results.append((name, path, description))
                    break
    return results

# Fonction pour gérer la recherche et afficher les résultats
def perform_search():
    query = entry.get()
    log_text.pack(fill=tk.X)  # Afficher la zone des logs
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Recherche en cours...\n", "log")

    def search_and_display():
        results = search_files(query, '/Users/backoffice')  # Remplace par le chemin de base

        result_text.delete(1.0, tk.END)
        log_text.pack_forget()  # Cacher la zone des logs après la recherche

        if results:
            for name, path, description in results:
                result_text.insert(tk.END, f"Nom: ", ("link_name", path))
                result_text.insert(tk.END, f"{name}\n", ("link_name", path))
                result_text.insert(tk.END, f"Chemin: {path}\nDescription: {description}\n\n", ("link", path))
        else:
            result_text.insert(tk.END, "Aucun résultat trouvé.")

    threading.Thread(target=search_and_display, daemon=True).start()

# Fonction pour ouvrir le dossier ou fichier correspondant au chemin cliqué
def open_path(event):
    widget = event.widget
    index = widget.index("@%s,%s" % (event.x, event.y))
    start, end = widget.tag_prevrange("link", index)
    path = widget.get(start, end)
    if os.path.exists(path):
        webbrowser.open('file://' + os.path.dirname(path))

# Fonction pour ouvrir le dossier ou fichier correspondant au nom cliqué
def open_name(event):
    widget = event.widget
    index = widget.index("@%s,%s" % (event.x, event.y))
    start, end = widget.tag_prevrange("link_name", index)
    path = widget.get(start, end)
    if os.path.exists(path):
        webbrowser.open('file://' + os.path.dirname(path))

# Fonction pour lancer la fenêtre Tkinter
def start_gui():
    global entry, log_text, result_text

    # Création de la fenêtre Tkinter
    root = tk.Tk()
    root.title("Recherche de fichiers")

    # Création du cadre principal
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Création du cadre pour la recherche
    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill=tk.X, padx=10, pady=10)

    # Label et champ de saisie pour la requête
    tk.Label(search_frame, text="Entrez le nom ou la description :").pack(side=tk.LEFT)
    entry = tk.Entry(search_frame, width=50)
    entry.pack(side=tk.LEFT, padx=5)

    # Bouton pour lancer la recherche
    tk.Button(search_frame, text="Rechercher", command=perform_search).pack(side=tk.LEFT)

    # Création du cadre pour les logs
    log_frame = tk.Frame(main_frame)
    log_frame.pack(fill=tk.X, padx=10, pady=10)
    log_text = tk.Text(log_frame, wrap=tk.WORD, height=2, fg="green")
    log_text.pack(fill=tk.X, expand=True)
    log_text.tag_config("log", foreground="green")

    # Création du cadre pour les résultats
    result_frame = tk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Création d'un widget Text pour afficher les résultats
    result_text = tk.Text(result_frame, wrap=tk.WORD, fg="green")
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    result_text.bind("<Button-1>", open_name)
    result_text.bind("<Button-1>", open_path, add="+")

    # Ajout d'une barre de défilement verticale
    scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)

    # Assurez-vous que la fenêtre est réactive
    root.update_idletasks()
    root.minsize(root.winfo_width(), root.winfo_height())

    # Lancer la fenêtre Tkinter
    root.mainloop()

# Fonction principale pour démarrer l'application
def main():
    # Lancer l'interface graphique Tkinter sur le thread principal
    start_gui()

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
