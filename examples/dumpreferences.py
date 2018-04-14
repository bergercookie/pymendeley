"""
Example usage of pymendeldey; dumps all references
in the Mendeley local database.

"""

from __future__ import print_function

import lmendeley
import operator

def main():
    db = lmendeley.MendeleyDatabaseInterface()
    references = db.get_all_references()

    references.sort(key=operator.attrgetter('authors'))

    for ref in references:
        print(ref.as_text_reference())

if __name__ == '__main__':
    main()
