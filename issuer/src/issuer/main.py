"""Main module, FastAPI runs from here"""
import asyncio
import base64
import os
import subprocess
import sys
from typing import Dict, Optional, Union
import redis.asyncio as redis
import hashlib
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pkcs11.exceptions import NoSuchKey
from pydantic import BaseModel
from python_x509_pkcs11.pkcs11_handle import PKCS11Session


async def pkcs11_startup() -> None:
    # Ensure pkcs11 env variables
    if (
        "PKCS11_MODULE" not in os.environ
        or "PKCS11_TOKEN" not in os.environ
        or "PKCS11_PIN" not in os.environ
    ):
        print("PKCS11_MODULE, PKCS11_TOKEN or PKCS11_PIN env variables is not set")
        sys.exit(1)

    # If SOFTHSM then create token if not exists
    if os.environ["PKCS11_BACKEND"] == "SOFTHSM":
        if not os.path.isdir("/var/lib/softhsm/tokens") or not os.listdir("/var/lib/softhsm/tokens"):
            subprocess.check_call(
                [
                    "softhsm2-util",
                    "--init-token",
                    "--slot",
                    "0",
                    "--label",
                    os.environ["PKCS11_TOKEN"],
                    "--pin",
                    os.environ["PKCS11_PIN"],
                    "--so-pin",
                    os.environ["PKCS11_PIN"],
                ]
            )


class CredentialRequest(BaseModel):
    name: str
    number: str

loop = asyncio.get_running_loop()
startup_task = loop.create_task(pkcs11_startup())

# Create fastapi app
app = FastAPI()

@app.post("/satosa/credential")
async def post_pkcs11_public_key_data(request: Request, credential_request: CredentialRequest) -> JSONResponse:

    # Fetch underlaying credential, driverslicense, diploma or whatever
    # data = fetch_underlaying_credential(subject_type, client_id, client_name)
    data = f"my_test_data_{credential_request.name}_{credential_request.number}"

    # Create vc credential
    sdjwt = {"credential": data}

    # store hash of data
    redis_con = redis.Redis(host="redis")
    hash_m = hashlib.sha256()
    hash_m.update(data.encode("utf-8"))
    await redis_con.set(f"data_{hash_m.hexdigest()}", "ok")

    # store hash of credential
    hash_m = hashlib.sha256()
    hash_m.update(json.dumps(sdjwt, indent=0).encode("utf-8"))
    await redis_con.set(f"sdjwt_{hash_m.hexdigest()}", "ok")

    # Return sdjwt to the satosa backend which will return it to the satosa frontend and then to the client (wallet)
    return JSONResponse({"status": "ok", "sdjwt": sdjwt})
