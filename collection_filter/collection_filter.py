import jsonpath_rw


def collection_filter(data, fields):
    '''Filter data by fields

    *** Confession ***
    @kudochien: I know this code is really complicated and dirty.
    Even the author does not exactly known what he had written,
    I guess the implementation may some how turn to use recursive.
    However, for my incapacity,
    I failed but with hybrid iterative and recursive.
    Thus makes such code looks awful.

    If you talent guy can help me to refactor the code,
    I would express my greatest thank for you.

    Well, please remember to refactor with
    the unit tests to ensure the correctness.
    '''

    if not fields:
        return data
    try:
        field_list = fields.split(',')
    except:
        return data

    if type(data) not in (list, dict):
        raise AssertionError('Only support type list or dict for data')

    def extract_json_matches(matches):
        match_length = len(matches)
        result = None
        if match_length == 1:
            result = matches[0]
        elif match_length > 0:
            result = matches
        return result

    def inner(_data, _field_list, _is_begin):
        if type(_field_list) != list:
            _field_list = (_field_list,)

        if type(_data) == list:
            new_data = []
            for entry in _data:
                assert type(entry) == dict
                new_entry = {}
                for field in _field_list:
                    assert field[:4] == '[*].'
                    field = field[4:]
                    if field:
                        jsonpath_expr = jsonpath_rw.parse(field)
                        matches = [match.value
                                   for match in jsonpath_expr.find(entry)]
                        result = extract_json_matches(matches)
                        if result:
                            new_entry[field] = result
                    else:
                        new_entry.update(entry)
                new_data.append(new_entry)
            return new_data

        elif type(_data) == dict:
            new_data = {}
            for field in _field_list:
                assert field[:4] != '[*].'
                keys = field.split('.')
                key_length = len(keys)
                curr_data = _data
                curr_dict_ref = new_data
                idx = 0
                while idx < key_length:
                    key = keys[idx]
                    is_array_query = key[-3:] == '[*]'
                    key_stripped = key[:-3] if is_array_query else key

                    if idx < key_length - 1:
                        key_for_query = '[*].' + keys[idx + 1] \
                            if is_array_query else keys[idx + 1]
                        idx += 1
                        curr_data = inner(curr_data, key_stripped, False)
                        if not is_array_query:
                            if key_stripped not in curr_dict_ref:
                                curr_dict_ref[key_stripped] = {}
                            curr_dict_ref = curr_dict_ref[key_stripped]
                            key_stripped = key_for_query

                        curr_data = inner(curr_data, key_for_query, False)
                        if curr_dict_ref.get(key_stripped):
                            curr_dict_ref[key_stripped].update(curr_data)
                        else:
                            curr_dict_ref[key_stripped] = curr_data
                    idx += 1

                if field[-3:] == '[*]':
                    field = field[:-3]
                if field in _data:
                    new_data[field] = _data[field]
                    if not _is_begin:
                        return _data[field]
            return new_data
        else:
            return _data

    return inner(data, field_list, True)
