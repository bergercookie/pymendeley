import sqlite3
from .MendeleyReference import MendeleyReference
import atexit
from typing import Dict, Any, Tuple
from . import find_mendeley_sqlite_path


class MendeleyDbInterface(object):
    """Class that interfaces with the Mendeley sqlite3 database."""

    def __init__(self, path=None):
        self.path = path or find_mendeley_sqlite_path()  # type: str

        """Document ID => MendeleyReference."""
        self.doc_id_to_reference = {}  # type: Dict[int, MendeleyReference]

        """Specifies whether we are interested only in the mendeley references
        that correspond to a local entry.
        """
        self.use_local_urls_only = True

        print("Connecting to the Mendeley db...")
        self.db = sqlite3.connect(self.path)

        atexit.register(self.cleanup)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()


    def cleanup(self) -> None:
        """Class cleanup method."""

        print("Cleaning up class instance {}.".format(type(self).__name__))
        self.db.close()

    def load_all_references(self) -> None:
        """Retrieves all references from the Mendeley database and caches them
        in dictionaries of the class.

        .. note:: Method takes care of filling the `doc_id_to_reference`
                  dictionary as well
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
        id2url = list(self.db.execute(
            "SELECT Documents.id, Files.localUrl "
            "FROM Files, DocumentFiles, Documents "
            "WHERE Files.hash = DocumentFiles.hash AND DocumentFiles.documentId = Documents.id"))
        doc_id_to_url = {doc_url[0]: doc_url[-1]
                         for doc_url in id2url
                         if id2url[-1]}  # Dict[str, str]

        id_authors = self.db.execute("SELECT Documents.id, group_concat(DocumentContributors.firstNames, ','), group_concat(DocumentContributors.lastName, ',') as authors_last "
                                     "FROM DocumentContributors, Documents, DocumentFolders "
                                     "WHERE Documents.id=DocumentContributors.documentId AND DocumentFolders.documentId=Documents.id group by Documents.title "
                                     "ORDER BY authors_last")
        # zip first names and last names
        # final form
        # {id: [(first_name1, last_name1), (first_name2, last_name2), ...}
        doc_id_to_authors_list = {
            i[0]: list(zip(i[1].split(','), i[2].split(',')))
            for i in id_authors
        }  # Dict[str, Tuple]

        # grab the tags of the documents
        id2tags = self.db.execute("SELECT Documents.id, Documenttags.tag "
                                  "FROM Documents, Documenttags "
                                  "WHERE Documents.id = Documenttags.documentId")
        doc_id_to_tags = {i[0]: i[-1] for i in id2tags}
        # tags should always be a list
        for key, val in doc_id_to_tags.items():
            if not isinstance(val, list):
                doc_id_to_tags[key] = [val]

        for cont in conts:
            curr_id = cont[id_indx]

            # Run only if we have the file locally?
            if self.use_local_urls_only and curr_id not in doc_id_to_url \
                    or not doc_id_to_url[curr_id]:
                continue

            # Create the MendeleyReference
            init_dict = {names[i]: cont[i] for i in indices_of_interest}
            ref = MendeleyReference(**init_dict)

            # fill the url
            ref.doc_url = doc_id_to_url[curr_id]

            # fill the authors
            if curr_id in doc_id_to_authors_list.keys():
                ref.authors = doc_id_to_authors_list[curr_id]

            self.doc_id_to_reference[curr_id] = ref

            # fill the tags
            if curr_id in doc_id_to_tags.keys():
                ref.tags = doc_id_to_tags[curr_id]


