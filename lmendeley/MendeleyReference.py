class MendeleyReference(object):
    """Simple class to hold a Mendeley document's reference data.

    """

    """Keys in a document that the MendeleyReference cares about"""
    param_keys = [
        "id",
        "uuid",
        "type",
        "isbn",
        "doi",
        "volume",
        "pages",
        "citationKey",
        "year",
        "title",
        "publication",
        "institution",
        "favourite",
        "note",
        "abstract",
    ]

    def __init__(self, *args, **kargs):
        """init method.

        Whatever keyword argument is passed is to be forwarded to the params
        dict.

        """
        super(MendeleyReference, self).__init__()

        """Parameters of a Mendeley Reference."""
        self.params = {
            key: None for key in MendeleyReference.param_keys
        }
        self.params.update(kargs)

        """List of authors of the paper.
        This list should store dictionaries of the form:
        {"first_name": ...,
        "last_name": ... }

        """
        self.authors = []

    def as_text_reference(self):
        """Get the string representation of the current MendeleyReference."""

        header = self.__repr__()
        msg = "-" * min(80, len(header)) + "\n\n"
        for key, val in self.params.items():
            msg += "{}: {}\n---\n".format(key, val)
        msg += "{}".format(self.authors)
        return msg

    def __repr__(self):
        msg = "{}: {} - {}".format(self.params["id"], self.params["uuid"],
                                   self.params["title"])
        return msg
