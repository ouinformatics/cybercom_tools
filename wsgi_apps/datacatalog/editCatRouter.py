class editCatRouter(object):
    """A router to control all database operations on models in
    the editCat application"""

    def db_for_read(self, model, **hints):
        "Point all operations on editCat models to 'catalog'"
        if model._meta.app_label == 'editCat':
            return 'catalog'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on editCat models to 'catalog'"
        if model._meta.app_label == 'editCat':
            return 'catalog'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in editCat is involved"
        if obj1._meta.app_label == 'editCat' or obj2._meta.app_label == 'editCat':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the editCat app only appears on the 'catalog' db"
        if db == 'catalog':
            return model._meta.app_label == 'editCat'
        elif model._meta.app_label == 'editCat':
            return False
        return None
