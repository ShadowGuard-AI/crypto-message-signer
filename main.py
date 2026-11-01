import argparse
import logging
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_HASHES = {"sha256": hashes.SHA256, "sha384": hashes.SHA384, "sha512": hashes.SHA512}


def _hash(name):
    # argparse already restricts name to the keys above, so this cannot
    # raise KeyError from the command line; library callers get one too.
    return _HASHES[name]()

def setup_argparse():
    """
    Sets up the command-line argument parser.
    """
    parser = argparse.ArgumentParser(description="Sign and verify messages using cryptographic keys.")
    parser.add_argument("action", choices=["sign", "verify"], help="Action to perform: sign or verify.")
    parser.add_argument("--message", type=str, required=True, help="The message to sign or verify.")
    parser.add_argument("--private_key", type=str, help="Path to the private key file (for signing).")
    parser.add_argument("--public_key", type=str, help="Path to the public key file (for verifying).")
    parser.add_argument("--signature", type=str, help="Path to the signature file (for verification).")
    parser.add_argument("--algorithm", choices=["rsa", "ecdsa", "ed25519"], default="rsa", help="The signature algorithm to use (default: rsa).")
    parser.add_argument("--hash_algorithm", choices=["sha256", "sha384", "sha512"], default="sha256", help="The hash algorithm to use (default: sha256).")
    return parser.parse_args()

def load_key(key_path, is_private=True):
    """
    Loads a key (private or public) from a file.
    Handles file not found and key loading errors.
    """
    try:
        with open(key_path, "rb") as key_file:
            key_data = key_file.read()
    except FileNotFoundError:
        logging.error(f"Key file not found: {key_path}")
        sys.exit(1)  # Exit if file not found

    try:
        if is_private:
            # password=None is a real limit, not a default I can relax
            # here: an encrypted PEM raises ValueError below and exits,
            # and no flag in this tool accepts a passphrase.
            private_key = load_pem_private_key(key_data, password=None)
            return private_key
        else:
            public_key = load_pem_public_key(key_data)
            return public_key
    except ValueError as e:
        logging.error(f"Error loading key from {key_path}: {e}")
        sys.exit(1)  # Exit if key loading fails

def sign_message(message, private_key_path, algorithm, hash_algorithm):
    """
    Signs a message using a private key.
    Supports RSA, ECDSA, and Ed25519 algorithms.
    """
    private_key = load_key(private_key_path, is_private=True)

    try:
        # Nothing checks the loaded key against the --algorithm choice.
        # I rely on the library to refuse a mismatched pair, and the
        # wide except below turns that refusal into a plain exit 1.
        message_bytes = message.encode('utf-8')
        h = _hash(hash_algorithm)

        # The old code called private_key.signer() / public_key.verifier(),
        # an incremental API that current cryptography releases removed, so
        # RSA and ECDSA signing failed on every run. The one-shot sign()
        # below is the supported replacement and is simpler here because
        # the whole message is already in memory.
        # RSA keeps PKCS1v15: the original passed a (non-working) padding
        # object rather than PSS, so v1.5 preserves the intended scheme.
        if algorithm == "rsa":
            return private_key.sign(message_bytes, padding.PKCS1v15(), h)
        elif algorithm == "ecdsa":
            return private_key.sign(message_bytes, ec.ECDSA(h))
        elif algorithm == "ed25519":
            # Ed25519 hashes internally; --hash_algorithm has no effect on
            # it. Saying nothing about that would make the flag look broken.
            return private_key.sign(message_bytes)
        else:
            raise ValueError("Unsupported algorithm")

    except Exception as e:
        logging.error(f"Error during signing: {e}")
        sys.exit(1)


def verify_message(message, public_key_path, signature_path, algorithm, hash_algorithm):
    """
    Verifies a message signature using a public key.
    Supports RSA, ECDSA, and Ed25519 algorithms.
    """
    public_key = load_key(public_key_path, is_private=False)

    try:
        with open(signature_path, "rb") as sig_file:
            signature = sig_file.read()
    except FileNotFoundError:
        logging.error(f"Signature file not found: {signature_path}")
        sys.exit(1)

    try:
        message_bytes = message.encode('utf-8')
        h = _hash(hash_algorithm)

        if algorithm == "rsa":
            public_key.verify(signature, message_bytes, padding.PKCS1v15(), h)
        elif algorithm == "ecdsa":
            public_key.verify(signature, message_bytes, ec.ECDSA(h))
        elif algorithm == "ed25519":
            public_key.verify(signature, message_bytes)
        else:
            raise ValueError("Unsupported algorithm")

        logging.info("Signature is valid.")
        return True

    except InvalidSignature:
        logging.error("Signature is invalid.")
        return False
    except Exception as e:
        # A wrong key type or a malformed signature lands here, not in
        # InvalidSignature, but main treats both the same way: False,
        # then exit 1. From the exit code alone, a broken setup and a
        # genuinely bad signature cannot be told apart.
        logging.error(f"Error during verification: {e}")
        return False


def main():
    """
    Main function to handle command-line arguments and perform signing/verification.
    """
    args = setup_argparse()

    if args.action == "sign":
        if not args.private_key:
            logging.error("Private key path is required for signing.")
            sys.exit(1)

        signature = sign_message(args.message, args.private_key, args.algorithm, args.hash_algorithm)

        # Output the signature to stdout (or save to a file if needed)
        # Careful: this prints hex text, while verify reads the
        # signature file as raw bytes. Saving this printout straight to
        # a file and verifying against it fails, because the hex has to
        # be decoded back to bytes first. The two ends do not match yet.
        print(signature.hex()) #Hex representation of the signature, suitable for storage/transfer


    elif args.action == "verify":
        if not args.public_key or not args.signature:
            logging.error("Public key path and signature path are required for verification.")
            sys.exit(1)

        # An invalid signature is a result a caller needs in the exit
        # code, not only in the log: exit 1 so scripts can branch on it.
        if not verify_message(args.message, args.public_key, args.signature, args.algorithm, args.hash_algorithm):
            sys.exit(1)


if __name__ == "__main__":
    main()