class MuvError(Exception):
    def __init__(self, msg, position=0):
        self.position = position
        super(MuvError, self).__init__(msg)


class MuvExceptionAlreadyDeclared(Exception):
    pass


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
