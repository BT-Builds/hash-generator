# Hash Generator API

Generate cryptographic hashes (MD5, SHA1, SHA256, SHA384, SHA512) via HTTP API.

## Endpoints

### POST /hash
Generate hashes for text input.

**Request:**
```json
{
  "text": "hello world",
  "algorithms": ["md5", "sha256", "sha512"]
}
```

**Response:**
```json
{
  "input": "hello world",
  "hashes": {
    "md5": "5eb63bbbe01eeed791a8c292d0a95f17",
    "sha256": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde",
    "sha512": "..."
  }
}
```

**Curl:**
```bash
curl -X POST https://<slug>.vercel.app/hash \
  -H "Content-Type: application/json" \
  -H "X-API-Key: free-demo-key" \
  -d '{"text": "hello world", "algorithms": ["md5", "sha256"]}'
```

### GET /health
Health check endpoint (no auth required).

**Response:**
```json
{"status": "ok", "timestamp": "2024-01-01T00:00:00.000000"}
```

## Authentication

- Header: `X-API-Key`
- Free tier: 60 requests/minute
- Default key: `free-demo-key`

## Supported Algorithms

- md5
- sha1
- sha256
- sha384
- sha512

## Postman
[![Run in Postman](https://run.pstmn.io/button.svg)](https://raw.githubusercontent.com/BT-Builds/hash-generator/main/postman_collection.json)
