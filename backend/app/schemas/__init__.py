"""
Pydantic Data Transfer Objects (DTOs / Request & Response Schemas).

Responsibilities:
- Strict validation of incoming HTTP payload boundaries.
- Serialization and formatting of outgoing HTTP responses.
- Automatic generation of OpenAPI (Swagger) data models.

Rules:
- Schemas define the public API contract. They are decoupled from the DB models.
"""
