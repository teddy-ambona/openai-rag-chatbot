FROM --platform=linux/amd64 python:3.11 as base

# Create app user
RUN groupadd -r user && useradd -r -g user --create-home app
RUN chown -R app /home/app
RUN mkdir -v /app && chown -R app /app

WORKDIR /app

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    make \
    curl \
    jq && \
    apt-get clean

# Create virtual environment and activate it
RUN pip install wheel pipx
RUN pipx install poetry
ENV PATH="/root/.local/bin:${PATH}"

COPY poetry.lock pyproject.toml ./

# Install required libraries
RUN poetry install --no-root
ENV PATH="/app/venv/bin:$PATH"

# Python won’t try to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure that the stdout and stderr streams are sent straight to terminal
ENV PYTHONUNBUFFERED 1

# Copy python files
COPY src ./

# Using non-root user to reduce vulnerabilities
USER app

ENTRYPOINT ["python", "src/serve.py"]
