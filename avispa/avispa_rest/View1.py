from CouchView import CouchView

class View1(CouchView):
    """ Count the number of documents available, per type. """

    @staticmethod
    def map(doc):
        """ Emit the document type for each document. """
        if 'doc_type' in doc:
            yield (doc['doc_type'], 1)

    @staticmethod
    def reduce(keys, values, rereduce):
        """ Sum the values for each type. """
        return sum(values)