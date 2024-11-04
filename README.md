# food-tracker-backend-2

```bash
food-tracker-backend-2$ docker-compose up
food-tracker-backend-2$ sam build
food-tracker-backend-2$ sam local start-api
food-tracker-backend-2/scripts$ sh create-populate-db.sh
DYNAMO_ENDPOINT=http://192.168.1.135:8000 dynamodb-admin
```

Bot
```bash
ssh -p 443 -R0:localhost:8025 a.pinggy.io
curl -F "url=<URL>/bot" https://api.telegram.org/bot<TOKEN>/setWebhook
```

### Errores
- Ver que la BD se conecta al puerto correcto ``ifconfig | grep 192.``
- Posible problema con docker hacer PRUNE de todo