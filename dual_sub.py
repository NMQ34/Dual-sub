import pysubs2
from deep_translator import GoogleTranslator
import glob
import time
import sys
import os

def process_all():
    start_time = time.time()
    
    # 1. Configuration des dossiers
    source_dir = "source"
    out_dir = "STREMIO_READY"
    
    # Le script crée les dossiers automatiquement s'ils n'existent pas
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    
    # 2. Chercher tous les fichiers dans le dossier "source"
    extensions = ('*.srt', '*.vtt', '*.txt')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(source_dir, ext)))
        
    if not files:
        print(f"Aucun fichier a traduire !")
        print(f"-> Glisse tes sous-titres originaux dans le dossier '{source_dir}' et relance.")
        return
        
    print(f"--- Lancement du mode Usine : {len(files)} fichier(s) detecte(s) ---")
    translator = GoogleTranslator(source='en', target='fr')
    
    # 3. Boucle sur chaque fichier trouve
    for input_file in files:
        base_name = os.path.basename(input_file)
        print(f"\n[TRAITEMENT] : {base_name}")
        
        try:
            subs = pysubs2.load(input_file, encoding="utf-8")
        except Exception as e:
            print(f"Erreur de lecture sur {base_name} : {e}")
            continue # On passe au fichier suivant en cas d'erreur

        # Nettoyage Extreme anti-plantage
        for i in range(len(subs) - 1, -1, -1):
            clean = subs[i].plaintext.strip()
            if not clean or any(x in clean for x in ["NOTE", "WEBVTT", "OpenSubtitles", "=&gt;"]):
                del subs[i] 

        texts = [line.plaintext.strip().replace('\n', ' ') for line in subs]

        # Batching & Traduction
        batch_size = 40
        all_translated = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            combined = " ||| ".join(batch)
            
            try:
                res = translator.translate(combined)
                trans_list = [t.strip() for t in res.split('|||')]
                
                if len(trans_list) == len(batch):
                    all_translated.extend(trans_list)
                else:
                    safe_res = translator.translate_batch(batch)
                    all_translated.extend(safe_res)
            except Exception as e:
                print(f"\nErreur reseau : {e}")
                all_translated.extend(batch)
                
            # Barre de progression
            percent = int((len(all_translated) / len(texts)) * 100)
            bar = '#' * (percent // 5) + '.' * (20 - (percent // 5))
            sys.stdout.write(f"\rProgression : [{bar}] {percent}% ({len(all_translated)}/{len(texts)})")
            sys.stdout.flush()

        # Formatage "Pur" pour Stremio
        for idx, fr_text in enumerate(all_translated):
            subs[idx].text = f"{texts[idx]}\\N{fr_text}"

        # 4. Nom dynamique et sauvegarde dans le dossier STREMIO_READY
        name_without_ext = os.path.splitext(base_name)[0]
        output_name = os.path.join(out_dir, f"{name_without_ext}_DUAL.srt")
        
        subs.save(output_name, format_="srt", encoding="utf-8")
        print(f"\n-> Sauvegarde reussie : {output_name}")

    print(f"\n\nSUCCES TOTAL ! {len(files)} fichier(s) traite(s) en {int(time.time() - start_time)} secondes.")

if __name__ == "__main__":
    process_all()