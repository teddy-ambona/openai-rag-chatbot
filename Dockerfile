FROM python:3.11

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
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install wheel poetry==1.8.2

COPY poetry.lock pyproject.toml ./

# Install required libraries in the virtual environment
RUN poetry install --no-root

# Python won’t try to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure that the stdout and stderr streams are sent straight to terminal
ENV PYTHONUNBUFFERED 1

# Copy python files
COPY src ./src
COPY data ./data

# Using non-root user to reduce vulnerabilities
USER app

CMD ["python", "src/server.py"]
