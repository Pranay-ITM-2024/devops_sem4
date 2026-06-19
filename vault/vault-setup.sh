#!/bin/bash
# Store secrets in Vault
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='root-token'

echo "📦 Storing SOC app secrets in Vault..."

vault kv put secret/soc-app \
    db_user="socuser" \
    db_password="socpass123" \
    db_name="soc_db" \
    jwt_secret="my-super-secret-jwt-key" \
    flask_secret="flask-production-secret"

echo "✅ Secrets stored. Verifying..."
vault kv get secret/soc-app

echo "🔑 Done! Secrets are now managed by Vault."
