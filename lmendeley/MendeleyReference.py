from .GenericReference import GenericReference
from typing import List


class MendeleyReference(GenericReference):
    """Simple class to hold a Mendeley document's reference data.

    """

    """Keys in a document that the MendeleyReference cares about.

    These correspond **only** to fields that can be found under the `documents`
    table of the Mendeley sqlite3 db. Therefore, do not add e.g., the tags of a
    document as a key here.
    """
    param_keys = [
        "abstract",
        "citationKey",
        "doi",
        "favourite",
        "isbn",
        "institution",
        "language",
        "pages",
        "publication",
        "volume",
        "year",
        "type",
        "note",
        "series",
        "seriesNumber",
        "publisher",
        *GenericReference.param_keys,
    ]  # type: List[str]

    def __init__(self, *args, **kargs):
        GenericReference.__init__(self, *args, **kargs)

        self.tags = []  # List[int, List]

    def as_text_reference(self) -> str:
        msg = super(MendeleyReference, self).as_text_reference()
        msg += "Authors: {}".format(self.authors)

        return msg
