# syntax=docker/dockerfile:1
FROM debian:trixie-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# The pinned PowerShell archive below is x86-64. Use --platform linux/amd64.
ARG TARGETARCH
ARG KOTLIN_VERSION=2.1.21
ARG KOTLIN_SHA256=1ba08a8b45da99339a0601134cc037b54cf85e9bc0edbe76dcbd27c2d684a977
ARG POWERSHELL_VERSION=7.5.4
ARG POWERSHELL_SHA256=1fd7983fe56ca9e6233f126925edb24bf6b6b33e356b69996d925c4db94e2fef
ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/opt/kotlinc/bin:/opt/venv/bin:/opt/powershell:${PATH}" \
    PYTHONUNBUFFERED=1 \
    POWERSHELL_TELEMETRY_OPTOUT=1 \
    DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    GOTOOLCHAIN=local

RUN test "${TARGETARCH:-amd64}" = amd64 \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl unzip python3 python3-venv nodejs golang-go \
       ruby rustc gcc libc6-dev php-cli lua5.4 perl openjdk-21-jdk-headless ghc libffi-dev libnuma-dev strace \
       libicu76 libssl3t64 libgssapi-krb5-2 libunwind8 zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/powershell \
    && curl --fail --location --retry 3 \
       "https://github.com/PowerShell/PowerShell/releases/download/v${POWERSHELL_VERSION}/powershell-${POWERSHELL_VERSION}-linux-x64.tar.gz" \
       --output /tmp/powershell.tar.gz \
    && echo "${POWERSHELL_SHA256}  /tmp/powershell.tar.gz" | sha256sum --check --strict \
    && tar -xzf /tmp/powershell.tar.gz -C /opt/powershell \
    && chmod +x /opt/powershell/pwsh \
    && rm /tmp/powershell.tar.gz \
    && curl --fail --location --retry 3 \
       "https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/kotlin-compiler-${KOTLIN_VERSION}.zip" \
       --output /tmp/kotlin.zip \
    && echo "${KOTLIN_SHA256}  /tmp/kotlin.zip" | sha256sum --check --strict \
    && unzip -q /tmp/kotlin.zip -d /opt \
    && rm /tmp/kotlin.zip \
    && python3 -m venv /opt/venv

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

# Fail the image build if any runtime is missing or any emitted program fails.
RUN python test.py --require-all && python test_strategies.py --require-all
CMD ["python", "test_strategies.py", "--require-all"]
