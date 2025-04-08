import hashlib
import time
import random


# zadanie1
def generate_hash(text):
    algorithms = {
        "MD5": hashlib.md5,
        "SHA-1": hashlib.sha1,
        "SHA-256": hashlib.sha256,
        "SHA-512": hashlib.sha512,
        "SHA-3-256": hashlib.sha3_256,
        "SHA-3-512": hashlib.sha3_512
    }

    hashes = {}
    for name, algorithm in algorithms.items():
        start_time = time.perf_counter()
        hash_value = algorithm(text.encode('utf-8')).hexdigest()
        elapsed_time = time.perf_counter() - start_time
        hashes[name] = {"hash": hash_value, "time": elapsed_time}

    return hashes


# zadanie2
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


file_sizes = ["0.5mb", "1mb", "5mb", "10mb"]

for file_size in file_sizes:
    file_name = f"{file_size}.txt"
    try:
        print(f"Processing file: (Size: {file_size})")
        text = read_file(file_name)
        text_length = len(text)
        print(f"Input length: {text_length} characters")

        hashes = generate_hash(text)
        for name, info in hashes.items():
            print(f"{name}: {info['hash']} (Time: {info['time']:.9f} sec)")
        print()
    except FileNotFoundError:
        print(f"File {file_name} not found. Please make sure the file exists.")
        print()

"""
# zadanie3
word = "word"
md5_hash = generate_hash(word)["MD5"]["hash"]
print(f"MD5 hash for '{word}': {md5_hash}")
"""

# zadanie5
def random_string(length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def check_collisions():
    collisions = 0
    hash1 = hashlib.md5(random_string(30).encode()).hexdigest()
    for _ in range(10000):
        hash2 = hashlib.md5(random_string(30).encode()).hexdigest()

        if hash1[:3] == hash2[:3]:
            collisions += 1

    print(f"Collision probability in first 12 bits for MD-5: {collisions / 10000:.5f}")


check_collisions()

"""
   Z badań świadczy o wysokiej unikalności wyników funkcji skrótu SHA-256.
   To pokazuje, że ta funkcja zapewnia bardzo niski poziom kolizji,
   co jest korzystne dla bezpieczeństwa i integralności danych.
"""


# zadanie6
def check_sac():
    text1_hash = generate_hash("tell me where have you been")["SHA-256"]["hash"]
    text2_hash = generate_hash("lell me where have you been")["SHA-256"]["hash"]

    hash1_bits = f"{int(text1_hash, 16):0256b}"
    hash2_bits = f"{int(text2_hash, 16):0256b}"

    similarity = sum(1 for i in range(256) if hash1_bits[i] == hash2_bits[i])

    return round((256 - similarity) / 256, 4)


sac_score = check_sac()
print(f"SAC score for SHA-256: {sac_score}")

"""
Wynik SAC równy 0.4844, czyli około 48.44% bitów zmienia się przy zmianie jednego bitu w danych wejściowych. 
Funkcja haszująca SHA-256 dobrze spełnia kryterium rozproszenia zmian, ponieważ jest prawie równa 0.5 
To potwierdza dobrą losowość i bezpieczeństwo tej funkcji skrótu.
"""
