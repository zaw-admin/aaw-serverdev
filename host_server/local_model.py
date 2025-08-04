import os
from functools import lru_cache
from transformers import pipeline

MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")


@lru_cache(maxsize=1)
def get_pipeline():
    return pipeline("text-generation", model=MODEL_NAME)


def analyze_code(code: str) -> str:
    pipe = get_pipeline()
    prompt = f"Analyze the following code:\n{code}\nAnalysis:"
    result = pipe(prompt, max_new_tokens=128)
    generated = result[0]["generated_text"][len(prompt):]
    return generated.strip()
