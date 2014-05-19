Examples
========

Query
-----

    .. code-block:: python

        from sfbulk import Bulk

        from pprint import pformat
        from time import sleep


        # initialize bulk
        bulk = Bulk()
        bulk.login('username',
                   'pasword',
                   'security_token')

        # create job
        bulk.job_create(u'query', u'Contact')

        # create batch
        data = 'SELECT Id FROM Contact'
        bulk.batch_create(data)

        # wait until job finishes
        while (not bulk.job_is_completed()):
            sleep(10)

        # show batch status
        status = bulk.batch_status()
        print "Batch status:\n%s" % pformat(status)

        # show batch result
        result = bulk.batch_result()
        print "Batch result:\n%s" % pformat(result)

        # close job
        bulk.job_close()

Insert
------

    .. code-block:: python

        from sfbulk import Bulk

        from pprint import pformat
        from time import sleep

        #NOTE: logger is optional
        import logging
        import sys
        

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        logger = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)

        # initialize bulk
        bulk = Bulk(logger)
        bulk.login('username',
                   'pasword',
                   'security_token')

        # create job
        bulk.job_create(u'insert', u'Case')

        # create batch
        data = 'Status,Subject\none,foo\ntwo,bar\nthree,foo'
        bulk.batch_create(data)

        # wait until job finishes
        while (not bulk.job_is_completed()):
            sleep(10)

        # show batch status
        status = bulk.batch_status()
        print "Batch status:\n%s" % pformat(status)

        # show batch result
        result = bulk.batch_result()
        print "Batch result:\n%s" % pformat(result)

        # close job
        bulk.job_close()

Update
------

    .. code-block:: python

        from sfbulk import Bulk

        from pprint import pformat
        from time import sleep

        #NOTE: logger is optional
        import logging
        import sys


        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        logger = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)

        # initialize bulk
        bulk = Bulk(logger)
        bulk.login('username',
                   'pasword',
                   'security_token')

        # create job
        bulk.job_create(u'update', u'Solution')

        # create batch
        #NOTE: Ids could be returned eg. by uery operation
        data = 'Id,SolutionName\n501i00000008yqOAAQ,one\n501i0000000iSEyAAM,two\n501i0000000iSEzAAM,three'
        bulk.batch_create(data)

        # wait until job finishes
        while (not bulk.job_is_completed()):
            sleep(10)

        # show batch status
        status = bulk.batch_status()
        print "Batch status:\n%s" % pformat(status)

        # show batch result
        result = bulk.batch_result()
        print "Batch result:\n%s" % pformat(result)

        # close job
        bulk.job_close()

Upsert
------

    .. code-block:: python

        from sfbulk import Bulk

        from pprint import pformat
        from time import sleep

        #NOTE: logger is optional
        import logging
        import sys


        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        logger = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)

        # initialize bulk
        bulk = Bulk(logger)
        bulk.login('username',
                   'pasword',
                   'security_token')

        # create job
        #NOTE: ExternalId must be set by web interface
        externalidfield = 'ownId__c'
        bulk.job_create(u'upsert', u'Campaign', externalidfield)

        # create batch
        data = 'Name,ownId__c\none,1\ntwo,2\nthree,3\nfour,4'
        bulk.batch_create(data)

        # wait until job finishes
        while (not bulk.job_is_completed()):
            sleep(10)

        # show batch status
        status = bulk.batch_status()
        print "Batch status:\n%s" % pformat(status)

        # show batch result
        result = bulk.batch_result()
        print "Batch result:\n%s" % pformat(result)

        # close job
        bulk.job_close()

Delete
------

    .. code-block:: python

        from sfbulk import Bulk

        from pprint import pformat
        from time import sleep


        #initialize bulk
        bulk = Bulk()
        bulk.login('username',
                   'pasword',
                   'security_token')

        # create job
        bulk.job_create(u'delete', u'Contact')

        # create batch
        #NOTE: Ids could be returned eg. by query operation
        data = 'Id\n003i000000iRBFWAA4\n003i000000iRBFdAAO\n'
        bulk.batch_create(data)

        # wait until job finishes
        while (not bulk.job_is_completed()):
            sleep(10)

        # show batch status
        status = bulk.batch_status()
        print "Batch status:\n%s" % pformat(status)

        # show batch result
        result = bulk.batch_result()
        print "Batch result:\n%s" % pformat(result)

        # close job
        bulk.job_close()
