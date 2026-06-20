from groq import Groq
from decouple import config

client = Groq(api_key=config('GROQ_API_KEY'))


def validate_answer(expected_answer, submitted_answer):
    prompt = f"""You are checking a DSA competition answer.

Expected answer: {expected_answer}
Submitted answer: {submitted_answer}

Are these semantically the same answer? Reply with ONLY "CORRECT" or "INCORRECT", nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    result = response.choices[0].message.content.strip().upper()
    return result == "CORRECT"