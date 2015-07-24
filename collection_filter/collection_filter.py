import copy


def _mergedict(dict1, dict2):
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


def _get_next_field(remain_query):
    if not remain_query:
        return None, None

    result = remain_query.split('.', 1)
    if len(result) == 1:
        field = result[0]
        remain_query = None
    else:
        field, remain_query = result
    return field, remain_query


def _inner_filter(inner_data,
                  inner_field,
                  remain_query,
                  expect_list=None):
    if expect_list is None:
        if inner_field and inner_field[:3] == '[*]':
            expect_list = True
        else:
            expect_list = False

    if expect_list:
        assert type(inner_data) == list
        if inner_field[-3:] == '[*]':
            inner_field = inner_field[:-3]
        for idx, element in enumerate(inner_data):
            inner_data[idx] = _inner_filter(element,
                                            inner_field,
                                            remain_query,
                                            expect_list=False)
        return inner_data
    else:
        assert type(inner_data) == dict
        if not inner_field:
            field, remain_query = _get_next_field(remain_query)
            if field:
                return _inner_filter(inner_data, field, remain_query)
            else:
                return inner_data
        if inner_field[-3:] == '[*]':
            expect_list = True
            inner_field = inner_field[:-3]
        result = inner_data.get(inner_field, {})
        field, remain_query = _get_next_field(remain_query)
        if field:
            result = _inner_filter(result,
                                   field,
                                   remain_query,
                                   expect_list=expect_list)
        if result:
            return {inner_field: result}
        else:
            return {}


def collection_filter(data, fields):
    '''Filter data by fields
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
        sub_field, remain_query = _get_next_field(field)
        subset = _inner_filter(copy.copy(data), sub_field, remain_query)
        if data_as_list:
            for idx in range(len(data)):
                result[idx] = _mergedict(result[idx], subset[idx])
        else:
            result = _mergedict(result, subset)
    return result
