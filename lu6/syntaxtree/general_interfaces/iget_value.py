class IGetValue(object):
    def set_value(self, value):
        raise NotImplementedError()

    def get_value(self):
        raise NotImplementedError()
