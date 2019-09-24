from werkzeug.exceptions import BadRequest


class Helper(object):
    @classmethod
    def get_sort_type_by_fields(cls, fields):
        sort_types = []
        for field in fields:
            sort_types.append('{}_asc'.format(field))
            sort_types.append('{}_desc'.format(field))
        return sort_types

    @classmethod
    def get_sort_from_args(cls, args, fields):
        # Sorting result
        if 'sort' in args and args['sort']:
            sort_by = args['sort']
            sorted_fields = Helper.get_sort_type_by_fields(fields)
            if sort_by not in sorted_fields:
                raise BadRequest(description='Sort is not valid')
            index = sort_by.rindex('_')
            sort = [sort_by[:index], sort_by[index + 1:]]
        else:
            sort = None
        return sort

    @classmethod
    def get_page_from_args(cls, args):
        if 'page' in args and args['page']:
            try:
                page = int(args['page'])
            except ValueError:
                raise BadRequest(description='Page is not valid')
        else:
            page = 1
        return page

    @classmethod
    def get_size_from_args(cls, args):
        if 'size' in args and args['size']:
            try:
                size = int(args['size'])
            except ValueError:
                raise BadRequest(description='Size is not valid')
        else:
            size = 10
        return size

    @classmethod
    def get_fields_from_args(cls, args):
        if 'filter' in args and args['filter']:
            fields = args['filter'].split()
        else:
            fields = None
        return fields

    @classmethod
    def filter_by_fields(cls, item, fields):
        return {k: v for k, v in item.items() if k in fields}
