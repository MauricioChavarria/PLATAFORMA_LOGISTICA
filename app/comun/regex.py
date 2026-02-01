import re

# Placa Colombia (simplificada): ABC123 o ABC12D
PLACA_RE = re.compile(r"^[A-Z]{3}\d{2}[A-Z0-9]$")

# Código de flota (ejemplo): FLT-0001
FLOTA_RE = re.compile(r"^FLT-\d{4}$")

# Guía (ejemplo): GUIA-2026-000001
GUIA_RE = re.compile(r"^GUIA-\d{4}-\d{6}$")
