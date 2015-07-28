import copy


def _mergedict(dict1, dict2):
    '''Merge two dictionaries and return the new dictionary
    '''
    def _merge_inner(inner_dict1, inner_dict2):
        for key, value in inner_dict1.items():
            if isinstance(value, dict):
                # get node or create one
                node = inner_dict2.setdefault(key, {})
                _merge_inner(value, node)
            else:
                inner_dict2[key] = value
        return inner_dict2

    # Immutable dict2
    return _merge_inner(dict1, copy.copy(dict2))


def _get_next_field(query):
    '''Parse query string to return a field and remaining query string
    '''
    if not query:
        return None, None

    result = query.split('.', 1)
    if len(result) == 1:
        field = result[0]
        remain_query = None
    else:
        field, remain_query = result
    return field, remain_query


def _inner_filter(data,
                  field,
                  remain_query,
                  expect_list=None):
    '''Inner function for recursive

    :param data: collection data
    :param field: a sub field name (a.k.a. without comma or dot)
    :param remain_query: remain query string next to `field`
    :param expect_list: True/False to handle the `data` input as list or not.
        Given default None will decide the input `field` format

    :returs: filtered list or dictionary
    '''

    # Check inputs
    if expect_list is None:
        if field and field[:2] == '[]':
            expect_list = True
        else:
            expect_list = False

    if expect_list:
        # `data` is list
        assert type(data) == list
        if field[-2:] == '[]':
            field = field[:-2]
        for idx, element in enumerate(data):
            data[idx] = _inner_filter(element,
                                      field,
                                      remain_query,
                                      expect_list=False)
        return data
    else:
        # `data` is dict
        assert type(data) == dict
        if not field:
            # If current field query is empty, try to fetch next query
            # The case happens such as '[].foo' case but not 'aKey[].foo' case
            next_field, remain_query = _get_next_field(remain_query)
            if next_field:
                # '[].foo' case
                return _inner_filter(data, next_field, remain_query)
            else:
                # '[]' case
                return data

        if field[-2:] == '[]':
            expect_list = True
            field = field[:-2]

        # Fetch subset dict data by field
        result = data.get(field)

        # Do next query if need
        next_field, remain_query = _get_next_field(remain_query)
        if next_field and result is not None:
            result = _inner_filter(result,
                                   next_field,
                                   remain_query,
                                   expect_list=expect_list)

        # Return {field: result} if there are existed next query
        # Otherwise, return empty dictionary
        if result is not None:
            return {field: result}
        else:
            return {}


def collection_filter(data, fields):
    '''Filter data by fields query
    '''

    # [0] Validations
    if not fields:
        return data

    if type(data) not in (list, dict):
        raise AssertionError('Only support type list or dict for data')

    data_as_list = type(data) == list
    if data_as_list:
        result = [{} for _ in range(len(data))]
    else:
        result = {}

    # [1] First to split comma sperated field query
    for field in fields.split(','):
        # [2] For each dot notated sub field, do further query recursively
        next_field, remain_query = _get_next_field(field)
        subset = _inner_filter(copy.copy(data), next_field, remain_query)
        if data_as_list:
            # [3-1] For list, set each element as merged dictionary
            for idx in range(len(data)):
                result[idx] = _mergedict(result[idx], subset[idx])
        else:
            # [3-2] For dictionary, simply do merge
            result = _mergedict(result, subset)
    return result
