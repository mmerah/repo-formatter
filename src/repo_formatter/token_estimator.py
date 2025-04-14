# Basic token estimation (can be replaced with tiktoken later)

def estimate_tokens(text: str) -> int:
    """
    Provides a very rough estimate of token count.
    A common rule of thumb is ~4 characters per token.
    """
    # Simple character-based estimate
    estimated_tokens = len(text) / 4

    # Alternative: Word count based estimate (often closer)
    # word_count = len(text.split())
    # estimated_tokens = word_count * 1.3 # Adjust multiplier as needed

    return int(estimated_tokens)

# Example using tiktoken (if installed)
# import tiktoken
# def estimate_tokens_tiktoken(text: str, encoding_name: str = "cl100k_base") -> int:
#     """Estimates tokens using tiktoken library."""
#     try:
#         encoding = tiktoken.get_encoding(encoding_name)
#         num_tokens = len(encoding.encode(text))
#         return num_tokens
#     except Exception as e:
#         print(f"Warning: tiktoken estimation failed ({e}). Falling back to basic estimation.")
#         return estimate_tokens(text)