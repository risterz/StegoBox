#!/usr/bin/env python3
import argparse
import os
import sys
import struct
import zipfile
import io
import getpass

from PIL import Image

# === Optional crypto (LSB only) ===
from base64 import urlsafe_b64encode
from hashlib import sha256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # type: ignore
from cryptography.hazmat.primitives import hashes  # type: ignore
from cryptography.hazmat.backends import default_backend  # type: ignore
from cryptography.fernet import Fernet  # type: ignore
import secrets

APPEND_MAGIC = b"STEGOBX\x00APPEND\x00"
LSB_MAGIC = b"STEGOBX\x00LSB\x00"
VERSION = 1

# ---------- Utilities ----------
def read_password(prompt="Password: ", confirm=False):
    pw = os.environ.get("STEGOBOX_PASSWORD")
    if pw:
        return pw
    pw1 = getpass.getpass(prompt)
    if confirm:
        pw2 = getpass.getpass("Confirm password: ")
        if pw1 != pw2:
            print("Passwords do not match.", file=sys.stderr)
            sys.exit(1)
    return pw1

def zip_folder_to_bytes(folder_path: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for f in files:
                full = os.path.join(root, f)
                arc = os.path.relpath(full, start=folder_path)
                zf.write(full, arcname=arc)
    return buf.getvalue()

def load_payload(input_folder: str = None, input_zip: str = None) -> bytes:
    if input_zip:
        with open(input_zip, "rb") as f:
            return f.read()
    elif input_folder:
        return zip_folder_to_bytes(input_folder)
    else:
        raise ValueError("Provide --input-folder or --input-zip")

# ---------- Append mode ----------
def append_embed(cover_path: str, payload: bytes, out_path: str):
    with open(cover_path, "rb") as f:
        cover = f.read()
    # structure: [cover][payload][footer]
    footer = APPEND_MAGIC + struct.pack("<I", VERSION) + struct.pack("<Q", len(payload))
    stego = cover + payload + footer
    with open(out_path, "wb") as f:
        f.write(stego)

def append_extract(stego_path: str, out_zip: str):
    with open(stego_path, "rb") as f:
        data = f.read()
    # scan footer from end
    if APPEND_MAGIC not in data:
        raise ValueError("No append footer found.")
    idx = data.rfind(APPEND_MAGIC)
    footer = data[idx:]
    # footer = MAGIC + u32 version + u64 payload_len
    if len(footer) < len(APPEND_MAGIC) + 4 + 8:
        raise ValueError("Corrupt footer.")
    magic = footer[:len(APPEND_MAGIC)]
    version = struct.unpack("<I", footer[len(APPEND_MAGIC):len(APPEND_MAGIC)+4])[0]
    payload_len = struct.unpack("<Q", footer[len(APPEND_MAGIC)+4:len(APPEND_MAGIC)+12])[0]
    payload_start = len(data) - (len(APPEND_MAGIC) + 4 + 8) - payload_len
    payload = data[payload_start:payload_start+payload_len]
    with open(out_zip, "wb") as f:
        f.write(payload)

# ---------- Crypto helpers (LSB) ----------
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend(),
    )
    key = urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    return key

def encrypt_payload(password: str, payload: bytes) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(payload)
    # package: salt_len(1) + salt + token_len(8) + token
    return b"\x10" + salt + struct.pack("<Q", len(token)) + token

def decrypt_payload(password: str, blob: bytes) -> bytes:
    if len(blob) < 1 + 16 + 8:
        raise ValueError("Corrupt encrypted blob.")
    salt_len = blob[0]
    if salt_len != 16:
        raise ValueError("Unsupported salt length.")
    salt = blob[1:1+salt_len]
    token_len = struct.unpack("<Q", blob[1+salt_len:1+salt_len+8])[0]
    token = blob[1+salt_len+8:1+salt_len+8+token_len]
    key = derive_key(password, salt)
    return Fernet(key).decrypt(token)

# ---------- Bit packing helpers ----------
def bytes_to_bits(b: bytes):
    for byte in b:
        for i in range(8):
            yield (byte >> (7 - i)) & 1

def bits_to_bytes(bits_iter, total_bits: int) -> bytes:
    out = bytearray()
    cur = 0
    cnt = 0
    for _ in range(total_bits):
        bit = next(bits_iter)
        cur = (cur << 1) | bit
        cnt += 1
        if cnt == 8:
            out.append(cur)
            cur = 0
            cnt = 0
    if cnt != 0:
        out.append(cur << (8 - cnt))
    return bytes(out)

# ---------- LSB core ----------
def lsb_capacity(img: Image.Image) -> int:
    # capacity in bits: num_pixels * channels (use RGB 3 channels) * 1 bit
    w, h = img.size
    return w * h * 3

