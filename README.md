![Banner](banner.png)

# crypto-message-signer

Signs a message with a PEM private key and verifies a signature with the matching PEM public key. Algorithms: RSA (PKCS1v15), ECDSA, and Ed25519, with SHA-256, SHA-384, or SHA-512 for RSA and ECDSA. Ed25519 hashes internally, so `--hash_algorithm` has no effect on it.

The tool does not generate keys. Use OpenSSL or another tool to create the PEM key pair first.

## Requirements

- Python 3
- `cryptography` 41.0.0 or later (see requirements.txt)

## Install

```bash
git clone https://github.com/ShadowGuard-AI/crypto-message-signer.git
cd crypto-message-signer
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py sign --message "hello" --private_key private.pem --algorithm rsa
python3 main.py verify --message "hello" --public_key public.pem --signature signature.bin --algorithm rsa
```

Signing prints the signature as hex on stdout. Verification takes the signature as a binary file (decode the hex output back to bytes first), logs whether it is valid, and exits 0 for a valid signature and 1 for an invalid one or any error.

## Parameters

- `action`: Positional. `sign` or `verify`.
- `--message`: The message to sign or verify (required).
- `--private_key`: Path to the private key PEM file (required for sign).
- `--public_key`: Path to the public key PEM file (required for verify).
- `--signature`: Path to the binary signature file (required for verify).
- `--algorithm`: `rsa`, `ecdsa`, or `ed25519` (default: rsa). The key file must match the chosen algorithm.
- `--hash_algorithm`: `sha256`, `sha384`, or `sha512` (default: sha256; RSA and ECDSA only).

## Verified run note

The usage and parameters above are taken from the argument parser in `main.py`. A live run in this environment is blocked because the `cryptography` package is not installed here, so even `--help` stops at that import; no run result is claimed for this tool.

## License

Licensed under the terms in LICENSE.
