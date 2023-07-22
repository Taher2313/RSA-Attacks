# RSA-Attacks

This project is designed to implement RSA encryption and decryption, as well as explore two potential attacks: the Chosen Ciphertext Attack and the Brute Force Attack.

### RSA Encryption and Decryption:
The project will include functions to generate RSA public and private keys. RSA encryption will be achieved by raising the message to the power of the public exponent and taking the result modulo the public modulus. RSA decryption will use the private exponent and the same modular arithmetic to recover the original plaintext from the ciphertext.

### Chosen Ciphertext Attack (CCA):
The project will investigate the concept of a Chosen Ciphertext Attack, a cryptographic attack where the adversary gains access to decrypted ciphertexts under the target's public key. However, as a responsible project, it will not engage in actual attacks but rather explore the potential vulnerabilities and countermeasures against this type of attack in RSA.

### Brute Force Attack:
The project will explore the idea of a Brute Force Attack, a straightforward method where the attacker systematically tries all possible private keys to decrypt a ciphertext. However, the project will not attempt any real attacks. Instead, it will focus on discussing the importance of using sufficiently large key sizes to render brute force attacks infeasible and ensure the security of RSA encryption.
