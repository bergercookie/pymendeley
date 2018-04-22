"""Access document data in the Mendeley sqlite3 database.

.. note:: Currently looks in fixed paths on Linux. Changing
          EXPECTED_MENDELEY_SQLITE_DIR and EXPECTED_MENDELEY_CONFIG_PATH
          should allow it to work on non-linux or non-standard
          installs.

"""

import os
from configparser import ConfigParser

# On Linux we can usually find the Mendeley sqlite3 database
# at this location.
EXPECTED_MENDELEY_SQLITE_DIR = \
    os.path.expanduser('~/.local/share/data/Mendeley Ltd./Mendeley Desktop')
EXPECTED_MENDELEY_CONFIG_PATH = \
    os.path.expanduser('~/.config/Mendeley Ltd./Mendeley Desktop.conf')


def find_mendeley_sqlite_path():
    """Get the path to the mendeley db file.

    :returns: The path to the Mendeley sqlite3 database if in standard location,
              otherwise returns None.
    :rtype str:

    """
    try:
        if os.path.exists(EXPECTED_MENDELEY_CONFIG_PATH):
            config_parser = ConfigParser()
            config_parser.read(EXPECTED_MENDELEY_CONFIG_PATH)

            email = config_parser.get('MendeleyWeb', 'userEmail')

            candidate_path = os.path.join(EXPECTED_MENDELEY_SQLITE_DIR,
                                          '%s@www.mendeley.com.sqlite' %
                                          (email,))
            if os.path.exists(candidate_path):
                return candidate_path
    except Exception:
        pass

    return None
