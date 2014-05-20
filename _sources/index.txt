sfbulk
=======
*Development Status :: 2 - Pre-Alpha*

sfbulk is a Python API for the `Salesforce.com`_ Bulk API.
##########################################################


.. _Salesforce.com: http://www.salesforce.com/


**Salesforce.com Inc.** is a global cloud computing company
best known for its customer relationship management (CRM) product.

Salesforce.com provides different types of `API`_.
The **Bulk API** provides programmatic access to allow you to quickly load your organization's data into Salesforce.

.. _API: https://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_intro.htm

Why sfbulk?
-----------

**sfbulk** attempts to alleviate many of the problems programmers might experience
with Salesforce.com's' Bulk API by providing a 
cleaner, simpler and much more coherent API.

- You don't need to care of a creating XML for SOAP requests (which is usually tedious)
- You can use the high `limits`_ of processing records (compared to REST API)

.. _limits: https://www.salesforce.com/us/developer/docs/api_asynch/Content/asynch_api_concepts_limits.htm

**sfbulk** supports most all of the Salesforce.com's Bulk API functionality 
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
    bulk.login('username', 'password', 'security_token')

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

License
-------

sfbulk is distributed under the `LGPL License`_.

.. _LGPL License: http://www.gnu.org/licenses/lgpl.html

Contents
--------

.. toctree::
    :maxdepth: 1

    install
    process
    bulk
    exception
    examples
