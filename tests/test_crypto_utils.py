import pytest
from crypto_utils import (generate_keys,
                          encrypt_message,
                          decrypt_message,
                          sign_message,
                          verify_signature)


# Testowanie dla pozytywnych scenariuszy####


@pytest.fixture
def keys():
    """Fixture generująca klucze RSA dla testów"""
    private_key, public_key = generate_keys()
    return private_key, public_key


def test_generate_keys():
    """Test sprawdzający, czy klucze są poprawnie generowane"""
    private_key, public_key = generate_keys()
    print("\n[INFO] Wygenerowany klucz prywatny:", private_key[:50])
    print("[INFO] Wygenerowany klucz publiczny:", public_key[:50])
    assert private_key.startswith("-----BEGIN RSA PRIVATE KEY-----")
    assert public_key.startswith("-----BEGIN PUBLIC KEY-----")


def test_encrypt_decrypt(keys):
    """Test poprawności szyfrowania i odszyfrowania"""
    private_key, public_key = keys
    message = "Testowa wiadomość"
    encrypted_message = encrypt_message(message, public_key)
    print("\n[INFO] Zaszyfrowana wiadomość:", encrypted_message[:50])
    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("[INFO] Odszyfrowana wiadomość:", decrypted_message)
    assert decrypted_message == message


def test_sign_verify(keys):
    """Test poprawności podpisywania i weryfikacji podpisu"""
    private_key, public_key = keys
    message = "Testowa wiadomość do podpisania"
    signature = sign_message(message, private_key)
    print("\n[INFO] Podpis cyfrowy:", signature[:50])
    verification_result = verify_signature(message, signature, public_key)
    print("[INFO] Wynik weryfikacji podpisu:", verification_result)
    assert verification_result == "Podpis jest poprawny."


def test_invalid_signature(keys):
    """Test weryfikacji podpisu, gdy wiadomość została zmieniona"""
    private_key, public_key = keys
    message = "Testowa wiadomość"
    wrong_message = "Inna wiadomość"
    signature = sign_message(message, private_key)
    print("\n[INFO] Fałszywa wiadomość:", wrong_message)
    print("[INFO] Prawidłowy podpis:", signature[:50])

    with pytest.raises(ValueError, match="Podpis jest nieprawidłowy."):
        verify_signature(wrong_message, signature, public_key)


# Testowanie dla negatywnych scenariuszy


def test_encrypt_with_invalid_key():
    """Test próby szyfrowania przy użyciu błędnego klucza"""
    invalid_key = "-----BEGIN PUBLIC KEY-----\nINVALIDKEY"
    with pytest.raises(ValueError):
        encrypt_message("Test", invalid_key)


def test_decrypt_with_invalid_key(keys):
    """Test odszyfrowania zaszyfrowanej wiadomości błędnym kluczem"""
    private_key, public_key = keys
    encrypted_message = encrypt_message("Test", public_key)

    invalid_private_key = "-----BEGIN RSA PRIVATE KEY-----\nINVALIDKEY"
    with pytest.raises(ValueError):
        decrypt_message(encrypted_message, invalid_private_key)


def test_verify_invalid_signature(keys):
    """Test weryfikacji podpisu z niepoprawnym kluczem"""
    private_key, public_key = keys
    message = "Test"
    signature = sign_message(message, private_key)

    invalid_public_key = "-----BEGIN PUBLIC KEY-----\nINVALIDKEY"
    with pytest.raises(ValueError):
        verify_signature(message, signature, invalid_public_key)


def test_sign_empty_message(keys):
    """Test podpisywania pustej wiadomości"""
    private_key, public_key = keys
    with pytest.raises(ValueError):
        sign_message("", private_key)


def test_decrypt_invalid_format(keys):
    """Test odszyfrowywania wiadomości w złym formacie"""
    private_key, _ = keys
    invalid_encrypted_message = "not_base64_encoded_data"
    with pytest.raises(ValueError):
        decrypt_message(invalid_encrypted_message, private_key)
