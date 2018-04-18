from .GenericReference import GenericReference
from typing import List


class MendeleyReference(GenericReference):
    """Simple class to hold a Mendeley document's reference data.

    """

    """Keys in a document that the MendeleyReference cares about"""
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

        """List of authors of the paper.
        This list should store dictionaries of the form:
        {"first_name": ...,
        "last_name": ... }

        """
        self.authors = []

    def as_text_reference(self) -> str:
        msg = super(MendeleyReference, self).as_text_reference()
        msg += "Authors: {}".format(self.authors)

        return msg
