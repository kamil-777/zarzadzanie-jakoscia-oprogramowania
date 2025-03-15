import os
import logging
from crypto_utils import generate_keys

# Konfiguracja logowania
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Katalog do przechowywania kluczy
KEYS_DIR = "keys"
os.makedirs(KEYS_DIR, exist_ok=True)

# Lista użytkowników
users = {"Kamil", "Sebastian", "Hubert"}

# Słownik do przechowywania kluczy w pamięci
user_keys = {}


def get_key_path(username, key_type):
    """Zwraca ścieżkę do pliku z kluczem użytkownika."""
    return os.path.join(KEYS_DIR, f"{username}_{key_type}.pem")


for user in users:
    private_key_path = get_key_path(user, "private")
    public_key_path = get_key_path(user, "public")

    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        with open(private_key_path, "rb") as priv_file:
            private_key = priv_file.read().decode()
        with open(public_key_path, "rb") as pub_file:
            public_key = pub_file.read().decode()
        logging.info(f"Załadowano klucze dla użytkownika: {user}")
    else:
        private_key, public_key = generate_keys()
        with open(private_key_path, "wb") as priv_file:
            priv_file.write(private_key.encode())
        with open(public_key_path, "wb") as pub_file:
            pub_file.write(public_key.encode())
        logging.info(f"Wygenerowano nowe klucze dla użytkownika: {user}")

    # Przechowywanie kluczy w pamięci
    user_keys[user] = {"private_key": private_key, "public_key": public_key}

logging.info("Wszystkie klucze użytkowników zostały poprawnie załadowane.")
