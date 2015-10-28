import copy


def dict_union(dict1, dict2):
    '''Return the union of two dictionaries
    '''
    def _union_inner(inner_dict1, inner_dict2):
        new_dict = copy.deepcopy(inner_dict1)
        for key, value in inner_dict2.items():
            if type(value) == dict:
                node = new_dict.setdefault(key, {})
                unioned_value = _union_inner(value, node)
            elif type(value) == list:
                if inner_dict1.get(key):
                    unioned_value = [_union_inner(inner_dict1[key][idx],
                                                  inner_dict2[key][idx])
                                     for idx in range(len(value))]
                else:
                    unioned_value = copy.copy(inner_dict2[key])
            else:
                unioned_value = new_dict.get(key) or value

            new_dict[key] = unioned_value

        return new_dict

    # Immutable dict2
    return _union_inner(dict1, dict2)


def dict_intersect(dict1, dict2):
    '''Return the intersection of two dictionaries
    '''
    def _intersect_inner(inner_dict1, inner_dict2):
        new_dict = {}
        for key, value1 in inner_dict1.items():
            value2 = inner_dict2.get(key)
            if not value2:
                continue
            if type(value1) != type(value2):
                intersected_value = value2
            elif type(value1) == dict:
                intersected_value = _intersect_inner(value1, value2)
            elif type(value1) == list:
                intersected_value = [_intersect_inner(value1[idx],
                                                      value2[idx])
                                     for idx in
                                     range(min(len(value1), len(value2)))]
            else:
                intersected_value = value2

            new_dict[key] = intersected_value

        return new_dict

    # Immutable dict2
    return _intersect_inner(dict1, dict2)
