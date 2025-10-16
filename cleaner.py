import pandas as pd
import io

def reading_words(content: bytes):

    df = pd.read_csv(io.BytesIO(content),header = None)
    keyword = df[0].astype(str).tolist()
    return keyword


def clean_words(keyword: list[str]):
    cleaned = []
    for k in keyword:
        k = k.strip().lower()
        if k and k not in cleaned:
            cleaned.append(k)
    return cleaned

