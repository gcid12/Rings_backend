from CouchView import CouchView

class View1(CouchView):
    """ Count the number of documents available, per type. """

    @staticmethod
    def map(doc):
        """ Emit the document type for each document. """
        if 'Name2' in doc.items[0]:
            yield (doc.added , doc.items[0].Name2)

    @staticmethod
    def reduce(keys, values, rereduce):
        """ Sum the values for each type. """
        return sum(values)