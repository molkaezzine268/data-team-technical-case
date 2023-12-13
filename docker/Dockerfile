# Base image
FROM python:3.11-slim AS base

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN mkdir -p \
        "/usr/local/lib/data-platform" \
        "/var/local/lib/data-platform" \
        "/var/log/data-platform" && \
    python -m "venv" "/usr/local/lib/data-platform"


ENV PATH="/usr/local/lib/data-platform/bin:${PATH}"

# Builder image
FROM base AS builder

RUN apt-get --yes update && \
    apt-get --yes install \
        "curl" \
        "unzip"

ENV PATH="/usr/local/bin:${PATH}"

RUN curl \
        --silent \
        --show-error \
        --location \
        --output "/tmp/duckdb_cli.zip" \
            "https://github.com/duckdb/duckdb/releases/download/v0.9.2/duckdb_cli-linux-amd64.zip" && \
    unzip \
        "/tmp/duckdb_cli.zip" \
        -d "/usr/local/bin" && \
    rm "/tmp/duckdb_cli.zip"

RUN curl \
        --silent \
        --show-error \
        --location \
            "https://pdm-project.org/install-pdm.py" | \
    python "-" --path "/usr/local/lib/pdm" && \
    ln --symbolic "/usr/local/lib/pdm/bin/pdm" "/usr/local/bin/pdm"

COPY ["./app/pyproject.toml", "./app/pdm.lock", "/tmp/data-platform/app/"]
RUN cd "/tmp/data-platform/app" && \
    touch "README.md" && \
    pdm use -f "/usr/local/lib/data-platform" && \
    pdm sync --no-editable --no-self --prod

COPY ["./app/src", "/tmp/data-platform/app/src"]
RUN cd "/tmp/data-platform/app" && \
    mkdir -p "src/jump/data_platform/dbt_project/dbt_packages" && \
    touch "src/jump/data_platform/dbt_project/dbt_packages/.keep" && \
    pdm sync --no-editable --prod


FROM base

ARG UID
ARG GID
RUN groupadd -g "${GID}" -o "data-platform" && \
    useradd -m -u "${UID}" -g "${GID}" -o -s "/bin/bash" -d "/var/local/lib/data-platform" "data-platform" && \
    chown -R "data-platform:data-platform" \
        "/var/local/lib/data-platform" \
        "/var/log/data-platform"

WORKDIR "/var/local/lib/data-platform"

COPY --from=builder ["/usr/local/bin/duckdb", "/usr/local/bin/duckdb"]
COPY --from=builder ["/usr/local/lib/data-platform", "/usr/local/lib/data-platform"]

USER "data-platform"
ENV PATH="/usr/local/lib/data-platform/bin:${PATH}"
RUN data-platform --version && \
    duckdb --version && \
    dbt --version

ENTRYPOINT ["data-platform"]
CMD ["extract", "load", "transform"]