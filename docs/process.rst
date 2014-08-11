.. _operation_process:

Operation process
=================

The Salesforce Bulk API lets you query, insert, update, upsert, or delete a large number of records asynchronously.

All operations use HTTP GET or POST methods to send and receive XML or CSV data.


How Salesforce Bulk API works?
------------------------------

You process a set of records by creating a **job that contains one or more batches**. The **job specifies which object is being processed and what type of action is being used** (query, insert, upsert, update, or delete). A job is represented by the **JobInfo** resource. This resource is used to create a new job, get status for an existing job, and change status for a job. A **batch is a set of records sent to the server**. You first send a number of batches to the server using an HTTP POST request and then the server processes the batches in the background. A batch is created by submitting a CSV or XML representation of a set of records and any references to binary attachment. Once created, the status of a batch is represented by a **BatchInfo** resource.  Each batch is processed independently by the server, not necessarily in the order it is received. While batches are being processed, you can track progress by checking the status of the job using an HTTP GET call. When a batch is complete, the result for each record is available in a result set resource.

.. _salesforce-bulk-api-monitor:

Salesforce Bulk API monitor
---------------------------
Salesforce web interface provides **monitor for Bulk API**. By using it you can monitor the status of recent bulk data load jobs created by **Data Loader** and other **Bulk API client applications**, including **sfbulk**. 

.. note:: **BULK API MONITOR**: You'll find this monitor under the section: **Setup**-> **Jobs** -> **Bulk Data Load Jobs**


sfbulk implementation
---------------------
This implementation is based on the primary **Bulk object that has methods to control job and batches**. In the present implementation one **Bulk** can simultaneously maintain a one **job** with many **batches**.

#. **Initialize bulk.**

    .. code-block:: python

        from sfbulk import Bulk

        bulk = Bulk()

    Method docs: :ref:`initialization<initialization>`  



#. Authorize bulk.

   Before performing any operations bulk must te authorized by login, password and security token.

    .. code-block:: python

        bulk.login('username', 'pasword', 'security_token')

    Method docs: :ref:`login<login>`  

#. Create job.

   Create a new job that specifies the **object** and **action**.

    .. code-block:: python

        bulk.job_create(u'query', u'Contact')

#. Create batch/batches.

   That's how data should be formatted is highly dependent on the type of action.

    .. code-block:: python

        data = 'SELECT Id FROM Contact'
        bulk.batch_create(data)

#. Wait untill job is completed.

   Check status of job at a reasonable interval.

    .. code-block:: python

        while (not bulk.job_is_completed()):
            sleep(10)

#. Check batch status (optional).

   When all batches have either completed or failed, retrieve the status for each batch.

    .. code-block:: python

        status = bulk.batch_status()

#. Check batch result (optional).

   Match the result sets with the original data set to determine which records failed and succeeded.

    .. code-block:: python

        result = bulk.batch_result()

#. Close job.

    Close the job. Once closed, no more batches can be sent as part of the job.

    .. code-block:: python

        bulk.job_close()
