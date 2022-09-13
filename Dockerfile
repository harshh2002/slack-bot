FROM python:3.10
RUN apt update -y
RUN pip install poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .
EXPOSE 5000
CMD ["poetry", "run", "python3", "bot.py"]