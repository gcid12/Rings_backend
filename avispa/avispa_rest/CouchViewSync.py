import couchdb
from View1 import View1

class CouchViewSync:

    def set_db_views(self,db):

        '''
        This function will be executed once for every ring that is created. If run again it will reload them
        '''

        couch_views = [
            View1()
            # Put other view classes here
        ]

        """
        def sync_many(db, views, remove_missing=False, callback=None):

        Ensure that the views stored in the database that correspond to a
        given list of `ViewDefinition` instances match the code defined in
        those instances.
       
        This function might update more than one design document. This is done
        using the CouchDB bulk update feature to ensure atomicity of the
        operation.

        :param db: the `Database` instance
                :param views: a sequence of `ViewDefinition` instances
                :param remove_missing: whether views found in a design document that
                                       are not found in the list of `ViewDefinition`
                                       instances should be removed
                :param callback: a callback function that is invoked when a design
                                 document gets updated; the callback gets passed the
                                 design document as only parameter, before that doc
                                 has actually been saved back to the database
        """


        couchdb.design.ViewDefinition.sync_many(db, couch_views, remove_missing=True)