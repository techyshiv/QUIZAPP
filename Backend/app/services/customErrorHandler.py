class customErrorHandler(Exception):
    def __init__(self, status, message):
        super().__init__(status, message)
        self.status = status
        self.message = message

    @staticmethod
    def alreadyExist(message="Created Data already Exist !!"):
        response = customErrorHandler(409, message)
        status = response.status
        message = response.message
        return {"status": status, "message": message}

    @staticmethod
    def unAuthorized(message="UnAuthorized Access !!"):
        response = customErrorHandler(401, message)
        status = response.status
        message = response.message
        return {"status": status, "message": message}

    @staticmethod
    def notFound(message="Resource Not Found !!"):
        response = customErrorHandler(400, message)
        status = response.status
        message = response.message
        return {"status": status, "message": message}

    @staticmethod
    def ValidationError(message="Request Payload is Not Valid !!"):
        response = customErrorHandler(403, message)
        status = response.status
        message = response.message
        return {"status": status, "error": message}

    @staticmethod
    def serverError(message="Internal Server Error !!"):
        response = customErrorHandler(500, message)
        status = response.status
        message = response.message
        return {"status": status, "message": message}
