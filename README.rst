Python package for accessing Mendeley's local sqlite3 database
==============================================================

.. image:: https://travis-ci.org/bergercookie/pymendeley.svg?branch=master
    :target: https://travis-ci.org/bergercookie/pymendeley

.. image:: https://readthedocs.org/projects/pymendeley/badge/?version=latest
    :target: http://pymendeley.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/bergercookie/pymendeley/blob/master/resources/pylint_badge.svg
   :target: https://github.com/bergercookie/pymendeley/blob/master/resources/pylint_badge.svg

.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/


.. image:: https://docs.google.com/drawings/pub?id=1kHdWh4RxbXWWCv5Q9CHMtnIRAtUFGad5xcRDKuBXIsA&w=829&h=279

Description
-----

pymendeley retrieves reference information from Mendeley's local sqlite3
database.

Install `bergercookie/pymendeley <https://github.com/brotchie/pymendeley/tarball/master>`_ using::

    sudo pip install https://github.com/bergercookie/pymendeley/tarball/master

Dump a list of all references::

    import lmendeley

    db = lmendeley.MendeleyDatabaseInterface()
    references = db.load_all_references()

    for ref in references:
        print(ref.as_text_reference())

Projects using pymendeley:

* `mendeley2calibre <https://github.com/bergercookie/mendeley2calibre>`_


Offline documentation
-----

A developer can also generate the *Sphinx* documentation for *pymendeley* offline:

- Install the related tools::

    apt-get install sphinx sphinx_rtd_theme

- To update the documentation run ``make html`` inside the ``docs`` directory.
  Open the build/html/index.html file to view the results::

    $ firefox docs/build/html/index.html


