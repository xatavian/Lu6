class TemplateEngineException(Exception):
    def __init__(self, exception_str, line, *args, **kwargs):
        super().__init__(
            "{exception} at line {line}".format(exception=exception_str, line=line),
            *args, **kwargs
        )