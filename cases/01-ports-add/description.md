This case demonstrates how Docker Compose **merges ports lists** when an
override file is used.

Important points:
- Ports are **appended**, not replaced
- This can expose ports unintentionally in production
