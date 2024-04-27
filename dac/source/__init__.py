
# from . import views, models, tasks

# from . import views # noqa

from . import *

class Source(object):
    def init(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError
