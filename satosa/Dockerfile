FROM debian:bookworm-20231120-slim@sha256:93ff361288a7c365614a5791efa3633ce4224542afb6b53a1790330a8e52fc7d

MAINTAINER victor@sunet.se

EXPOSE 8085/tcp

# Metadata
LABEL version="1.03"
LABEL description="vc_satosa"

# Set work dir
WORKDIR /app


WORKDIR /app/satosa

# Install deps
RUN apt-get update \
    && apt-get install -y \
    python3-pip \
    python3 \
    build-essential \
    wget \
    xmlsec1 \
    dnsutils \
    python3-venv \
    git \
    curl


# Add user and add to softhsm group
RUN useradd satosa -u 1500 -s /usr/sbin/nologin


# Copy files
# COPY ./satosa/backend/wallet.py /app/SATOSA/src/satosa/backends/wallet.py
ADD ./satosa/oidc_oidc /app/satosa
ADD ./satosa/satosa-static-ds /app/satosa/satosa-static-ds

RUN chown -R satosa ./

USER satosa

RUN python3 -m venv .venv
# RUN bash -c '. .venv/bin/activate && pip3 install --upgrade satosa gunicorn idpyoidc satosa_oidcop'
RUN bash -c '. .venv/bin/activate && pip3 install --upgrade satosa gunicorn'
RUN bash -c '. .venv/bin/activate && git clone https://github.com/IdentityPython/idpy-oidc.git && cd idpy-oidc && git checkout id_assurance && pip3 install ./'
RUN bash -c '. .venv/bin/activate && git clone https://github.com/UniversitaDellaCalabria/SATOSA-oidcop.git && cd SATOSA-oidcop && git checkout key_val_store && pip3 install ./'

USER root
ADD ./satosa/satosa_sunet_wallet /app/satosa/satosa_sunet_wallet
RUN chown -R satosa ./
USER satosa
RUN . .venv/bin/activate && cd satosa_sunet_wallet && pip3 install ./ && cd ../satosa-static-ds && pip3 install ./

USER root
# Remove setuid and setgid
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

USER satosa

# Add healthcheck
# HEALTHCHECK --interval=120s --timeout=15s --retries=1 --start-period=30s \
#     CMD sh '. .venv/bin/activate && healthcheck.sh' || bash -c 'kill -s 15 1 && (sleep 7; kill -s 9 1)'

# CMD sh -c '. .venv/bin/activate && gunicorn -b0.0.0.0:8080 satosa.wsgi:app --keyfile=private-key.pem --certfile=cert.pem'
CMD sh -c '. .venv/bin/activate && gunicorn -b0.0.0.0:8085 satosa.wsgi:app'

# FIx letsencrypt cert and keyfile
