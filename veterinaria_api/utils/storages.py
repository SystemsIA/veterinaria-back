from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    # Tipo de almacenamiento
    default_acl = "private"
    # Campo necesario
    custom_domain = False
    # peticiones por authenticación
    querystring_auth = True
    # Tiempo de vida del archivo (segundos)
    querystring_expire = 60 * 60
