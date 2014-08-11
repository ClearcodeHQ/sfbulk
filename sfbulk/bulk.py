import time

from sfbulk.callout import Callout
from sfbulk.exceptions import BulkException
from sfbulk.sf import sf
from sfbulk.jobinfo import JobInfo
from sfbulk.utils_csv import loadFromCSVFile
from sfbulk.utils_xml import parseXMLResult


class Bulk(sf):
    """
    Salesforce Bulk API Implementation.
    Main class to intiate bulk operation.
    """
    # CONSTANTS
    MAX_RECORDS = 10000
    USERAGENT = u'Python-BulkApiClient/26.0.0'
    API_VERSION = u'26.0'

    CONTENT_TYPE_XML = u'application/xml'
    CONTENT_TYPE_CSV = u'text/csv'
    CHARSET = u'charset=UTF-8'

    # WORDS
    REQUEST = u'request'
    RESULT = u'result'
    BATCH = u'batch'
    JOB = u'job'
    CLOSED = u'Closed'
    COMPLETED = u'Completed'
    FAILED = u'Failed'

    # RE-LOGIN SETTINGS
    LOG_BACK_IN = True
    LOG_BACK_IN_WAIT_TIME = 60*2

    def __init__(self, bulk_server=u'',
                 sessionid=None, logger=None):
        """
        Standard constructor.

        @type: string
        @param bulk_server: url to connect for the bulk operation
        @type: string
        @param sessionid: sessionid which can be use for initial.
                           This property will ALWAYS be overriden
                           when you use the login method.
        @type: logger instance
        @param logger: loger instance
        """
        self.bulk_server = bulk_server
        self.sessionid = sessionid
        self.callClient = None
        self.logger = self.LOGGER

    def job_create(self, operation, sf_object, externalidfield=None):
        self.jobinfo = JobInfo.factory(operation, sf_object, externalidfield)
        self.createJob(self.jobinfo)

    def job_close(self):
        self.closeJob(self.jobinfo)
        self.jobinfo = None

    def batch_create_from_csv(self, csv_filename, max_csvrecord):
        self.createBatchFromCSV(self.jobinfo,
                                csv_filename,
                                max_csvrecord)
        self.logger.info("Job: %s batch total number: %s" %
                        (self.runningJobId, len(self.jobinfo.batch)))

    def batch_create(self, batchdata):
        self.createBatch(self.jobinfo,
                         batchdata)
        self.logger.info("Job: %s batch total number: %s" %
                        (self.runningJobId, len(self.jobinfo.batch)))

    def job_is_completed(self):
        return self.is_jobs_completed(self.jobinfo)

    def batch_status(self):
        """
        @rtype: None
        """
        for batch_id in self.jobinfo.batch:
            self.updateBatchStatus(self.jobinfo, batch_id)
        return self.jobinfo.batch

    def createJob(self, jobinfo):
        """
        Creating new job.

        @type: JobInfo
        @param jobinfo: will be used to populate the job information
        """
        resp = self._bulkHttp(self.JOB,
                              jobinfo.createJob(),
                              self.__content_xml)
        dict_result = parseXMLResult(resp)
        if self.__check_result(dict_result):
            self.__update_running_job(dict_result)
            self.__update_jobinfo(jobinfo, dict_result)
            self.logger.info("Job: %s created" % jobinfo.id)
        else:
            if self._handle_errors(dict_result):
                self.createJob(jobinfo)
            else:
                self.__raise('Job creating failed')

    def closeJob(self, jobinfo):
        """
        Closing job.

        @type: JobInfo
        @param jobinfo: indicate job information which needs to be closed
        """
        jobinfo.state = self.CLOSED
        resp = self._bulkHttp(self.__join((self.JOB, jobinfo.id)),
                              jobinfo.closeJob(),
                              self.__content_xml)
        dict_result = parseXMLResult(resp)
        if self.__check_result(dict_result):
            self.__update_running_job(dict_result)
            self.__update_jobinfo(jobinfo, dict_result)
            self.logger.info("Job: %s state: %s" % (jobinfo.id, jobinfo.state))
        else:
            if self._handle_errors(dict_result):
                self.closeJob(jobinfo)
            else:
                self.__raise("Job: %s closing failed" % jobinfo.id)

    def createBatch(self, jobinfo, batchdata):
        """
        Create individual batch operation with batchdata.

        @type: JobInfo
        @param jobinfo: job information
        @type: string
        @param batchdata: information which will be sent
                          (e.g SOQL, CSV lines in string)
        """
        if self.runningJobId is None:
            self.__raise('Job in running not found')

        resp = self._bulkHttp(
            self.__join((self.JOB, self.runningJobId, self.BATCH)),
            batchdata, self.__content_csv)

        dict_result = parseXMLResult(resp)
        if self.__check_result(dict_result):
            self.__update_batch_state(jobinfo, dict_result)
            self.logger.info("Batch: %s status is: %s" %
                             (dict_result['id'], dict_result['state']))
            return dict_result['id']
        else:
            if self._handle_errors(dict_result):
                return self.closeJob(jobinfo)
            else:
                self.__raise('Batch creating failed')

    def createBatchFromCSV(self, jobinfo, cvsfile, maxrecord=None):
        """
        Create batch from csv file, also includes the max_record limitation.

        @type: JobInfo
        @param jobinfo: job information
        @type: string
        @param csvfile: CSV file name to load
                        and will be divided based on the max_record limitation
        """
        batches_id = []
        if maxrecord is None or maxrecord == '':
            maxrecord = self.MAX_RECORDS
        batches_file = loadFromCSVFile(cvsfile, int(maxrecord))
        for batch_file in batches_file:
            batchid = self.createBatch(jobinfo, batch_file)
            batches_id.append(batchid)
        return batches_id

    def updateBatchStatus(self, jobinfo, batchId):
        """
        Update individual batch status.

        @type: JobInfo
        @param jobinfo: job information
        @type: string
        @param batchId: batch id
        """
        resp = self._bulkHttp(
            self.__join((self.JOB, self.runningJobId, self.BATCH, batchId)),
            None, self.__content_csv, 'GET')
        dict_result = parseXMLResult(resp)
        if self.__check_result(dict_result):
            if dict_result['id'] in jobinfo.batch:
                self.__update_batch_state(jobinfo, dict_result)
        else:
            if self._handle_errors(dict_result):
                self.updateBatchStatus(jobinfo, batchId)
            else:
                self.__raise("Batch: %s updateing status failed" % batchId)

    def batch_result(self, only_invalid=False):
        self.jobinfo.batch_result = dict()
        for batch in self.jobinfo.batch:
            result = self.showBatchResult(self.jobinfo, batch, only_invalid)
            self.jobinfo.batch_result.update({batch: result})
        return self.jobinfo.batch_result

    def showBatchResult(self, jobinfo, batchId, only_invalid=False):
        """
        Show the specific batch result.

        @type JobInfo
        @param jobinfo: job information
        @type: string
        @param batchId: batch id
        """
        resp = self._bulkHttp(
            self.__join((self.JOB, self.runningJobId, self.BATCH,
                        batchId, self.RESULT)),
            None, self.__content_csv, 'GET')

        if jobinfo.operation == 'query':
            results = parseXMLResult(resp)
            resp = self._bulkHttp(
                self.__join((self.JOB, self.runningJobId, self.BATCH,
                            batchId, self.RESULT, results['result'])),
                None, self.__content_csv, 'GET')

        results = resp.split('\n')
        #TODO: improve parsing response
        if only_invalid:
            invalid_results = []
            counter = 0
            for result in results:
                counter += 1
                result = result.replace('"', '')
                split = result.split(',')
                if len(split) > 2 and split[1] == 'false':
                    invalid_results.append(
                        "%s - Row number: %s" % (split, counter))
            results = invalid_results
        return results

    def is_jobs_completed(self, jobinfo):
        """
        Will check whether all batches in specific jobinfo record
        is completed/failed.

        @type: JobInfo
        @param jobinfo: job information
        """
        completed = True
        for batchId in jobinfo.batch:
            self.updateBatchStatus(jobinfo, batchId)
            status = jobinfo.findBatchState(batchId)
            if status != self.COMPLETED and status != self.FAILED:
                self.logger.info("Batch: %s status is: updateing..." % batchId)
                completed = False

        if completed == True:
            for batch in jobinfo.batch:
                if status != self.FAILED:
                    self.logger.info("Batch: %s status is: %s" %
                                    (batch, status))
                else:
                    self.logger.info("Batch: %s status is: %s: %s" %
                                     (batch, status,
                                     jobinfo.batch[batch]['stateMessage']
                                     ))

        return completed

    def _bulkHttp(self, bulkmethod, submitdata=None, pheaders=None,
                  httpmethods='POST'):
        """
        Methods to run http callout to salesforce.

        @type: string
        @param bulkmethod: what kind of bulk request (e.g self.JOB, self.BATCH)
        @type: string
        @param submitdata: data to be submitted
        @type: dict
        @param pheaders: HTTP header information
        @type: string
        @param: httpmethods: GET / POST methods to be used in bulk request
        """
        headers = self.__standardHeaders
        if headers is not None:
            if type(pheaders) == dict:
                for keyh, valueh in pheaders.iteritems():
                    headers[keyh] = valueh

        if self.callClient is None:
            if self.sessionid is not None:
                self.callClient = Callout(logger=self.logger)
            else:
                self.__raise('Unauthorized Error')

        resp = self.callClient.docall(
            self.__constructBulkUrl(
                bulkmethod), httpmethods, submitdata, headers)
        return resp

    def _handle_errors(self, dict_result):
        if 'exceptionCode' in dict_result:
            if dict_result['exceptionCode'] == 'InvalidSessionId':
                if self.LOG_BACK_IN:
                    self.logger.info('Invalid session: sleeping and retrying')
                    time.sleep(self.LOG_BACK_IN_WAIT_TIME)
                    self.login(self.USERNAME,
                               self.PASSWORD,
                               self.SECURITY_TOKEN,
                               self.SF_VERSION,
                               self.SANDBOX)
                    return True
        return False

    @staticmethod
    def __check_result(dict_result):
        if 'id' in dict_result:
            return True

    def __update_running_job(self, dict_result):
        self.runningJobId = dict_result['id']

    def __update_jobinfo(self, jobinfo, dict_result):
        jobinfo.id = dict_result['id']
        jobinfo.debug_result = dict_result
        jobinfo.state = dict_result['state']

    def __update_batch_state(self, jobinfo, dict_result):
        jobinfo.batch[dict_result['id']] = dict_result

    def __join(self, values):
        return u'/'.join(values)

    def __raise(self, message):
        self.logger.info(message)
        raise BulkException(message)

    def __constructBulkUrl(self, bulkmethod):
        """
        Helper method to create valid bulk operation url.

        @type: string
        @param bulkmethod: what kind of bulk request (e.g self.JOB, self.BATCH)
        """
        return self.__join((self.bulk_server, 'services/async',
                            self.API_VERSION, bulkmethod))

    @property
    def __standardHeaders(self):
        """
        Prepare standard headers information.
        """
        headersValue = {u'X-SFDC-Session': self.sessionid,
                        u'Accept': self.CONTENT_TYPE_XML,
                        u'User-Agent': self.USERAGENT}
        return headersValue

    @property
    def __content_xml(self):
        return {u'Content-Type': '{content}, {charset}'.format(
            content=self.CONTENT_TYPE_XML,
            charset=self.CHARSET)}

    @property
    def __content_csv(self):
        return {u'Content-Type': '{content}, {charset}'.format(
            content=self.CONTENT_TYPE_CSV,
            charset=self.CHARSET)}
