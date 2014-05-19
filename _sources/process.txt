Operation process
=================

#. Initialize bulk.

    .. code-block:: python

        from sfbulk import Bulk

        bulk = Bulk()

#. Authorize bulk.

    .. code-block:: python

        bulk.login('username',
                   'pasword',
                   'security_token')

#. Create job.

    .. code-block:: python

        bulk.job_create(u'query', u'Contact')

#. Create batch.

    .. code-block:: python

        data = 'SELECT Id FROM Contact'
        bulk.batch_create(data)

#. Wait untill job finishes.

    .. code-block:: python

        while (not bulk.job_is_completed()):
            sleep(10)

#. Show batch status.

    .. code-block:: python

        status = bulk.batch_status()

#. Show batch result.

    .. code-block:: python

        result = bulk.batch_result()

#. Close job.

    .. code-block:: python

        bulk.job_close()
