import random
import math


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits) | 1
        if num % 4 == 3 and is_prime(num):
            return num


def bbs_generate(n_bits):
    p = generate_prime(24)
    q = generate_prime(24)
    N = p * q
    x = random.randint(2, N - 1)
    while math.gcd(x, N) != 1:
        x = random.randint(2, N - 1)

    bits = []
    for _ in range(n_bits):
        x = (x ** 2) % N
        bits.append(x % 2)

    return bits


def test_single_bits(bits):
    count_ones = sum(bits)
    return 9725 < count_ones < 10275


def test_series(bits):
    series_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    current_length = 1

    for i in range(1, len(bits)):
        if bits[i] == bits[i - 1]:
            current_length += 1
        else:
            if current_length >= 6:
                series_counts[6] += 1
            else:
                series_counts[current_length] += 1
            current_length = 1

    if current_length >= 6:
        series_counts[6] += 1
    else:
        series_counts[current_length] += 1

    thresholds = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209)
    }

    #print(series_counts)

    for length, (low, high) in thresholds.items():
        if not (low <= series_counts[length]/2 <= high):
            return False

    return True




def test_long_series(bits):
    max_length = 0
    current = bits[0]
    length = 1
    for i in range(1, len(bits)):
        if bits[i] == current:
            length += 1
        else:
            max_length = max(max_length, length)
            current = bits[i]
            length = 1
    max_length = max(max_length, length)
    return max_length < 26


def test_poker(bits):

    freq = {
        "0000": 0, "0001": 0, "0010": 0, "0011": 0,
        "0100": 0, "0101": 0, "0110": 0, "0111": 0,
        "1000": 0, "1001": 0, "1010": 0, "1011": 0,
        "1100": 0, "1101": 0, "1110": 0, "1111": 0
    }

    segments = []
    for i in range(0, len(bits), 4):
        segments.append(bits[i:i + 4])

    for seg in segments:
        seg_str = ''.join(map(str, seg))
        freq[seg_str] += 1

    #for k,v in freq.items():
    #    print(k, ":", v)

    total_sum = sum(v ** 2 for v in freq.values())
    X = (16 / 5000) * total_sum - 5000

    return 2.16 < X < 46.17




bits = bbs_generate(20000)

results = {
    "Test pojedynczych bitów": test_single_bits(bits),
    "Test serii": test_series(bits),
    "Test długiej serii": test_long_series(bits),
    "Test pokerowy": test_poker(bits)
}


for test, passed in results.items():
    print(f"{test}: {'Passed' if passed else 'Failed'}")


