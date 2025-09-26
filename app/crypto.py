from cryptography.fernet import Fernet
import base64
import hashlib
# from typing import str


def derive_key_from_master_password(master_password: str, salt: bytes = b'stable_salt') -> bytes:
    # Create a key derivation from the master password
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    # Fernet needs a base64-encoded 32-byte key
    return base64.urlsafe_b64encode(key[:32])


def encrypt_password(password: str, master_password: str) -> str:
    # Encrypt a password using the master password
    key = derive_key_from_master_password(master_password)
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password: str, master_password: str) -> str:
    # Decrypt a password using master
    key = derive_key_from_master_password(master_password)
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
