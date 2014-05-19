class BulkException(Exception):

    default_detail = u'Bulk Exception'

    def __init__(self, detail=u''):
        """
        Bulk Exception class.
        """
        super(BulkException, self).__init__()
        if detail:
            self.detail = detail

    def get_detail(self):
        return self.detail or self.default_detail

    def __str__(self):
        return self.get_detail()
