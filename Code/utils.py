import random
import numpy as np
import textwrap


def Convert_String_To_Integer(message_str):
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res


def Convert_Integer_To_String(n):
    res = ""
    while n > 0:
        res += chr(int(n) % 256)
        n //= 256
    return res[::-1]


def Calc_GCD(a, b):
    if b == 0:
        return a
    return Calc_GCD(b, a % b)


def Extended_Euclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = Extended_Euclid(b, a % b)
    k = a // b
    return (y, x - k * y)


def Mod_Inverse(a, n):
    (b, x) = Extended_Euclid(a, n)
    if b < 0:
        b = (b % n + n) % n  # we don’t want −ve integers
    return b


def Mod_of_Power(a, n, mod):
    if n == 0:
        return 1 % mod
    elif n == 1:
        return (a*1) % (mod*1) * 1
    else:
        b = Mod_of_Power(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
            return b
        else:
            return b * a % mod


def is_prime(n):
    if n < 2:
        return False
    if n < 10:
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
    if Mod_of_Power(10, n-1, n) == 1:
        if Mod_of_Power(12, n-1, n) == 1:
            if Mod_of_Power(14, n-1, n) == 1:
                return True
    return False


def Encrypt(m, n, e):
    c = Mod_of_Power(Convert_String_To_Integer(m), e, n)
    return c


def Decrypt(c, n, d):
    m = Convert_Integer_To_String(Mod_of_Power(c, d, n))
    return m


def CalcPrivateKey(p, q, e):
    phi = (p-1) * (q-1)
    d = Mod_Inverse(e, phi)
    return d


def generate_keys():
    n = 0
    p = 0
    q = 0
    e = 0
    d = 0
    while True:
        e = random.randint(7,
                           7000000)
        if is_prime(e):
            break
    while True:
        p = random.randint(10000000000000000000000000000000000,
                           1000000000000000000000000000000000000)
        if is_prime(p):
            break
    while True:
        q = random.randint(10000000000000000000000000000000000,
                           1000000000000000000000000000000000000)
        if is_prime(q):
            break
    n = p * q
    d = CalcPrivateKey(p, q, e)
    return n, e, d, p, q


def generate_keys_bits(n_bits):
    n = 0
    p = 0
    q = 0
    e = 0
    d = 0
    while True:
        p = random.getrandbits(n_bits//2)
        if is_prime(p):
            break
    while True:
        q = random.getrandbits(n_bits//2)
        if is_prime(q):
            break
    n = p * q
    while True:
        e = random.getrandbits(30)
        if is_prime(e):
            break
    d = CalcPrivateKey(p, q, e)
    return n, e, d, p, q


def Find_p_q(n):
    if n % 2 == 0:
        return 2, n//2
    else:
        for i in range(3, n, 2):
            if n % i == 0:
                return i, n//i


def Brute_Force_Attack(p, q, e, c):
    d = CalcPrivateKey(p, q, e)
    return Decrypt(c, p * q, d)


def encrypt_long_message(message, n, e):
    result = ""
    for i in range(0, len(message), 15):
        end = min(len(message), i+15)
        enc = str(Encrypt(message[i:end], n, e))
        if len(enc) < 72:
            enc = enc.zfill(72)
        result += enc
    return result


def decrypt_long_message(c, n, d):
    result = ""
    for i in range(0, len(c), 72):
        end = min(len(c), i+72)
        result += Decrypt(int(c[i:end]), n, d)
    return result


def Chosen_Ciphertext_Attack(p, q, e, c):
    n = p*q
    r = 2
    while Calc_GCD(n, r) != 1:
        r = r+1
    c_dash = (c * Mod_of_Power(r, e, n)) % n
    d = CalcPrivateKey(p, q, e)
    y = Mod_of_Power(c_dash, d, n)
    m = (y * Mod_Inverse(r, n)) % n
    m = Convert_Integer_To_String(m)
    return m


def main():
    msg = "Hello World!"
    n, e, d, p, q = generate_keys()
    c = Encrypt(msg, n, e)
    m = Decrypt(c, n, d)
    print("Original message: ", msg)
    print("Decrypted message: ", m)


if __name__ == '__main__':
    main()
