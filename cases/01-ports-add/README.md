# Case: 01-ports-add

## Description

This case demonstrates how Docker Compose **merges ports lists** when an
override file is used.

Important points:
- Ports are **appended**, not replaced
- This can expose ports unintentionally in production

---

## Input configurations

### docker-compose.yaml

```yaml
services:
  web:
    image: nginx
    ports:
    - "8080:8080" # Expose a first port
```

### docker-compose.override.yaml

```yaml
services:
  web:
    ports:
      - "5000:5000"  # Expose a second port
```

---

## Expected merged configuration

### expected.yaml

```yaml
name: 01-ports-add
services:
  web:
    image: nginx
    networks:
      default: null
    ports:
      - mode: ingress
        target: 8080
        published: "8080"
        protocol: tcp
      - mode: ingress
        target: 5000
        published: "5000"
        protocol: tcp
networks:
  default:
    name: 01-ports-add_default
```

---

## Command used

```bash
docker compose \
  -f docker-compose.yaml \
  -f docker-compose.override.yaml \
  config
```
