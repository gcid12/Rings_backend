from CouchView import CouchView

class View2(CouchView):
    """ Count2 the number of documents available, per type. """

    @staticmethod
    def map(doc):
        """ Emit2 the document type for each document. """
        if 'Name2' in doc.items[0]:
            yield (doc.added , doc.items[0].Name2)

    @staticmethod
    def reduce(keys, values, rereduce):
        """ Sum2 the values for each type. """
        return sum(values)