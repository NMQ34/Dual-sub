# 🎬 Stremio Dual Subtitles

Un script Python ultra-rapide pour transformer vos sous-titres anglais en **sous-titres bilingues (Anglais/Français)** optimisés pour **Stremio**.

## ✨ Caractéristiques
- **Vitesse Éclair** : Traduction par lots (batching) via Google Translate.
- **Nettoyage Auto** : Supprime les pubs (OpenSubtitles), les balises WEBVTT et les métadonnées qui font planter Stremio.
- **Organisation** : Gestion automatique des dossiers source et sortie.

## 🚀 Installation

1. Clonez ce dépôt.
2. Assurez-vous d'avoir Python 3.10+ installé.
3. Installez les dépendances :
   ```bash
   pip install deep-translator pysubs2

🛠 Utilisation

    Placez vos fichiers .txt, .srt ou .vtt anglais dans le dossier /source.

    Double-cliquez sur GO.bat.

    Récupérez vos fichiers traduits dans /STREMIO_READY.

    Glissez-déposez le fichier final dans Stremio pendant la lecture.

⚙️ Structure du Projet

    dual_sub.py : Le script de traduction.

    GO.bat : Le lanceur Windows.

    /source : Dossier d'entrée.

    /STREMIO_READY : Dossier de sortie.

Fait avec amour pour la communauté Stremio.