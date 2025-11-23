#!/usr/bin/env python3
import os
import pathlib
from dotenv import load_dotenv
from tqdm import tqdm
from google import genai
from google.genai import types

# Load .env variables and initialize Gemini client
load_dotenv()
client = genai.Client()

# List of paragraphs to process
paragraphs = [
    '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10', '1.11', '1.12',
    '2.1', '2.2', '2.3', '2.4', '2.5',
    '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11',
    '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9',
    '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11',
    '6.1', '6.2', '6.3', '6.4', '6.5',
    '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10',
    '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9',
    '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10',
    '10.1', '10.2', '10.3', '10.4', '10.5', '10.6', '10.7', '10.8', '10.9',
    '11.1', '11.2', '11.3', '11.4', '11.5', '11.6', '11.7', '11.8', '11.9',
    '12.1', '12.2', '12.3', '12.4', '12.5', '12.6', '12.7'
]

# Process each paragraph
for paragraph in tqdm(paragraphs):
    i, k = paragraph.split('.')

    # Retrieve and encode the PDF byte
    filepath = pathlib.Path(f'data/pdfs/section{i}.pdf')

    # Upload the PDF using the File API
    sample_file = client.files.upload(
    file=filepath,
    )

    # Generate markdown content from the uploaded PDF
    prompt = f"Convert the sub-section {paragraph} in this document to markdown format. Make sub-section title to be the first level headers and paragraph titles within subsection to be the second level headers. Exercises section should be 2nd level header and each exercise must have start and end markers. Theorems, examples, definitions, tables and other numbered items must contain start and end markers with their number, e.g., <<Theorem 2.1>> ... <</Theorem 2.1>>. Remove page headers and footers. Use latex syntax for all math expressions"
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[sample_file, prompt]
    )

    # Save the generated markdown to a file
    os.makedirs("data/parsed", exist_ok=True)
    with open(f"data/parsed/paragraph{paragraph}.md", "w") as f:
        f.write(response.text)
