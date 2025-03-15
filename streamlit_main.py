import streamlit as st
from users import user_keys
from crypto_utils import (
    encrypt_message,
    decrypt_message,
    sign_message,
    verify_signature)

st.title("Symulator GPG - Komunikator")

# Wyświetlanie kluczy użytkowników
st.header("Klucze użytkowników")
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for i, (user, keys) in enumerate(user_keys.items()):
    with columns[i % 3]:
        st.subheader(user)
        st.text_area(
            f"Klucz publiczny {user}",
            keys["public_key"],
            height=100)
        st.text_area(
            f"Klucz prywatny {user}",
            [keys["private_key"]],
            height=100,
            disabled=True)

# Wysyłanie wiadomości
st.header("Wyślij wiadomość")
recipient = st.selectbox(
    "Wybierz odbiorcę:",
    list(user_keys.keys())
    )

message_to_send = st.text_input("Wpisz wiadomość:")

if st.button("Zaszyfruj i wyślij"):
    try:
        recipient_public_key = user_keys[recipient]["public_key"].encode()
        encrypted_message = encrypt_message(
            message_to_send,
            recipient_public_key)
        st.text_area("Zaszyfrowana wiadomość:",
                     encrypted_message,
                     height=100)
    except Exception as e:
        st.error(f"Błąd: {e}")

# Odbieranie wiadomości
st.header("Odbierz wiadomość")
receiver = st.selectbox(
    "Wybierz siebie (odbiorcę):",
    list(user_keys.keys()),
    key="receiver")
message_to_decrypt = st.text_area(
    "Wklej zaszyfrowaną wiadomość:",
    key="decrypt_input")

if st.button("Odszyfruj"):
    try:
        receiver_private_key = user_keys[receiver]["private_key"].encode()
        decrypted_message = decrypt_message(
            message_to_decrypt,
            receiver_private_key)
        st.success(f"Odszyfrowana wiadomość: {decrypted_message}")
    except Exception as e:
        st.error(f"Błąd: {e}")

# Podpisywanie wiadomości
st.header("Podpisywanie wiadomości")
signer = st.selectbox(
    "Wybierz nadawcę (podpisującego):",
    list(user_keys.keys()),
    key="signer")
message_to_sign = st.text_input(
    "Wpisz wiadomość do podpisania:",
    key="sign_input")

if st.button("Podpisz"):
    try:
        signer_private_key = user_keys[signer]["private_key"].encode()
        signature = sign_message(message_to_sign, signer_private_key)
        st.text_area("Podpis cyfrowy:", signature, height=100)
    except Exception as e:
        st.error(f"Błąd: {e}")

# Weryfikacja podpisu
st.header("Weryfikacja podpisu")
verifier = st.selectbox(
    "Wybierz nadawcę podpisu:",
    list(user_keys.keys()),
    key="verifier")
message_to_verify = st.text_input(
    "Wpisz wiadomość do weryfikacji:",
    key="verify_input")
signature_to_verify = st.text_area(
    "Wklej podpis cyfrowy:",
    key="signature_input")

if st.button("Zweryfikuj podpis"):
    try:
        verifier_public_key = user_keys[verifier]["public_key"].encode()
        verification_result = verify_signature(
            message_to_verify,
            signature_to_verify,
            verifier_public_key)
        st.success(verification_result)
    except Exception as e:
        st.error(f"Błąd: {e}")
