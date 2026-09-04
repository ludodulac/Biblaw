# Biblaw

Interface web légère pour charger un PDF, le consulter et en extraire le texte directement dans le navigateur.

## Utilisation

1. Ouvrez `index.html` dans un navigateur moderne, ou servez le dossier avec un serveur statique :
   ```bash
   python3 -m http.server 8000
   ```
2. Ouvrez http://localhost:8000.
3. Déposez un PDF ou choisissez-le depuis votre ordinateur.

Le PDF reste local : il n’est envoyé vers aucun serveur. L’application utilise PDF.js pour l’affichage et l’extraction du texte.

## Limites

- Taille maximale : 50 Mo.
- Les PDF scannés sans couche texte nécessiteront ultérieurement un module OCR.
