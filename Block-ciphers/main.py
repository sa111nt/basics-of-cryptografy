import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt

MODES = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'OFB': AES.MODE_OFB,
    'CTR': AES.MODE_CTR
}

KEY = get_random_bytes(16)

FILES = {
    '100KB': '100kb.txt',
    '1MB': '1mb.txt',
    '10MB': '10mb.txt'
}

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def encrypt_decrypt(mode_name, data):
    mode = MODES[mode_name]
    iv_or_nonce = get_random_bytes(16)

    if mode == AES.MODE_ECB:
        cipher = AES.new(KEY, mode)
        decipher = AES.new(KEY, mode)
    elif mode == AES.MODE_CTR:
        cipher = AES.new(KEY, mode, nonce=iv_or_nonce[:8])
        decipher = AES.new(KEY, mode, nonce=iv_or_nonce[:8])
    else:
        cipher = AES.new(KEY, mode, iv=iv_or_nonce)
        decipher = AES.new(KEY, mode, iv=iv_or_nonce)

    pad_len = 16 - (len(data) % 16)
    padded = data + bytes([pad_len]) * pad_len if mode in [AES.MODE_ECB, AES.MODE_CBC] else data

    start_enc = time.perf_counter()
    ciphertext = cipher.encrypt(padded)
    end_enc = time.perf_counter()

    start_dec = time.perf_counter()
    decrypted = decipher.decrypt(ciphertext)
    end_dec = time.perf_counter()

    if mode in [AES.MODE_ECB, AES.MODE_CBC]:
        decrypted = decrypted[:-decrypted[-1]]

    return end_enc - start_enc, end_dec - start_dec


results = {mode: {'enc': [], 'dec': []} for mode in MODES}
sizes_labels = list(FILES.keys())

for size_label, filename in FILES.items():
    print(f"\nPlik: {filename}")
    data = read_file(filename)

    for mode_name in MODES:
        enc_time, dec_time = encrypt_decrypt(mode_name, data)
        results[mode_name]['enc'].append(enc_time)
        results[mode_name]['dec'].append(dec_time)
        print(f"Tryb {mode_name} | Szyfrowanie: {enc_time:.6f}s | Deszyfrowanie: {dec_time:.6f}s")


for mode in MODES:
    plt.plot(sizes_labels, results[mode]['enc'], label=f'{mode}', marker='o')

plt.title("Czas szyfrowania w różnych trybach AES")
plt.xlabel("Rozmiar pliku")
plt.ylabel("Czas (s)")
plt.legend(title="Tryb")
plt.grid(True)
plt.tight_layout()
plt.show()



print("\nPropagacja błędów: ")

sample_text = b"To jest przykladowy tekst do zaszyfrowania w celu testowania propagacji bledow. " * 2

for mode_name in MODES:
    mode = MODES[mode_name]
    iv_or_nonce = get_random_bytes(16)

    if mode == AES.MODE_ECB:
        cipher = AES.new(KEY, mode)
        decipher = AES.new(KEY, mode)
    elif mode == AES.MODE_CTR:
        cipher = AES.new(KEY, mode, nonce=iv_or_nonce[:8])
        decipher = AES.new(KEY, mode, nonce=iv_or_nonce[:8])
    else:
        cipher = AES.new(KEY, mode, iv=iv_or_nonce)
        decipher = AES.new(KEY, mode, iv=iv_or_nonce)

    padded = sample_text
    if mode in [AES.MODE_ECB, AES.MODE_CBC]:
        pad_len = 16 - (len(sample_text) % 16)
        padded += bytes([pad_len]) * pad_len

    ciphertext = bytearray(cipher.encrypt(padded))

    #zmieniamy 1 bajt w środku szyfrogramu
    corrupted_ciphertext = ciphertext[:]
    corrupted_ciphertext[len(ciphertext)//2] ^= 0xFF  # XORujemy bajt ze 11111111

    decrypted = decipher.decrypt(bytes(corrupted_ciphertext))

    if mode in [AES.MODE_ECB, AES.MODE_CBC]:
        try:
            decrypted = decrypted[:-decrypted[-1]]
        except:
            pass  # W przypadku błędnego paddingu ignorujemy

    print(f"\nTryb {mode_name}:")
    print("Odszyfrowany tekst z błędem:\n", decrypted.decode('utf-8', errors='replace'))




def encrypt_cbc_using_ecb(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_ECB)  # Używamy trybu ECB do szyfrowania
    padded_data = data + bytes([16 - len(data) % 16]) * (16 - len(data) % 16)

    # Szyfrujemy bloki używając IV i operacji XOR
    ciphertext = bytearray(len(padded_data))
    prev_block = iv
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i + 16]
        xor_block = bytes([block[j] ^ prev_block[j] for j in range(16)])  # XOR z poprzednim blokiem
        cipher_block = cipher.encrypt(xor_block)  # Szyfrujemy blok przy użyciu ECB
        ciphertext[i:i + 16] = cipher_block
        prev_block = cipher_block

    return iv + ciphertext

