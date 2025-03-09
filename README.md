# Symulator GPG - Komunikator

## Opis projektu

**Symulator GPG - Komunikator** to aplikacja umożliwiająca szyfrowanie, odszyfrowywanie, podpisywanie oraz weryfikację podpisów wiadomości przy użyciu kluczy **RSA**. Projekt został zbudowany w **Pythonie** i wykorzystuje bibliotekę **Streamlit** do interaktywnego interfejsu użytkownika oraz **PyCryptodome** do operacji kryptograficznych.

---

## Struktura katalogów
```
📂 CYBER-SECURITY-PROJECT/
│── 📂 keys/                # Katalog przechowujący klucze użytkowników
│   ├── Hubert_private.pem
│   ├── Hubert_public.pem
│   ├── Kamil_private.pem
│   ├── Kamil_public.pem
│   ├── Sebastian_private.pem
│   ├── Sebastian_public.pem
│
│── 📂 tests/               # Katalog testów jednostkowych
│   ├── test_crypto_utils.py
│   ├── test_users.py
│
│── .github/workflows/      # Konfiguracja CI/CD (GitHub Actions)
│   ├── ci.yml
│
│── .gitignore              # Plik ignorujący pliki binarne
│── app.log                 # Plik logów aplikacji
│── keys.db                 # Baza danych (opcjonalna)
│── private_key.pem         # Przykładowy klucz prywatny
│── public_key.pem          # Przykładowy klucz publiczny
│── README.md               # Dokumentacja projektu
│── requirements.txt        # Lista zależności
│── streamlit_main.py       # Interfejs użytkownika (UI)
│── crypto_utils.py         # Logika kryptograficzna
│── users.py                # Obsługa użytkowników i zarządzanie kluczami
```

---

## Instalacja i uruchomienie

### Instalacja zależności
Aby uruchomić projekt, należy zainstalować wymagane biblioteki:
```bash
pip install -r requirements.txt
```

### Uruchomienie aplikacji
Aplikację można uruchomić za pomocą **Streamlit**:
```bash
streamlit run streamlit_main.py
```

### Uruchomienie testów jednostkowych
```bash
pytest tests/
```

### Sprawdzenie zgodności kodu ze standardem **PEP8**
```bash
flake8 streamlit_main.py users.py crypto_utils.py --max-line-length=100
```

---

## Funkcjonalności

✅ **Generowanie kluczy RSA** (2048-bit) dla użytkowników
✅ **Szyfrowanie i odszyfrowywanie wiadomości** przy użyciu kluczy RSA
✅ **Podpisywanie cyfrowe wiadomości** i weryfikacja podpisów
✅ **Interaktywny interfejs użytkownika** (Streamlit)
✅ **Zarządzanie kluczami użytkowników** (pliki `.pem`)
✅ **Testy jednostkowe** (`pytest`)
✅ **Automatyczna analiza kodu (CI/CD)** przy użyciu **GitHub Actions**

---

## Testy jednostkowe
Projekt zawiera testy sprawdzające poprawność implementacji funkcji kryptograficznych i zarządzania użytkownikami.

### **Testy w `tests/test_crypto_utils.py`**
- **Test generowania kluczy RSA**
- **Test szyfrowania i odszyfrowania wiadomości**
- **Test podpisywania i weryfikacji podpisu**
- **Testy negatywne (np. nieprawidłowy klucz, błędny podpis)**

### **Testy w `tests/test_users.py`**
- **Test wczytywania kluczy użytkowników**
- **Test generowania kluczy dla nowego użytkownika**
- **Test poprawności zapisu i odczytu kluczy**

Uruchomienie testów:
```bash
pytest tests/
```

---

## CI/CD (GitHub Actions)
Projekt wykorzystuje **GitHub Actions** do automatycznego testowania kodu oraz sprawdzania stylu PEP8.

**Plik konfiguracyjny `.github/workflows/ci.yml` zawiera:**
- Automatyczną instalację zależności (`pip install -r requirements.txt`)
- Uruchomienie testów jednostkowych (`pytest tests/`)
- Sprawdzenie jakości kodu (`flake8`)

---

## Licencja
Projekt jest dostępny na licencji **MIT**. Możesz go dowolnie modyfikować i wykorzystywać w swoich projektach.

---

## Autor
**Kamil Kwiek** 



