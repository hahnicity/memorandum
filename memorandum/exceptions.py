"""
memorandum.exceptions
~~~~~~~~~~~~~~~~~~~~~
"""


class HTTPStatusCodeError(Exception):
    def __init__(self, response):
        super(HTTPStatusCodeError, self).__init__(
            "You received a non-200 status code.\nStatus Code:{}\nText: {}".
            format(response.status_code, response.text)
        )