def decrypt_cbc_using_ecb(ciphertext):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(KEY, AES.MODE_ECB)

    decrypted_data = bytearray(len(ciphertext))
    prev_block = iv
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        decrypted_block = cipher.decrypt(block)  # Deszyfrujemy blok przy użyciu ECB
        decrypted_data[i:i + 16] = bytes([decrypted_block[j] ^ prev_block[j] for j in range(16)])  # XOR z poprzednim blokiem
        prev_block = block

    pad_len = decrypted_data[-1]
    return decrypted_data[:-pad_len]

sample_text = b"To jest przykladowy tekst do zaszyfrowania w celu testowania trybu CBC."

ciphertext_cbc = encrypt_cbc_using_ecb(sample_text)
print("\n\nZaszyfrowany tekst (CBC z ECB):", ciphertext_cbc.hex())

decrypted_text_cbc = decrypt_cbc_using_ecb(ciphertext_cbc)
print("Odszyfrowany tekst (CBC z ECB):", decrypted_text_cbc.decode('utf-8', errors='replace'))









""" 
 ECB (Electronic Codebook)
Jak działa: Każdy blok danych szyfruje się osobno.

Zaleta: Bardzo szybki i prosty.

Wada: Niezabezpieczony – jeśli te same dane pojawią się kilka razy, szyfrogramy będą takie same. Można "zobaczyć" wzory w danych.

Użycie: raczej unikać w praktyce.


 CBC (Cipher Block Chaining)
Jak działa: Każdy blok przed szyfrowaniem jest mieszany z poprzednim blokiem szyfrogramu (pierwszy z tzw. wektorem IV).

Zaleta: Ukrywa powtarzające się dane, dużo bezpieczniejszy niż ECB.

Wada: Wolniejszy, bo trzeba przetwarzać bloki po kolei.

Użycie: popularny w starszych systemach, ale powoli wypierany przez nowsze tryby.


 CFB (Cipher Feedback)
Jak działa: Przekształca szyfr blokowy w strumieniowy – dane mogą być szyfrowane "po kawałku".

Zaleta: Nadaje się do przesyłania danych strumieniowo (np. przez sieć).

Wada: Jeszcze wolniejszy, bo każdy bajt zależy od poprzedniego.

Użycie: Rzadziej stosowany, np. w transmisji danych.

 
 OFB (Output Feedback)
Jak działa: Podobny do CFB, ale szyfrowanie danych nie zależy od samej wiadomości, tylko od wcześniejszych wyników szyfrowania.

Zaleta: Stabilny i odporny na błędy transmisji.

Wada: Trochę wolniejszy, i mniej popularny.

Użycie: Gdy ważna jest odporność na błędy (np. połączenia sieciowe).


CTR (Counter)
Jak działa: Zamiast zależności między blokami, używa rosnącego licznika (counter) dla każdego bloku.

Zaleta: Bardzo szybki – pozwala szyfrować bloki równolegle, bez czekania.

Bezpieczeństwo: Bardzo dobre, jeśli licznik jest unikalny.

Użycie: Nowoczesne systemy, dyski, VPN-y itp.
"""