def lsb_embed(cover_path: str, payload: bytes, out_path: str, password: str = None):
    img = Image.open(cover_path).convert("RGB")
    w, h = img.size
    px = img.load()

    # Build payload: MAGIC | VERSION | enc_flag(1) | total_len(4) | data
    if password:
        data = encrypt_payload(password, payload)
        enc_flag = b"\x01"
    else:
        data = payload
        enc_flag = b"\x00"

    header = LSB_MAGIC + struct.pack("<I", VERSION) + enc_flag + struct.pack("<I", len(data))
    blob = header + data

    required_bits = len(blob) * 8
    cap = lsb_capacity(img)
    if required_bits > cap:
        raise ValueError(f"Payload too large for this image. Need {required_bits} bits, have {cap} bits.")

    bitstream = bytes_to_bits(blob)
    # Write across pixels row-major
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            try:
                r = (r & 0xFE) | next(bitstream)
                g = (g & 0xFE) | next(bitstream)
                b = (b & 0xFE) | next(bitstream)
            except StopIteration:
                px[x, y] = (r, g, b)
                img.save(out_path, format="PNG")
                return
            px[x, y] = (r, g, b)

    img.save(out_path, format="PNG")

def lsb_extract(stego_path: str, out_zip: str, password: str = None):
    img = Image.open(stego_path).convert("RGB")
    w, h = img.size
    px = img.load()

    # Read bits into bytes progressively, first enough to parse header
    # Header lengths:
    # LSB_MAGIC(len) + 4(version) + 1(enc_flag) + 4(total_len)
    header_len = len(LSB_MAGIC) + 4 + 1 + 4
    header_bits = header_len * 8

    def pixel_bits():
        for y in range(h):
            for x in range(w):
                r, g, b = px[x, y]
                yield r & 1
                yield g & 1
                yield b & 1

    gen = pixel_bits()
    header_bytes = bits_to_bytes(gen, header_bits)

    if not header_bytes.startswith(LSB_MAGIC):
        raise ValueError("No LSB payload found (magic mismatch).")

    offset = len(LSB_MAGIC)
    version = struct.unpack("<I", header_bytes[offset:offset+4])[0]
    offset += 4
    enc_flag = header_bytes[offset]
    offset += 1
    total_len = struct.unpack("<I", header_bytes[offset:offset+4])[0]
    offset += 4

    data_bits = total_len * 8
    data_bytes = bits_to_bytes(gen, data_bits)

    if enc_flag == 1:
        if not password:
            raise ValueError("Password required to decrypt.")
        data = decrypt_payload(password, data_bytes)
    else:
        data = data_bytes

    with open(out_zip, "wb") as f:
        f.write(data)

# ---------- CLI ----------
def main():
    p = argparse.ArgumentParser(prog="StegoBox", 
                               description="Hide and extract ZIPs in images (append or LSB). Created by @Risterz")
    sub = p.add_subparsers(dest="cmd", required=True)

    # append-embed
    a1 = sub.add_parser("append-embed", help="Append ZIP to cover image with footer marker.")
    a1.add_argument("--cover", required=True, help="Cover image path (any format).")
    g = a1.add_mutually_exclusive_group(required=True)
    g.add_argument("--input-folder", help="Folder to zip and embed.")
    g.add_argument("--input-zip", help="Existing ZIP to embed.")
    a1.add_argument("--out", required=True, help="Output stego image (e.g., stego.png).")

    # append-extract
    a2 = sub.add_parser("append-extract", help="Extract appended ZIP from stego image.")
    a2.add_argument("--stego", required=True, help="Stego image path.")
    a2.add_argument("--out", required=True, help="Output ZIP path.")

    # lsb-embed
    l1 = sub.add_parser("lsb-embed", help="Embed ZIP via LSB (PNG/BMP recommended).")
    l1.add_argument("--cover", required=True, help="Cover image path (use PNG/BMP for safety).")
    g2 = l1.add_mutually_exclusive_group(required=True)
    g2.add_argument("--input-folder", help="Folder to zip and embed.")
    g2.add_argument("--input-zip", help="Existing ZIP to embed.")
    l1.add_argument("--out", required=True, help="Output stego image (PNG will be used).")
    l1.add_argument("--password", help="Optional password (if omitted, you'll be prompted).")

    # lsb-extract
    l2 = sub.add_parser("lsb-extract", help="Extract LSB-embedded ZIP.")
    l2.add_argument("--stego", required=True, help="Stego image path.")
    l2.add_argument("--out", required=True, help="Output ZIP path.")
    l2.add_argument("--password", help="Password if encryption was used (will prompt if missing).")

    args = p.parse_args()

    try:
        if args.cmd == "append-embed":
            payload = load_payload(args.input_folder, args.input_zip)
            append_embed(args.cover, payload, args.out)
            print(f"[OK] Appended payload into: {args.out}")

        elif args.cmd == "append-extract":
            append_extract(args.stego, args.out)
            print(f"[OK] Extracted ZIP to: {args.out}")

        elif args.cmd == "lsb-embed":
            payload = load_payload(args.input_folder, args.input_zip)
            pw = args.password
            if pw is None:
                choice = input("Encrypt with password? [y/N]: ").strip().lower()
                if choice == "y":
                    pw = read_password(confirm=True)
            lsb_embed(args.cover, payload, args.out, password=pw)
            print(f"[OK] LSB embedded into: {args.out}")

        elif args.cmd == "lsb-extract":
            pw = args.password
            # defer prompt only if needed
            try:
                lsb_extract(args.stego, args.out, password=pw)
            except ValueError as e:
                msg = str(e)
                if "Password required" in msg and pw is None:
                    pw = read_password()
                    lsb_extract(args.stego, args.out, password=pw)
                else:
                    raise
            print(f"[OK] Extracted ZIP to: {args.out}")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()