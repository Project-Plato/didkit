from ctypes import *
from sys import platform
import os.path

didkit = None
didpath = os.path.dirname(os.path.abspath(__file__))

if platform == "linux" or platform == "linux2":
    didpath = os.path.join(didpath, 'libdidkit.so')
    didkit = libc = CDLL(didpath)
elif platform == "darwin":
    didpath = os.path.join(didpath, 'libdidkit.dylib')
    didkit = libc = CDLL(didpath)
else:
    didpath = os.path.join(didpath, 'libdidkit.dll')
    didkit = libc = CDLL(didpath, winmode=1)

# String get_version()
didkit.didkit_get_version.restype = c_char_p
didkit.didkit_get_version.argtype = ()

# String didkit_error_message()
didkit.didkit_error_message.restype = c_char_p
didkit.didkit_error_message.argtype = ()

# int didkit_error_code()
didkit.didkit_error_code.restype = c_int32
didkit.didkit_error_code.argtype = ()

# String generate_ed25519_key()
didkit.didkit_vc_generate_ed25519_key.restype = c_void_p
didkit.didkit_vc_generate_ed25519_key.argtype = ()

# String key_to_did(String method_pattern, String key)
didkit.didkit_key_to_did.restype = c_void_p
didkit.didkit_key_to_did.argtype = (c_char_p, c_char_p)

# String key_to_verification_method(String method_pattern, String key)
didkit.didkit_key_to_verification_method.restype = c_void_p
didkit.didkit_key_to_verification_method.argtype = (c_char_p, c_char_p)

# String issue_credential(String credential, String options, String key)
didkit.didkit_vc_issue_credential.restype = c_void_p
didkit.didkit_vc_issue_credential.argtype = (c_char_p, c_char_p, c_char_p)

# String verify_credential(String credential, String options)
didkit.didkit_vc_verify_credential.restype = c_void_p
didkit.didkit_vc_verify_credential.argtype = (c_char_p, c_char_p)

# String issue_presentation(String presentation, String options, String key)
didkit.didkit_vc_issue_presentation.restype = c_void_p
didkit.didkit_vc_issue_presentation.argtype = (c_char_p, c_char_p, c_char_p)

# String verify_presentation(String presentation, String options)
didkit.didkit_vc_verify_presentation.restype = c_void_p
didkit.didkit_vc_verify_presentation.argtype = (c_char_p, c_char_p)

# String resolve_did(String did, String input_metadata)
didkit.didkit_did_resolve.restype = c_void_p
didkit.didkit_did_resolve.argtype = (c_char_p, c_char_p)

# String dereference_did_url(String did_url, String input_metadata)
didkit.didkit_did_url_dereference.restype = c_void_p
didkit.didkit_did_url_dereference.argtype = (c_char_p, c_char_p)

# String did_auth(String did, String options, String key)
didkit.didkit_did_auth.restype = c_void_p
didkit.didkit_did_auth.argtype = (c_char_p, c_char_p, c_char_p)

# void didkit_free_string(String str)
didkit.didkit_free_string.restype = None
didkit.didkit_free_string.argtype = (c_void_p)


class DIDKitException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    @staticmethod
    def last_error():
        code = didkit.didkit_error_code()
        message = didkit.didkit_error_message()
        message_str = 'Unable to get error message' if not message else message.decode()
        return DIDKitException(code, message_str)


def get_version():
    return didkit.didkit_get_version().decode()


def generate_ed25519_key():
    key = didkit.didkit_vc_generate_ed25519_key()
    if not key:
        raise DIDKitException.last_error()
    key_str = cast(key, c_char_p).value.decode()
    didkit.didkit_free_string(cast(key, c_void_p))
    return key_str


def key_to_did(method_pattern, key):
    did = didkit.didkit_key_to_did(method_pattern.encode(), key.encode())
    if not did:
        raise DIDKitException.last_error()
    did_str = cast(did, c_char_p).value.decode()
    didkit.didkit_free_string(cast(did, c_void_p))
    return did_str


def key_to_verification_method(method_pattern, key):
    vm = didkit.didkit_key_to_verification_method(method_pattern.encode(),
                                                  key.encode())
    if not vm:
        raise DIDKitException.last_error()
    vm_str = cast(vm, c_char_p).value.decode()
    didkit.didkit_free_string(cast(vm, c_void_p))
    return vm_str


def issue_credential(credential, options, key):
    vc = didkit.didkit_vc_issue_credential(credential.encode(),
                                           options.encode(), key.encode())
    if not vc:
        raise DIDKitException.last_error()
    vc_str = cast(vc, c_char_p).value.decode()
    didkit.didkit_free_string(cast(vc, c_void_p))
    return vc_str


def verify_credential(credential, options):
    result = didkit.didkit_vc_verify_credential(credential.encode(),
                                                options.encode())
    if not result:
        raise DIDKitException.last_error()
    result_str = cast(result, c_char_p).value.decode()
    didkit.didkit_free_string(cast(result, c_void_p))
    return result_str


def issue_presentation(presentation, options, key):
    vp = didkit.didkit_vc_issue_presentation(presentation.encode(),
                                             options.encode(), key.encode())
    if not vp:
        raise DIDKitException.last_error()
    vp_str = cast(vp, c_char_p).value.decode()
    didkit.didkit_free_string(cast(vp, c_void_p))
    return vp_str


def verify_presentation(presentation, options):
    result = didkit.didkit_vc_verify_presentation(presentation.encode(),
                                                  options.encode())
    if not result:
        raise DIDKitException.last_error()
    result_str = cast(result, c_char_p).value.decode()
    didkit.didkit_free_string(cast(result, c_void_p))
    return result_str


def resolve_did(did, input_metadata):
    result = didkit.didkit_did_resolve(did.encode(), input_metadata.encode())
    if not result:
        raise DIDKitException.last_error()
    result_str = cast(result, c_char_p).value.decode()
    didkit.didkit_free_string(cast(result, c_void_p))
    return result_str


def dereference_did_url(did_url, input_metadata):
    result = didkit.didkit_did_url_dereference(did_url.encode(),
                                               input_metadata.encode())
    if not result:
        raise DIDKitException.last_error()
    result_str = cast(result, c_char_p).value.decode()
    didkit.didkit_free_string(cast(result, c_void_p))
    return result_str


def did_auth(did, options, key):
    vp = didkit.didkit_did_auth(did.encode(), options.encode(), key.encode())
    if not vp:
        raise DIDKitException.last_error()
    vp_str = cast(vp, c_char_p).value.decode()
    didkit.didkit_free_string(cast(vp, c_void_p))
    return vp_str
