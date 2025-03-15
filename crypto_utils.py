import logging
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


# Konfiguracja logowania
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_keys():
    """Generuje klucz RSA (2048 bitów) i zwraca go jako (private_key, public_key)."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    logging.info("Wygenerowano nowe klucze RSA.")
    
    return private_key.decode(), public_key.decode()


def is_valid_base64(s):
    """Sprawdza, czy string jest poprawnym Base64"""
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def encrypt_message(message, public_key):
    """Szyfruje wiadomość kluczem publicznym."""

    if not message.strip():
        logging.error("Próba zaszyfrowania pustej wiadomości.")
        raise ValueError("Wiadomość do zaszyfrowania nie może być pusta.")

    try:
        recipient_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(recipient_key)
        encrypted_message = cipher.encrypt(message.encode())

        encoded_message = base64.b64encode(encrypted_message).decode()

        logging.info("Wiadomość została poprawnie zaszyfrowana.")
        return encoded_message

    except Exception as e:
        logging.error(f"Błąd podczas szyfrowania: {e}")
        raise ValueError("Błąd podczas szyfrowania wiadomości.")


def decrypt_message(encrypted_message, private_key):
    """Odszyfrowuje wiadomość kluczem prywatnym"""

    if not encrypted_message.strip():
        logging.error("Próba odszyfrowania pustej wiadomości.")
        raise ValueError("Nie można odszyfrować pustej wiadomości.")

    # Sprawdzenie poprawności base64 przed dekodowaniem
    if not is_valid_base64(encrypted_message):
        logging.error("Wiadomość nie jest poprawnym Base64.")
        raise ValueError("Błąd: wiadomość nie jest poprawnie zakodowana w Base64.")

    try:
        private_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(private_key)

        # Dekodowanie Base64
        decoded_message = base64.b64decode(encrypted_message)

        # Odszyfrowanie wiadomości
        decrypted_message = cipher.decrypt(decoded_message).decode().strip()

        logging.info("Wiadomość została poprawnie odszyfrowana.")
        return decrypted_message

    except Exception as e:
        logging.error(f"Błąd podczas odszyfrowywania: {e}")
        raise ValueError("Błąd podczas odszyfrowywania. Sprawdź poprawność wiadomości.")


def sign_message(message: str, private_key: str) -> str:
    """Tworzy podpis cyfrowy wiadomości"""
    
    if not message.strip():
        logging.error("Próba podpisania pustej wiadomości.")
        raise ValueError("Wiadomość do podpisania nie może być pusta.")
    
    try:
        private_key = RSA.import_key(private_key)
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(private_key).sign(h)
        
        logging.info("Wiadomość została podpisana cyfrowo.")
        return base64.b64encode(signature).decode()

    except Exception as e:
        logging.error(f"Błąd podczas podpisywania wiadomości: {e}")
        raise ValueError("Błąd podczas podpisywania wiadomości.")


def verify_signature(message: str, signature: str, public_key: str) -> str:
    """Weryfikuje podpis cyfrowy wiadomości"""
    
    try:
        public_key = RSA.import_key(public_key)
        h = SHA256.new(message.encode())
        decoded_signature = base64.b64decode(signature)
        pkcs1_15.new(public_key).verify(h, decoded_signature)
        
        logging.info("Podpis został poprawnie zweryfikowany.")
        return "Podpis jest poprawny."
    
    except (ValueError, TypeError) as e:
        logging.warning(f"Nieudana weryfikacja podpisu: {e}")
        raise ValueError("Podpis jest nieprawidłowy.")
