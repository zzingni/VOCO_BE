import re
from collections import Counter
from sqlalchemy.orm import Session

from app.models.repeated_word import RepeatedWord


def tokenize(text: str):
    return re.findall(r"\w+", text.lower())


def extract_word_counts(text: str):
    words = tokenize(text)
    return Counter(words)


def save_repeated_words(db: Session, answer_id: int, text: str, min_count: int = 3):
    counter = extract_word_counts(text)

    for word, count in counter.items():
        # ✔️ 여기 핵심 조건 추가
        if count < min_count:
            continue

        db_word = RepeatedWord(
            answer_id=answer_id,
            word=word,
            word_count=count
        )
        db.add(db_word)

    db.commit()