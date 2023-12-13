# Usage

```bash
docker-compose up -d

```

## How to do a wallet test request to the satosa, which in turn will fetch a credential from the issuer

```bash
curl -vk -X POST localhost:8085/wallet -H 'Content-Type: application/json' -d '{"subject_type": "sunet_wallet", "client_id": "35345", "client_name": "VictorNaslund", "client_number": "09834759"}'

```

## See the logs

```bash
docker logs vc_satosa
docker logs vc_issuer

```