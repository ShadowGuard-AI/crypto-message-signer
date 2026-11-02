![Introduction banner: the themed scene before any name is spoken](intro-banner.png)

# crypto-message-signer

Title block: the name above is set in BioRhyme in ladybird red on a cream plate, with a black spot rule beneath it and one small raft oval at the left of the first heading only, in the manner of a field guide plate.

![Logo](logo.png)

![Wordmark banner](banner.png)

![Animated scene](scene.svg)

![Major separator](sep-heavy.svg)


# crypto-message-signer

Signs a message with a PEM private key and verifies a signature with the matching PEM public key. Algorithms: RSA (PKCS1v15), ECDSA, and Ed25519, with SHA-256, SHA-384, or SHA-512 for RSA and ECDSA. Ed25519 hashes internally, so `--hash_algorithm` has no effect on it.

The tool does not generate keys. Use OpenSSL or another tool to create the PEM key pair first.

![Major separator](sep-heavy.svg)

## Requirements

- Python 3
- `cryptography` 41.0.0 or later (see requirements.txt)

![Minor separator](sep-light.svg)

## Install

```bash
git clone https://github.com/ShadowGuard-AI/crypto-message-signer.git
cd crypto-message-signer
pip install -r requirements.txt
```


> Field note: hex must be decoded back to bytes before verification, because the verify form reads the signature file as raw bytes, not as hex text.

![Minor separator](sep-light.svg)

## Usage

```bash
python3 main.py sign --message "hello" --private_key private.pem --algorithm rsa
python3 main.py verify --message "hello" --public_key public.pem --signature signature.bin --algorithm rsa
```

Signing prints the signature as hex on stdout. Verification takes the signature as a binary file (decode the hex output back to bytes first), logs whether it is valid, and exits 0 for a valid signature and 1 for an invalid one or any error.


> Field note: the hash flag does nothing for Ed25519, which hashes inside its own scheme, so the chosen hash changes nothing on that bank.

![Minor separator](sep-light.svg)

## Parameters

- `action`: Positional. `sign` or `verify`.
- `--message`: The message to sign or verify (required).
- `--private_key`: Path to the private key PEM file (required for sign).
- `--public_key`: Path to the public key PEM file (required for verify).
- `--signature`: Path to the binary signature file (required for verify).
- `--algorithm`: `rsa`, `ecdsa`, or `ed25519` (default: rsa). The key file must match the chosen algorithm.
- `--hash_algorithm`: `sha256`, `sha384`, or `sha512` (default: sha256; RSA and ECDSA only).


> Field note: no passphrase is accepted for an encrypted PEM, because private keys load with no passphrase and no control asks for one.

![Minor separator](sep-light.svg)

## Verified run note

The usage and parameters above are taken from the argument parser in `main.py`. A live run in this environment is blocked because the `cryptography` package is not installed here, so even `--help` stops at that import; no run result is claimed for this tool.


> Field note: one exit code covers both a false signature and a broken setup, so exit 1 alone cannot split a failed verification from a failed loading.

![Minor separator](sep-light.svg)

## License

Licensed under the terms in LICENSE.

![Major separator](sep-heavy.svg)

## Field notes, gathered at the bank

The buttons of this re-skin read Sign the Message, Verify the Signature, and Show the Field Notes. Its headings read Two Actions Only, Keys Are Brought, Not Made, Hex Out, Raw Bytes Back, and One Exit for Many Failings. Two facts are entered once more at full size: the message is encoded as utf-8 before signing, and the repository LICENSE file carries the MIT License, its holder line giving a pen name together with a single initial for the remaining name.
