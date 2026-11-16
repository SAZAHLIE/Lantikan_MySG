"""
========================================================================
MYSG KPM: MODUL STORAN BILIK KEBAL (ZERO-SERVER-STORAGE)
========================================================================
"""

import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import zlib

# KATA LALUAN TETAP (HARDCODED) UNTUK PENYULITAN AUTOMATIK LATAR BELAKANG
_HARDCODED_SECRET = "MYSG_KPM_SECURE_KEY_2026_MASTER"
_SALT = b'mysg_kpm_salt_2026' 

def _get_fernet():
    """Menjana objek Fernet berasaskan kata laluan tetap dan salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(_HARDCODED_SECRET.encode()))
    return Fernet(key)

def encrypt_payload(payload_dict):
    """
    Mampatkan (compress) dan sulitkan (encrypt) data JSON secara automatik.
    """
    try:
        json_str = json.dumps(payload_dict)
        json_bytes = json_str.encode('utf-8')
        
        # Mampatkan data untuk menjimatkan ruang storan
        compressed_bytes = zlib.compress(json_bytes)
        
        # Sulitkan menggunakan kunci tetap
        f = _get_fernet()
        encrypted_bytes = f.encrypt(compressed_bytes)
        return encrypted_bytes
    except Exception as e:
        raise Exception(f"Gagal menyulitkan data: {str(e)}")

def decrypt_payload(encrypted_bytes):
    """
    Nyahsulit (decrypt) dan nyahmampat (decompress) fail .mysg secara automatik.
    """
    try:
        f = _get_fernet()
        decrypted_compressed = f.decrypt(encrypted_bytes)
        
        # Nyahmampat data
        decrypted_json_bytes = zlib.decompress(decrypted_compressed)
        
        json_str = decrypted_json_bytes.decode('utf-8')
        return json.loads(json_str)
    except Exception as e:
        raise Exception("Gagal menyahsulit data. Fail mungkin rosak atau format tidak sah.")
