"""Confronto tra hash veloce senza sale e derivazione lenta con sale (lezione 2.2)."""
import hashlib
import secrets
import time

from archivio_password import ITERAZIONI, deriva

password = "estate2024"

print("1. SHA-256 senza sale: la stessa password dà sempre lo stesso valore")
for utente in ("anna", "bruno"):
    print(f"   {utente}: {hashlib.sha256(password.encode()).hexdigest()}")

print("2. Con un sale casuale diverso per ogni utente i valori sono diversi")
for utente in ("anna", "bruno"):
    sale = secrets.token_bytes(16)
    print(f"   {utente}: sale {sale.hex()[:12]}...  valore {deriva(password, sale).hex()[:24]}...")

print("3. Costo di un singolo calcolo")
inizio = time.perf_counter()
for _ in range(100_000):
    hashlib.sha256(password.encode()).digest()
t_sha = (time.perf_counter() - inizio) / 100_000
inizio = time.perf_counter()
deriva(password, secrets.token_bytes(16))
t_pbkdf2 = time.perf_counter() - inizio
print(f"   SHA-256:                      {t_sha * 1e6:.2f} microsecondi")
print(f"   PBKDF2 con {ITERAZIONI} iterazioni: {t_pbkdf2 * 1000:.0f} millisecondi")
print(f"   rapporto: circa {t_pbkdf2 / t_sha:,.0f} volte più lento".replace(",", "."))
