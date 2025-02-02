# Use an official Python runtime as a parent image
FROM python:3.11-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install the minimal LaTeX distribution and poppler-utils
#   texlive-latex-base: Minimal TeX Live for basic latex -> PDF
#   poppler-utils: for pdftoppm (PDF -> image conversions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-base \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies using pip from the setup.py and requirements.txt
RUN pip install --upgrade pip \
    && pip install setuptools \
    && pip install .


# Set ENTRYPOINT to our script
RUN chmod +x /app/docker/entrypoint.sh
ENTRYPOINT ["/app/docker/entrypoint.sh"]

# Run the application when the container starts
CMD ["python", "app.py"]