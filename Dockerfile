# Builder image
FROM python:3-alpine as builder
RUN apk add --no-cache \
    ca-certificates \
    ffmpeg \
    openssl \
    aria2 \
    g++ \
    git \
    py3-cffi \
    libffi-dev \
    zlib-dev
RUN pip install poetry
WORKDIR /builder
COPY pyproject.toml poetry.lock ./
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \ 
    poetry install --no-interaction

# Final image
FROM python:3-alpine as runner
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /bot
COPY . .
EXPOSE 5000
CMD ["python3", "bot.py"]