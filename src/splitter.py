def split_text(text, max_length):
    """
    Splits input text into chunks of `max_length` characters.
    This is necessary because LLMs have input token limits and perform better
    with smaller, focused prompts.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]