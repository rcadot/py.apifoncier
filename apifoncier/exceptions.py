class ApiDFError(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        message = f"""Erreur {status_code} : {detail}"""
        super().__init__(message)


class TokenNotConfigured(Exception):
    def __init__(self):
        message = f"""Le token n'a pas été configuré. Utiliser apifoncier.configure(TOKEN="jeton")"""
        super().__init__(message)
