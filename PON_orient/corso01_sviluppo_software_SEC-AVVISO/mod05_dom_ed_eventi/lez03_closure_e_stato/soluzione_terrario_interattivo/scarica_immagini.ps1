# Scarica le 14 immagini delle piante (repository Microsoft Web-Dev-For-Beginners, licenza MIT)
# nella sottocartella images. Eseguire dalla cartella del progetto: .\scarica_immagini.ps1
# Se Windows blocca l'esecuzione degli script (criterio di esecuzione predefinito), copiare
# le righe seguenti e incollarle direttamente nel terminale PowerShell.
New-Item -ItemType Directory -Force -Path images | Out-Null
1..14 | ForEach-Object {
  Invoke-WebRequest "https://raw.githubusercontent.com/microsoft/Web-Dev-For-Beginners/main/3-terrarium/solution/images/plant$_.png" -OutFile "images/plant$_.png"
}
