Development Status :: 2 - Pre-Alpha
-----------------------------------

sfbulk
======

sfbulk is a Python wrapper for the Salesforce.com Bulk API.

Docs: http://clearcode.github.io/sfbulk/


Salesforce.com Inc. is a global cloud computing company
best known for its customer relationship management (CRM) product.
Salesforce.com provides different types of `API`_.
The Bulk API provides programmatic access to allow you to quickly load your organization`s data into Salesforce.
sfbulk attempts to alleviate many of the problems programmers might experience
with Salesforce.com`s` Bulk API by providing a 
cleaner, simpler and much more coherent API.

sfbulk supports most all of the Salesforce.com`s Bulk API functionality 
including:

- Query
- Insert
- Update
- Upsert
- Delete

a large number of records asynchronously by submitting batches
which are processed in the background by Salesforce.

Here is a simple example of a basic insert Campaign operation.

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


sfbulk is released under the LGPL License: http://www.gnu.org/licenses/lgpl.html
