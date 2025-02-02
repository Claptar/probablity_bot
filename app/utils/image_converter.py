import re
import matplotlib.pyplot as plt
import logging
import os


def split_text_smart(text: str, line_length: int = 60) -> str:
    """
    Split text into lines of a certain length, while avoiding breaking LaTeX-style math equations
    Args:
        text (str): Text to split
        line_length (int, optional): Maximum line length. Defaults to 60.

    Returns:
        str: Splited text
    """
    matches = re.finditer(r"\$.*?\$", text)
    equation_spans = [match.span() for match in matches]

    check_loc = lambda loc, span: loc > span[0] and loc < span[1]

    valid_space_positions = [
        i
        for i, char in enumerate(text)
        if all(not check_loc(i, span) for span in equation_spans) and char == " "
    ]
    new_line_positions = [
        pos
        for i, pos in enumerate(valid_space_positions)
        if i > 0 and pos % line_length < valid_space_positions[i - 1] % line_length
    ]

    for pos in new_line_positions:
        text = text[:pos] + "\n" + text[pos + 1 :]
    return text


def render_math_image(text: str, output_file: str, dpi: int = 300):
    """
    Render a LaTeX-style math equation to an image
    Args:
        text (str): Math equation in LaTeX-style
        output_file (str): Output file path
        dpi (int, optional): Image resolution. Defaults to 300.
    """
    logging.info(f"Rendering text to image: {text}")
    plt.rcParams.update(
        {
            "text.usetex": False,  # Disable external LaTeX
            "mathtext.fontset": "stix",  # Use a built-in math font
            "font.family": "serif",
            "font.size": 14,
        }
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.text(0.5, 0.5, text, fontsize=14, ha="center", va="center", ma="left")
    ax.axis("off")

    plt.savefig(
        output_file, dpi=dpi, bbox_inches="tight", transparent=True, pad_inches=0.2
    )
    plt.close(fig)
    if os.path.getsize(output_file) == 0:
        logging.error("Rendered image file is empty")
        raise ValueError("Rendered image file is empty")
    else:
        logging.info(f"Image successfully saved to {output_file}")
