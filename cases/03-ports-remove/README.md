# Case: 03-ports-remove

## Description

This case documents how Docker Compose merges configuration files when multiple compose files are used.

---

## Input configurations

### docker-compose.yaml

```yaml
services:
  web:
    image: nginx
    ports:
    - "8080:8080" # Expose somes ports
    - "5000:5000" # Expose somes ports
```

### docker-compose.override.yaml

```yaml
services:
  web:
    ports: !reset [] # Remove exposed ports
```

---

## Expected merged configuration

### expected.yaml

```yaml
name: 03-ports-remove
services:
  web:
    image: nginx
    networks:
      default: null
networks:
  default:
    name: 03-ports-remove_default
```

---

## Command used

```bash
docker compose \
  -f docker-compose.yaml \
  -f docker-compose.override.yaml \
  config
```
