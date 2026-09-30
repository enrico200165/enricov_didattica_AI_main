"""Archiviazione a oggetti con l'API S3, su un emulatore locale (moto).

Prima avviare l'emulatore in un altro terminale:
    moto_server -p 5000
Poi, per esempio:
    python archivio_oggetti.py crea
    python archivio_oggetti.py carica esempi\\regolamento.txt documenti/regolamento.txt
    python archivio_oggetti.py carica-cartella esempi
    python archivio_oggetti.py elenco
    python archivio_oggetti.py elenco documenti/
    python archivio_oggetti.py info documenti/regolamento.txt
    python archivio_oggetti.py scarica documenti/regolamento.txt copia.txt
    python archivio_oggetti.py link documenti/regolamento.txt
    python archivio_oggetti.py pubblica esempi/orari.json
    python archivio_oggetti.py cancella documenti/regolamento.txt

Nessun dato esce dal PC: l'emulatore conserva tutto in memoria e lo perde quando viene chiuso.
"""

import mimetypes
import os
import sys

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# indirizzo dell'emulatore; con un servizio reale si userebbe l'indirizzo del fornitore
ENDPOINT = os.environ.get("ENDPOINT_S3", "http://127.0.0.1:5000")
BUCKET = "biblioteca-scuola"
REGIONE = "eu-south-1"      # nome di una regione: con l'emulatore serve solo come dato formale


def client(endpoint=None):
    """Client S3. Le credenziali sono fittizie: l'emulatore accetta qualsiasi valore."""
    return boto3.client(
        "s3",
        endpoint_url=endpoint or ENDPOINT,
        region_name=REGIONE,
        aws_access_key_id="chiave-di-prova",
        aws_secret_access_key="segreto-di-prova",
        # indirizzi nella forma http://host/bucket/chiave invece di http://bucket.host/chiave
        config=Config(s3={"addressing_style": "path"}),
    )


def crea_bucket(s3, nome=BUCKET):
    s3.create_bucket(Bucket=nome, CreateBucketConfiguration={"LocationConstraint": REGIONE})


def carica(s3, percorso, chiave=None, metadati=None, bucket=BUCKET):
    """Carica un file; il tipo di contenuto si ricava dall'estensione. Restituisce la chiave."""
    chiave = chiave or os.path.basename(percorso)
    tipo = mimetypes.guess_type(percorso)[0] or "application/octet-stream"
    with open(percorso, "rb") as f:
        s3.put_object(Bucket=bucket, Key=chiave, Body=f, ContentType=tipo, Metadata=metadati or {})
    return chiave


def carica_cartella(s3, cartella, prefisso="", bucket=BUCKET):
    """Carica tutti i file di una cartella; le sottocartelle diventano parti della chiave."""
    chiavi = []
    for radice, _, file in os.walk(cartella):
        for nome in sorted(file):
            percorso = os.path.join(radice, nome)
            relativo = os.path.relpath(percorso, cartella).replace(os.sep, "/")   # "/" anche su Windows
            chiavi.append(carica(s3, percorso, prefisso + relativo, bucket=bucket))
    return chiavi


def elenco(s3, prefisso="", bucket=BUCKET):
    """(chiave, dimensione in byte) degli oggetti che iniziano con il prefisso."""
    risultato = []
    paginatore = s3.get_paginator("list_objects_v2")      # l'elenco arriva a pagine di al massimo 1000
    for pagina in paginatore.paginate(Bucket=bucket, Prefix=prefisso):
        risultato += [(o["Key"], o["Size"]) for o in pagina.get("Contents", [])]
    return risultato


def info(s3, chiave, bucket=BUCKET):
    """Metadati di un oggetto, senza scaricarne il contenuto (richiesta HEAD)."""
    r = s3.head_object(Bucket=bucket, Key=chiave)
    return {"dimensione": r["ContentLength"], "tipo": r["ContentType"], "etag": r["ETag"].strip('"'),
            "modificato": r["LastModified"].isoformat(), "metadati": r["Metadata"]}


def scarica(s3, chiave, destinazione, bucket=BUCKET):
    s3.download_file(bucket, chiave, destinazione)


def link_temporaneo(s3, chiave, secondi=300, bucket=BUCKET):
    """URL firmato: permette di leggere un oggetto privato per un tempo limitato, senza credenziali."""
    return s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": chiave}, ExpiresIn=secondi)


def rendi_pubblico(s3, chiave, bucket=BUCKET):
    """Permette a chiunque di leggere l'oggetto (ACL public-read). Da usare solo per contenuti pubblici."""
    s3.put_object_acl(Bucket=bucket, Key=chiave, ACL="public-read")


def cancella(s3, chiave, bucket=BUCKET):
    s3.delete_object(Bucket=bucket, Key=chiave)


def main(argomenti):
    if not argomenti:
        print(__doc__)
        return
    s3 = client()
    comando, resto = argomenti[0], argomenti[1:]
    try:
        if comando == "crea":
            crea_bucket(s3)
            print(f"Bucket {BUCKET} creato")
        elif comando == "carica" and resto:
            chiave = carica(s3, resto[0], resto[1] if len(resto) > 1 else None, {"caricato-da": "lab63"})
            print(f"Caricato come {chiave}")
        elif comando == "carica-cartella" and resto:
            for chiave in carica_cartella(s3, resto[0], "esempi/"):
                print("Caricato", chiave)
        elif comando == "elenco":
            oggetti = elenco(s3, resto[0] if resto else "")
            for chiave, dimensione in oggetti:
                print(f"{dimensione:>9}  {chiave}")
            print(f"Oggetti: {len(oggetti)}")
        elif comando == "info" and resto:
            for k, v in info(s3, resto[0]).items():
                print(f"{k:<12}{v}")
        elif comando == "scarica" and len(resto) == 2:
            scarica(s3, *resto)
            print(f"Scaricato in {resto[1]}")
        elif comando == "link" and resto:
            print(link_temporaneo(s3, resto[0]))
        elif comando == "pubblica" and resto:
            rendi_pubblico(s3, resto[0])
            print(f"{resto[0]} ora è leggibile da chiunque: {ENDPOINT}/{BUCKET}/{resto[0]}")
        elif comando == "cancella" and resto:
            cancella(s3, resto[0])
            print(f"Cancellato {resto[0]}")
        else:
            print(__doc__)
    except ClientError as errore:                    # errore restituito dal servizio (codice e messaggio)
        print("Errore del servizio:", errore.response["Error"]["Code"], errore.response["Error"].get("Message", ""))
    except Exception as errore:                      # tipicamente: emulatore non avviato
        print("Impossibile contattare il servizio:", type(errore).__name__, errore)


if __name__ == "__main__":
    main(sys.argv[1:])
