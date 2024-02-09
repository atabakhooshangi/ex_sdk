

class exchangeAuthenticationException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'exchangeAuthenticationException(code=%s): %s' % (self.code, self.message)


class TraderBotAuthenticationException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'exchangeAuthenticationException(code=%s): %s' % (self.code, self.message)


class NotFoundException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'exchangeAuthenticationException(code=%s): %s' % (self.code, self.message)