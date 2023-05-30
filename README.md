# Flowo

Jedná se o hlavní aplikaci systému pro řízení digiralizace knih MZK,
skládající se ze dvou částí, jádra a uživatelského rozhraní. Jádro
se stará o samotné workflow, tedy primárně volání API dotazů nad všemi aplikacemi, které
nastavené workflow zahrnuje. Jádro také poskytuje REST API, pomocí kterého se mohou
řídit nejen jednotlivé procesy, ale také například získávat statistiky. Uživatelské rozhraní
slouží hlavně k jednoduché a přehledné správě záznamů celého procesu digitalizace

## Používání docker-compose

Flowo implementované tak, aby běželo jako docker container. Je zde tedy obsažen docker-compose,
pomocí kterého lze Flowo jak překládat, tak spouštět. Následující kapitoly popisují jak správně
přeložit nebo spustit tento systém.

## Jak spustit docker-compsoe

1. [Nainstalovat docker-compose](https://docs.docker.com/compose/install/)
1. Nahranit potřebnou konfiguraci v `docker-compose.yml`
1. Spustit Rope pomocí `make up` v adresáři Rope.
1. Vytvořit docker image pomocí `docker-compose build` v adresáři Flowo.
1. Spustit Flowo pomocí `docker-compose up -d` v adresáři Flowo.

Nyní bude frontend dostupný na adrese localhost:3000/ a backend na adrese localhost:8000/.
Základní přihlašovací jméno je `flowoAdmin`.
Základní přihlašovací heslo je `flowoAdmin`.

### Příklad docker-compose

```yaml
version: '2'

services:
  api:
    build: ./    
    ports:
      - "8000:8000"
    command:
      - /bin/sh
      - -c
      - |
        celery -A flowo worker --loglevel=INFO --detach
        python3 manage.py runserver api:8000
    container_name: api
    networks:
      - reactdrf
    volumes:
      - /mnt/:/nf/
      - ./flowo_db/db.sqlite3:/db.sqlite3
    environment:
      - PA_USERNAME={ZMENIT_JMENO_PA_UZIVATELE}
      - PA_PASSWORD={ZMENIT_HESLO_PA_UZIVATELE}
      - PATH_TO_FLOWO_DIR={ZMENIT_CESTU_K_FLOWO_SOUBORUM}
      - PATH_TO_PA_IMPORT_DIR={ZMENIT_CESTU_K_PA_SOUBORUM}
      - PA_URL={ZMENIT_URL_NA_PROARC}
      - ROPE_URL={ZMENIT_URL_NA_ROPE}
    extra_hosts:
      - "host.docker.internal:host-gateway"
  web:
    build: ./frontend
    ports:
      - "3000:3000"
    container_name: web
    stdin_open: true
    networks:
      - reactdrf
  rabbitmq:
    image: rabbitmq
    container_name: 'rabbitmq'
    ports:
      - 5672:5672
    networks:
      - reactdrf

networks:
  reactdrf:
    driver: bridge
```
