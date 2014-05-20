sfbulk
=======

*Development Status :: 2 - Pre-Alpha*


sfbulk is a Python API for the `Salesforce.com`_ Bulk API.

.. _Salesforce.com: http://www.salesforce.com/


Salesforce.com Inc. is a global cloud computing company
best known for its customer relationship management (CRM) product.

Salesforce.com provides different types of `API`_.
The Bulk API provides programmatic access to allow you to quickly load your organization`s data into Salesforce.

sfbulk attempts to alleviate many of the problems programmers might experience
with Salesforce.com`s` Bulk API by providing a 
cleaner, simpler and much more coherent API.

.. _API: https://www.salesforce.com/us/developer/docs/api_asynch/

sfbulk supports most all of the Salesforce.com`s Bulk API functionality 
including:

- Query
- Insert
- Update
- Upsert
- Delete

a large number of records asynchronously by submitting batches
which are processed in the background by Salesforce.

Example
-------

Here is a simple example of a basic insert operation for Campaign object.

.. code-block:: python

    from sfbulk import Bulk

    # initialize bulk
    bulk = Bulk()
    bulk.login('username', 'password','security_token')

    # create job
    bulk.job_create(u'insert', u'Campaign')

    # create batch
    data = 'Name\none\ntwo\nthree'
    bulk.batch_create(data)

    # wait until job finishes
    while (not bulk.job_is_completed()):
        sleep(10)

    # close the job
    bulk.job_close()


Documentation
-------------

Please visit the `Github Page`_ for full documentation.

.. _Github Page: http://clearcode.github.io/sfbulk/


License
-------

sfbulk is distributed under the `LGPL License`_.

.. _LGPL License: http://www.gnu.org/licenses/lgpl.html


Support
-------

All bug reports, new feature requests and pull requests are handled through 
this project's `Github issues`_ page.

.. _Github issues: https://github.com/clearcode/sfbulk/issues
