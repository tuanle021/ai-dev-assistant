def load_text_file(file_path: str) -> str:
    """
    Reads a text or markdown file and returns raw text.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()