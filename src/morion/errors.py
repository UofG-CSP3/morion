from typing import Callable, NamedTuple


class MorionError(Exception):
    """Base class for Morion exceptions."""

    def __init__(self, message: str = ''):
        super(MorionError, self).__init__(message)
        self.message = message


class FunctionErrorPair(NamedTuple):
    func: Callable
    error: Exception


class ReadError(MorionError):
    """Error thrown on failed attempted read of a file."""
    pass


class ReadListError(ReadError):
    """Error for when readers try and fail to read a file"""

    def __init__(self, reader_errors: list[FunctionErrorPair]):
        super(ReadError, self).__init__(ReadListError.format_error(reader_errors))

    @staticmethod
    def format_error(reader_errors: list[FunctionErrorPair]):
        ret = [f'{len(reader_errors)} reader(s) attempted to read this file, and none were able to.']
        ret.extend([f'{reader}: {error}' for reader, error in reader_errors])
        return '\n'.join(ret)


class WriteError(MorionError):
    """Use this to throw errors raised by writers."""
    pass


class WriteListError(WriteError):
    """Error for when writers try and fail to write a file"""

    def __init__(self, writer_errors: list[FunctionErrorPair], ):
        super(WriteError, self).__init__(WriteListError.format_error(writer_errors))

    @staticmethod
    def format_error(writer_errors: list[FunctionErrorPair]):
        ret = [f'{len(writer_errors)} writer(s) attempted to read this file, and none were able to.']
        ret.extend([f'{writer}: {error}' for writer, error in writer_errors])
        return '\n'.join(ret)
