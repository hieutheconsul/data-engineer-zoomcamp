FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
# to copy file from another environment eg the virtual env

RUN pip install pandas pyarrow

WORKDIR /code
# to define the directory after running the docker

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

COPY ingest_data.py .
# # to copy file from local/host

ENTRYPOINT ["uv", "run", "python", "ingest_data.py" ] 
# to run this file automatically when we run the docker