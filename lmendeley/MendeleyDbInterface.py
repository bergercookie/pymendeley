import sqlite3
from .MendeleyReference import MendeleyReference
import atexit
from . import find_mendeley_sqlite_path


class MendeleyDbInterface(object):
    """Class that interfaces with the Mendeley sqlite3 database."""

    def __init__(self, path=None):
        self.path = path or find_mendeley_sqlite_path()

        """Document ID => MendeleyReference."""
        self.doc_id_to_reference = {}
        """Document ID => local path."""
        self.doc_id_to_url = {}

        """Specifies whether we are interested only in the mendeley references
        that correspond to a local entry.
        """
        self.use_local_urls_only = True

        print("Connecting to the Mendeley db...")
        self.db = sqlite3.connect(self.path)

        atexit.register(self.cleanup)


    def cleanup(self):
        """Class cleanup method."""

        print("Cleaning up class instance {}.".format(type(self).__name__))
        self.db.close()

    def load_all_references(self):
        """Retrieves all references from the Mendeley database

        .. note:: Method takes care of filling the `doc_id_to_reference`,
                  `doc_id_to_url` dictionaries as well
        """

        # the table that holds the files metadata is called "documents"
        # grab the column names and the actual contents of the latter
        cursor = self.db.execute("SELECT * FROM documents")
        names = [description[0] for description in cursor.description]
        conts = list(cursor)

        # get the indices we are interested in for creating a MendeleyReference
        id_indx = names.index('id')
        indices_of_interest = [names.index(i) for i in
                               MendeleyReference.param_keys]

        # grab and cache the paths to the documents
        self.doc_id_to_url = list(self.db.execute(
            "SELECT Documents.id, Files.localUrl "
            "FROM Files, DocumentFiles, Documents "
            "WHERE Files.hash = DocumentFiles.hash AND DocumentFiles.documentId = Documents.id"))
        self.doc_id_to_url = {doc_url[0]: doc_url[-1]
                              for doc_url in self.doc_id_to_url
                              if self.doc_id_to_url[-1]}

        for cont in conts:
            # Run only if we have the file locally?
            curr_id = cont[id_indx]

            if self.use_local_urls_only and curr_id not in self.doc_id_to_url \
                    or not self.doc_id_to_url[curr_id]:
                continue

            # Create the MendeleyReference
            init_dict = {names[i]: cont[i] for i in indices_of_interest}

            # fill the authors
            # TODO
            ref = MendeleyReference(**init_dict)
            self.doc_id_to_reference[curr_id] = ref


