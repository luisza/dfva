def calc_bccr_call(obj):
    """
    Calcula la duración de solicitar al BCCR

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    if obj.start_bccr_call is None or obj.end_bccr_call is None:
        return 0
    return (obj.end_bccr_call - obj.start_bccr_call).total_seconds()


def calc_save_database(obj):
    """
    Calcula la duración de guardar en la base de datos

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    if obj.start_save_database is None or obj.end_save_database is None:
        return 0
    return (obj.end_save_database - obj.start_save_database).total_seconds()


def calc_check_institution_certificate(obj):
    """
    Calcula la duración de verificar que la institución solicitante está autorizada

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    if obj.start_check_institution_certificate is None or obj.end_check_institution_certificate is None:
        return 0
    return (obj.end_check_institution_certificate - obj.start_check_institution_certificate).total_seconds()


def calc_decrypt_time(obj):
    """
    Calcula la duración de desencriptar la petición

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    if obj.start_decrypt is None or obj.end_decrypt is None:
        return 0
    return (obj.end_decrypt - obj.start_decrypt).total_seconds()


def calc_encrypt_time(obj):
    """
    Calcula la duración de encriptar la respuesta

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    if obj.start_encryption is None or obj.end_encryption is None:
        return 0
    return (obj.end_encryption - obj.start_encryption).total_seconds()


def calc_total_spend_time(obj):
    """
    Calcula la duración de la solicitud dentro de la aplicación (no contempla transmición entre el usuario y el servidor)

    :return: int - Si es 0 si no se calculó, o la duración en segundos
    """
    return calc_bccr_call(obj) + calc_save_database(obj) \
           + calc_check_institution_certificate(obj) + calc_decrypt_time(obj) \
           + calc_encrypt_time(obj)
