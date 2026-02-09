# Case: 02-ports-override

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
    - "8080:8080"  # Base app port (to be overridden in dev)
```

### docker-compose.override.yaml

```yaml
services:
  web:
    ports: !override
      - "80:8080"  # Expose only app port on host 80
```

---

## Expected merged configuration

### expected.yaml

```yaml
name: 02-ports-override
services:
  web:
    image: nginx
    networks:
      default: null
    ports:
      - mode: ingress
        target: 8080
        published: "80"
        protocol: tcp
networks:
  default:
    name: 02-ports-override_default
```

---

## Command used

```bash
docker compose \
  -f docker-compose.yaml \
  -f docker-compose.override.yaml \
  config
```
