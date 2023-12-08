from motogram import raw
from .auto_name import Auto_name

class CodeType(Auto_name):
    """Sent code type enumeration used in :obj:`~motogram.types.SentCode`."""

    APP = raw.types.auth.CodeTypeApp
    "The code was sent through the telegram app."

    CALL = raw.types.auth.CodeTypeCall
    "The code will be sent via a phone call. A synthesized voice will tell the user which verification code to input."

    FLASH_CALL = raw.types.auth.CodeTypeFlashCall
    "The code will be sent via a flash phone call, that will be closed immediately."

    MISSED_CALL = raw.types.auth.CodeTypeMissedCall
    "Missed call."

    SMS = raw.types.auth.CodeTypeSms
    "The code was sent via SMS."

    FRAGMENT_SMS = raw.types.auth.CodeTypeFragmentSms
    "The code was sent via Fragment SMS."

    EMAIL_CODE = raw.types.auth.CodeTypeEmailCode
    "The code was sent via email."
