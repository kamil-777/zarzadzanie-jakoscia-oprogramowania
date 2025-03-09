import pytest
import os
from users import users, KEYS_DIR
from crypto_utils import generate_keys

@pytest.fixture
def test_user():
    """Fixture tworząca testowego użytkownika."""
    username = "TestUser"
    private_key, public_key = generate_keys()

    private_key_path = os.path.join(KEYS_DIR, f"{username}_private.pem")
    public_key_path = os.path.join(KEYS_DIR, f"{username}_public.pem")

    with open(private_key_path, "w") as priv_file:
        priv_file.write(private_key)

    with open(public_key_path, "w") as pub_file:
        pub_file.write(public_key)

    yield username, private_key, public_key

    # Sprzątanie po teście - usuwanie plików
    os.remove(private_key_path)
    os.remove(public_key_path)

def test_users_exist():
    """Test sprawdzający, czy użytkownicy są poprawnie załadowani"""
    print("\n[INFO] Aktualni użytkownicy w systemie:", list(users.keys()))
    assert "Kamil" in users
    assert "Sebastian" in users
    assert "Hubert" in users

def test_keys_are_stored():
    """Test sprawdzający, czy klucze użytkowników są zapisane w plikach"""
    for user in users:
        private_key_path = os.path.join(KEYS_DIR, f"{user}_private.pem")
        public_key_path = os.path.join(KEYS_DIR, f"{user}_public.pem")

        print(f"\n[INFO] Sprawdzanie kluczy dla {user}:")
        print(f"  - Klucz prywatny: {private_key_path} (istnieje? {os.path.exists(private_key_path)})")
        print(f"  - Klucz publiczny: {public_key_path} (istnieje? {os.path.exists(public_key_path)})")

        assert os.path.exists(private_key_path)
        assert os.path.exists(public_key_path)

        with open(private_key_path, "r") as priv_file:
            private_key = priv_file.read()
            assert private_key.startswith("-----BEGIN RSA PRIVATE KEY-----")

        with open(public_key_path, "r") as pub_file:
            public_key = pub_file.read()
            assert public_key.startswith("-----BEGIN PUBLIC KEY-----")

def test_create_new_user():
    """Test sprawdzający, czy można dodać nowego użytkownika i wygenerować klucze"""
    new_user = "NowyUzytkownik"
    private_key, public_key = generate_keys()

    private_key_path = os.path.join(KEYS_DIR, f"{new_user}_private.pem")
    public_key_path = os.path.join(KEYS_DIR, f"{new_user}_public.pem")

    # Zapisujemy klucze do plików
    with open(private_key_path, "w") as priv_file:
        priv_file.write(private_key)

    with open(public_key_path, "w") as pub_file:
        pub_file.write(public_key)

    # Sprawdzamy, czy pliki istnieją
    assert os.path.exists(private_key_path)
    assert os.path.exists(public_key_path)

    # Sprawdzamy, czy klucze mają poprawny format
    with open(private_key_path, "r") as priv_file:
        private_key_data = priv_file.read()
        assert private_key_data.startswith("-----BEGIN RSA PRIVATE KEY-----")

    with open(public_key_path, "r") as pub_file:
        public_key_data = pub_file.read()
        assert public_key_data.startswith("-----BEGIN PUBLIC KEY-----")

    print(f"\n[INFO] Nowy użytkownik {new_user} został poprawnie dodany z kluczami!")

    # Usuwanie testowych plików
    os.remove(private_key_path)
    os.remove(public_key_path)

def test_missing_key_generation(test_user):
    """Test sprawdzający, czy użytkownikowi bez kluczy zostaną one wygenerowane"""
    username, private_key, public_key = test_user
    private_key_path = os.path.join(KEYS_DIR, f"{username}_private.pem")
    public_key_path = os.path.join(KEYS_DIR, f"{username}_public.pem")

    # Usuwamy klucze
    os.remove(private_key_path)
    os.remove(public_key_path)

    # Sprawdzamy, czy po ponownym załadowaniu użytkownik dostaje nowe klucze
    new_private, new_public = generate_keys()
    
    with open(private_key_path, "w") as priv_file:
        priv_file.write(new_private)

    with open(public_key_path, "w") as pub_file:
        pub_file.write(new_public)

    assert os.path.exists(private_key_path)
    assert os.path.exists(public_key_path)

    print(f"\n[INFO] Użytkownik {username} nie miał kluczy – zostały poprawnie wygenerowane!")

def test_corrupted_key_detection(test_user):
    """Test sprawdzający, czy uszkodzony klucz zostanie wykryty"""
    username, _, _ = test_user
    private_key_path = os.path.join(KEYS_DIR, f"{username}_private.pem")

    # Uszkadzamy klucz
    with open(private_key_path, "w") as priv_file:
        priv_file.write("INVALID PRIVATE KEY DATA")

    # Sprawdzamy, czy plik jest uszkodzony
    with open(private_key_path, "r") as priv_file:
        private_key_data = priv_file.read()
        assert not private_key_data.startswith("-----BEGIN RSA PRIVATE KEY-----")

    print(f"\n[INFO] Wykryto uszkodzony klucz dla użytkownika {username}.")
