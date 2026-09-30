# Dockerfile per il servizio della biblioteca (lezione 5.3), da leggere e commentare in classe.
# Costruzione dell'immagine:   docker build -t biblioteca:1.0 .
# Avvio di un container:       docker run -p 8000:8000 biblioteca:1.0

# 1. Immagine di partenza: un sistema Linux minimo con Python 3.12 già installato
FROM python:3.12-slim

# 2. Cartella di lavoro dentro l'immagine: i comandi successivi partono da qui
WORKDIR /app

# 3. Copia dei file dell'applicazione dalla cartella del progetto all'immagine
COPY servizio_biblioteca.py .
COPY static/ static/
COPY biblioteca.db .

# 4. Comando eseguito durante la costruzione: crea un utente senza privilegi
#    e gli assegna i file (il servizio non deve girare come amministratore)
RUN useradd --create-home servizio && chown -R servizio /app

# 5. Da qui in poi i comandi, e il servizio, girano con l'utente "servizio"
USER servizio

# 6. Documenta la porta su cui il servizio ascolta dentro il container
EXPOSE 8000

# 7. Comando avviato quando parte un container da questa immagine
CMD ["python", "servizio_biblioteca.py", "8000"]
