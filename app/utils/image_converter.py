import os
import shutil
import subprocess
import tempfile
from string import Template
import logging


def latex_to_png(latex_snippet, output_png="output.png"):
    """
    Convert a LaTeX snippet (string) into a cropped PNG
    Args:
        latex_snippet (str): LaTeX code to render
        output_png (str): Output PNG file path
    """
    # Create a minimal LaTeX document template.
    # Using the 'standalone' or 'preview' class helps produce tightly cropped output.
    doc_template = Template(r"""
    \documentclass[preview,border={0.5cm 2cm 0.5cm 2cm}]{standalone}
    \usepackage{amsmath,amssymb}
    \begin{document}
    \vspace*{1cm}  % Add vertical space at the top
    $latex_snippet
    \vspace*{1cm}  % Add vertical space at the top
    \end{document}
    """)
    latex_document = doc_template.substitute(latex_snippet=latex_snippet)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "temp.tex")
        pdf_name = "temp.pdf"

        # Write the LaTeX source to a temporary file
        with open(tex_path, "w") as f:
            f.write(latex_document)

        # Run pdflatex (or xelatex)
        # "--interaction=nonstopmode" avoids user prompts on errors
        subprocess.run(
            ["pdflatex", "--interaction=nonstopmode", tex_path],
            check=True,
            cwd=tmpdir
        )

        # Convert cropped PDF to PNG
        # "-density" can be adjusted for higher/lower resolution (e.g., 150, 300, 600)
        subprocess.run(
            ["pdftoppm", "-png", "-r", "300", pdf_name, 'output'],
            check=True,
            cwd=tmpdir
        )

        # Rename the output file to the desired name
        shutil.move(os.path.join(tmpdir, 'output-1.png'), output_png)

    logging.info(f"Converted LaTeX to PNG: {output_png}")
