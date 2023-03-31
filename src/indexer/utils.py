def str_to_felt(text):
    b_text = bytes(text, "ascii")
    return int.from_bytes(b_text, "big")


def felt_to_str(int):
    b_int = int.to_bytes(32, "big")
    return str(b_int, "ascii")


def get_key_by_value(v, dict):
    for key, value in dict.items():
        if value == v:
            return key
    return None
