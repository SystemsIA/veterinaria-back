from django.core.validators import RegexValidator

celular_regex_validator = RegexValidator(
    regex=r"\+?1?\d{9,12}$", message="El celular puede comenzar con '+' o tener mín 9 y máx 12 dígitos."
)
dni_regex_validator = RegexValidator(regex=r"^\d{8,8}$", message="El DNI debe tener exactamente 8 dígitos.")
