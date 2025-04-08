import random
import math
from sympy import mod_inverse

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits) | 1
        if is_prime(num):
            return num

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_keys():
    p = generate_prime(24)
    q = generate_prime(24)

    while abs(p - q) < 3000000:
        q = generate_prime(8)

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi - 1)
        if math.gcd(e, phi) == 1 and is_prime(e):
            break

    d = mod_inverse(e, phi)

    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = p * q = {n}")
    print(f"φ(n) = (p - 1) * (q - 1) = {phi}")
    print(f"e (public) = {e}")
    print(f"d (private) = {d}")
    print()

    return ((e, n), (d, n))

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)



def is_primitive_root(g, n):
    n_minus_1 = n - 1
    for d in range(1, n_minus_1):
        if n_minus_1 % d == 0 and pow(g, d, n) == 1:
            return False
    return True

def diffie_hellman():
    n = generate_prime(16)
    g = random.randint(2, n - 1)

    while not is_primitive_root(g, n):
        g = random.randint(2, n - 1)

    x = random.randint(2, n - 1)
    y = random.randint(2, n - 1)

    X = pow(g, x, n)
    Y = pow(g, y, n)

    k_A = pow(Y, x, n)
    k_B = pow(X, y, n)

    return k_A, k_B


public_key, private_key = generate_keys()
message = "Example message to encrypt using RSA"
ciphertext = encrypt(message, public_key)
decrypted_message = decrypt(ciphertext, private_key)

dh_key_A, dh_key_B = diffie_hellman()

print("Public Key:", public_key)
print("Private Key:", private_key)
print()
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted_message)
print()
print("DH Shared Key A:", dh_key_A)
print("DH Shared Key B:", dh_key_B)
