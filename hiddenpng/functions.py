from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.layout import Layout


def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="main"),
        Layout(name="footer", size=5),
    )

    return layout


def generate_key(keyword) -> bytes:
    salt = b'QP9&PJ&V&2sm&U3l'
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000
            )
    key = urlsafe_b64encode(kdf.derive(bytes(keyword, 'utf-8')))
    return key


def encrypt_data(data, key) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(encrypted_data, key) -> bytes:
    f = Fernet(key)
    return f.decrypt(encrypted_data)


def hide_data(image_path, output_path, data, key) -> None:
    image = Image.open(image_path)
    data_bytes = data.encode()
    encrypted_data = encrypt_data(data_bytes, key)
    binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)
    width, height = image.size
    data_size = len(binary_data)
    max_data_size = width * height * 3
    if data_size > max_data_size:
        raise ValueError('Data too large for image.')
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                if data_index < data_size:
                    bit = binary_data[data_index]
                    pixel[i] = (pixel[i] & 0b11111110) | int(bit)
                    data_index += 1
            image.putpixel((x, y), tuple(pixel))
    image.save(output_path)


def extract_data(image_path, key) -> bytes:
    image = Image.open(image_path)
    width, height = image.size
    data = []
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            bit_string = ''.join([str(pixel[i] & 1) for i in range(3)])
            data.append(bit_string)

    binary_data = ''.join(data)
    padding_length = len(binary_data) % 8
    if padding_length != 0:
        binary_data = binary_data[:-padding_length]

    binary_data = bytes([int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)]) # noqa
    padder = padding.PKCS7(256).padder()
    key = padder.update(key) + padder.finalize()
    decrypted_data = decrypt_data(binary_data, key)

    return decrypted_data
