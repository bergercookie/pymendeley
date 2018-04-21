from typing import List, Any
import os
import re


class GenericReference(object):
    """Generic type to  be used as the base class for holding a reference of a
    book/scientific papers management software.

    See :class:`lmendeley.MendeleyReference` as an inheritance example

    """

    """Keys in a document that the GenericReference instance cares about"""
    param_keys = [
        "id",
        "uuid",
        "title"
    ]  # type: List[str]


    def __init__(self, *args, **kargs):
        """init method.

        Whatever keyword argument is passed is to be forwarded to the params
        dict.

        """

        """Parameters of a Generic Reference."""
        self.params = {
            key: None for key in GenericReference.param_keys
        }  # Dict[str, Any]
        self.params.update(kargs)
        self.doc_url = ''  # type: str

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


    def should_fetch_from_web(self) -> bool:
        """Does the current reference correspond to a resource from the web?
        """
        return not re.search('^file:///.$', self.doc_url)

    def get_doc_extension(self) -> str:
        """Return the extension of the file.

        If there is no extension return None
        """

        # Get the path since the last slash, split at last dot
        extension = self.doc_url.split(os.sep)[-1].split('.')[-1]
        return extension



    def as_text_reference(self) -> str:
        """Get the string representation of the current MendeleyReference."""

        header = self.__repr__()
        msg = "{}\n{}\n\n".format(header, "-" * min(80, len(header)))
        for key, val in self.params.items():
            msg += "{}: {}\n".format(key, val)
        msg += "\n\n"
        return msg

    def __repr__(self) -> str:
        msg = "{}: {} - {}".format(self.params["id"], self.params["uuid"],
                                   self.params["title"])
        return msg

