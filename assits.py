import os
import spacy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import webbrowser

# Chargement du modèle NLP
nlp = spacy.load('en_core_web_sm')

# Fonction pour traiter la requête de l'utilisateur
def process_query(query):
    doc = nlp(query)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return tokens

# Fonction pour rechercher les fichiers directement sur la machine
def search_files_on_disk(base_path, query):
    tokens = process_query(query)
    results = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            for token in tokens:
                if token.lower() in file.lower():
                    results.append((file, os.path.join(root, file)))
                    break  # Arrêter après le premier token trouvé

    return results

# Fonction pour gérer la recherche et afficher les résultats
def perform_search():
    query = entry.get()
    result_text.delete(1.0, tk.END)
    log_text.delete(1.0, tk.END)
    
    log_text.insert(tk.END, "Démarrage de la recherche...\n", "log")
    
    results = search_files_on_disk('/Users/backoffice', query)

    if results:
        log_text.insert(tk.END, "Recherche terminée. Affichage des résultats.\n", "log")
        for result in results:
            result_text.insert(tk.END, f"{result[0]}\n", "link")
            result_text.tag_bind("link", "<Button-1>", lambda e, path=result[1]: open_file_location(path))
    else:
        log_text.insert(tk.END, "Aucun résultat trouvé.\n", "log")
        result_text.insert(tk.END, "Aucun résultat trouvé.")

    root.update_idletasks()

# Fonction pour ouvrir l'emplacement du fichier
def open_file_location(path):
    try:
        webbrowser.open(f'file://{path}')
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'emplacement du fichier: {e}")

# Fonction pour lancer la fenêtre Tkinter
def start_gui():
    global root, entry, result_text, log_text

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
    log_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    # Création d'un widget Text pour afficher les logs
    log_text = tk.Text(log_frame, height=5, wrap=tk.WORD, fg='green')
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Création du cadre pour les résultats
    result_frame = tk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Création d'un widget Text pour afficher les résultats
    result_text = tk.Text(result_frame, wrap=tk.WORD, fg='blue')
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Ajout d'une barre de défilement verticale pour les résultats
    scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)

    # Assurez-vous que la fenêtre est réactive
    root.update_idletasks()
    root.minsize(root.winfo_width(), root.winfo_height())

    # Configurer les tags pour les liens et les logs
    result_text.tag_configure("link", foreground="blue", underline=True)
    log_text.tag_configure("log", foreground="green")

    # Lancer la fenêtre Tkinter
    root.mainloop()

# Fonction principale pour démarrer l'application
def main():
    # Lancer l'interface graphique Tkinter sur le thread principal
    start_gui()

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
