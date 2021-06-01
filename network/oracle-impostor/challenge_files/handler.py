import random
import socket
import string
import os.path

SECRET_SIZE = 128

FLAG_PATH = "/code/flag.txt"


def handle_connection(sock: socket.socket) -> None:
    # who even needs buffering?
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

    # generate our secret
    #   Let's make sure to use a secure prng.
    #   Messing this up would be really embarrassing, ha.
    #   (Note: Breaking the PRNG is *not* part of the challenge)
    prng = random.SystemRandom()
    random_data = generate_secret(prng)

    timeout_counter = 0

    while True:
        try:
            sock.send(
                b"I'm only talking to the real oracle. "
                b"Prove that you're the oracle by predicting my secret.\n",
            )

            # don't want to give these oracle impostors too much time to think
            sock.settimeout(10)

            received = sock.recv(300)
            if received == random_data:
                if os.path.isfile(FLAG_PATH):
                    with open("/code/flag.txt", "r") as f:
                        flag = f.read().strip()
                else:
                    flag = "CSCG{FLAG_FILE_MISSING}"
                sock.send(f"Nice, here's your flag: {flag}\n".encode())
                return
            else:
                sock.send(
                    b"IMPOSTOR! "
                    b"The real oracle would have known that the secret was:\n",
                )

                # drumroll
                for i in range(10):
                    sock.send(b"+" + b"#" * 998 + b"=")

                sock.send(b"-" * 1000 + b"SECRET=[" + random_data + b"]\n")

                sock.send(b"If you're the real oracle, then try again.\n")

                # generate a new secret
                random_data = generate_secret(prng)

        except socket.timeout:
            timeout_counter += 1
            if timeout_counter > 3:
                return

            sock.settimeout(60)
            sock.send(b"Too slow, too slow! Try again.\n")


def generate_secret(prng: random.Random) -> bytes:
    return "".join(
        [prng.choice(string.ascii_letters) for _ in range(SECRET_SIZE)]
    ).encode()
