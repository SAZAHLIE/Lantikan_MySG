"""
========================================================================
SISTEM PENGURUSAN & PENGIRAAN BEBAN KERJA KAKITANGAN SEKOLAH (MYSG KPM)
MODULE: CRYPTO VAULT ENGINE (AES-256 ENCRYPTION / DECRYPTION)
========================================================================
"""

import json
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _generate_key_from_passphrase(passphrase: str, salt: bytes) -> bytes:
    """Menjana kunci AES-256 daripada kata laluan pengguna mengikut standard PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode('utf-8')))

def encrypt_payload(data_dict: dict, passphrase: str) -> bytes:
    """
    Menenkripsi JSON dictionary menjadi bytes terenkripsi selamat (AES-256).
    Mengeksport data berserta salt untuk nyah-enkripsi selamat.
    """
    if not passphrase:
        raise ValueError("Kata laluan tidak boleh kosong.")

    salt = os.urandom(16)
    key = _generate_key_from_passphrase(passphrase, salt)
    fernet = Fernet(key)

    json_str = json.dumps(data_dict)
    encrypted_bytes = fernet.encrypt(json_str.encode('utf-8'))

    # Cantumkan Salt (16 bytes) di bahagian hadapan data terenkripsi
    final_payload = salt + encrypted_bytes
    return final_payload

def decrypt_payload(encrypted_payload: bytes, passphrase: str) -> dict:
    """
    Menyah-enkripsikan bytes terenkripsi menggunakan kata laluan.
    Mengembalikan data asal dalam bentuk Python Dictionary.
    """
    if not passphrase:
        raise ValueError("Kata laluan tidak boleh kosong.")
    
    if len(encrypted_payload) < 16:
        raise ValueError("Format fail vault tidak sah atau rosak.")

    # Ekstrak Salt (16 bytes pertama)
    salt = encrypted_payload[:16]
    actual_encrypted_data = encrypted_payload[16:]

    key = _generate_key_from_passphrase(passphrase, salt)
    fernet = Fernet(key)

    decrypted_bytes = fernet.decrypt(actual_encrypted_data)
    json_str = decrypted_bytes.decode('utf-8')
    return json.loads(json_str)