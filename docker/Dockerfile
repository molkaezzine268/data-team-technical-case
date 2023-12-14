# Base image
FROM python:3.11-slim AS base

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN mkdir -p \
        "/usr/local/lib/data-platform" \
        "/var/local/lib/data-platform" \
        "/var/log/data-platform" && \
    python -m "venv" "/usr/local/lib/data-platform/venv"

# Builder image
FROM base AS builder

ARG DUCKDB_VERSION="0.9.2"

RUN apt-get --yes update && \
    apt-get --yes install \
        "curl" \
        "unzip" \
        "git" \
        "g++" \
        "cmake" \
        "libssl-dev" 


ENV PATH="/usr/local/bin:${PATH}"

RUN curl \
        --silent \
        --show-error \
        --location \
        --output "/tmp/duckdb_cli.zip" \
            "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-amd64.zip" && \
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

ENV PATH="/usr/local/lib/data-platform/venv/bin:${PATH}"

COPY ["./cli/pyproject.toml", "./cli/pdm.lock", "/tmp/data-platform/cli/"]
RUN cd "/tmp/data-platform/cli" && \
    touch "README.md" && \
    pdm use -f "/usr/local/lib/data-platform/venv" && \
    pdm sync --no-editable --no-self --prod

COPY ["./cli/src", "/tmp/data-platform/cli/src"]
RUN cd "/tmp/data-platform/cli" && \
    pdm sync --no-editable --prod

COPY ["./dbt", "/usr/local/lib/data-platform/dbt"]
RUN cd "/usr/local/lib/data-platform/dbt" && \
    dbt deps

FROM base

ARG UID
ARG GID
RUN groupadd -g "${GID}" -o "data-platform" && \
    useradd -m -u "${UID}" -g "${GID}" -o -s "/bin/bash" -d "/var/local/lib/data-platform" "data-platform" && \
    chown -R "data-platform:data-platform" \
        "/var/local/lib/data-platform" \
        "/var/log/data-platform"

WORKDIR "/var/local/lib/data-platform"

COPY ["./docker/data-platform", "/usr/local/bin/data-platform"]
COPY --from=builder ["/usr/local/bin/duckdb", "/usr/local/bin/duckdb"]
COPY --from=builder ["/usr/local/lib/data-platform", "/usr/local/lib/data-platform"]

USER "data-platform"

RUN data-platform --version

ENTRYPOINT ["data-platform"]
CMD ["extract", "load", "transform"]