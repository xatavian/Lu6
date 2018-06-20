from copy import deepcopy


class ContextSanitizer(object):

    @staticmethod
    def sanitize_context(context):
        result, temp = context.copy(), context.parentcontext

        while temp is not None and temp.in_statement_context:
            for entry in temp.localentries:
                result.add(deepcopy(entry))
            temp = temp.parentcontext

        # The sanitized parent context is the last one that was analysed and was not valid
        result.parentcontext = temp

        return result