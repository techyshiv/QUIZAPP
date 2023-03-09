from jsonschema import Draft202012Validator
userSchema = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string", "minLength": 3, "maxLength": 21},
        "lastname": {"type": "string", "minLength": 3, "maxLength": 21},
        "email": {"type": "string", "pattern": "^\\S+@\\S+\\.\\S+$", "format": "email"},
        "password": {"type": "string", "minLength": 8, "maxLength": 21},
        "role": {"type": "string"}
    },
    "required": ["firstname", "lastname", "email", "password"],
    "additionalProperties": False
}


loginSchema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": "^\\S+@\\S+\\.\\S+$", "format": "email"},
        "password": {"type": "string", "minLength": 8, "maxLength": 21}
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

register_validator = Draft202012Validator(userSchema)
login_validator = Draft202012Validator(loginSchema)


def Validate(payload):
    print("payload :", payload)
    response = list(register_validator.iter_errors(payload))
    print("response :", response)
    if (len(response) == 0):
        return {
            "statusCode": 200,
            "message": "Request Payload is Valid"
        }
    else:
        return {
            "statusCode": 403,
            "message": "Request Payload is Not Valid",
            "body": response[0].message
        }


def loginValidate(payload):
    response = list(login_validator.iter_errors(payload))
    print("response :", response)
    if (len(response) == 0):
        return {
            "statusCode": 200,
            "message": "Request Payload is Valid"
        }
    else:
        return {
            "statusCode": 422,
            "message": "Request Payload is Not Valid",
            "body": response[0].message
        }


# from jsonschema import Draft202012Validator
# draft_202012_validator = Draft202012Validator(userSchema)
# try:
#     instance1 = {'firstname': '', 'lastname': '',
#                  'email': '1616510104@kit.ac.in', 'password': 'shivang607', 'role': 'user'}
#     print(list(draft_202012_validator.iter_errors(instance1)))
#     print(draft_202012_validator.is_valid(instance1))
# except Exception as e:
#     print("Error :", e)
