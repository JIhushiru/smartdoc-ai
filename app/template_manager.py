TEMPLATE_KEYWORDS = {
    "invoice": ["invoice number", "billing address", "total due"],
    "resume": ["education", "experience", "skills"],
    "contract": ["terms and conditions", "agreement", "signature"],
    "receipt": ["item", "subtotal", "vat", "total"],
}


def detect_template(text: str) -> str | None:
    """
    Heuristically match document text to known template types based on keyword presence.
    """
    text_lower = text.lower()
    for template, keywords in TEMPLATE_KEYWORDS.items():
        if all(keyword in text_lower for keyword in keywords):
            return template
    return None
