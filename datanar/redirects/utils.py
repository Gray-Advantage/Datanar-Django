import hashlib

from sqids import Sqids

from redirects.models import Redirect

sqids = Sqids()

MAX_GENERATION_ATTEMPTS = 200


def generate_short_link(long_link: str) -> str:
    if not isinstance(long_link, str):
        msg = "long_link must be a string"
        raise TypeError(msg)

    for i in range(MAX_GENERATION_ATTEMPTS):
        temp_string = f"{long_link}{i}" if i > 0 else long_link
        hash_object = hashlib.sha256(temp_string.encode())
        number = int.from_bytes(hash_object.digest(), byteorder="big")
        short_link = sqids.encode(list(map(int, list(str(number)))))[:5]
        if not Redirect.objects.get_by_short_link(short_link):
            return short_link

    msg = "Error generating short link"
    raise RuntimeError(msg)


__all__ = ["generate_short_link"]
