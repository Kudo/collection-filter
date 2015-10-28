# flake8: noqa for E501
import pytest

from collection_filter import dict_utils


class Test_DictUtils(object):

    def test_UnionSimpleDict_ReturnUnionData(self):
        # Arrange
        dict1 = {'foo': 1}
        dict2 = {'bar': 2}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'foo': 1, 'bar': 2}

    def test_UnionDeepDict_ReturnUnionData(self):
        # Arrange
        dict1 = {'deep': {'foo': 1}}
        dict2 = {'deep': {'bar': 2}}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'deep': {'foo': 1, 'bar': 2}}

    def test_UnionDeepDictWithExtraDataInDict1_KeepExtraData(self):
        # Arrange
        dict1 = {'deep': {'foo': 1}, 'extra': True}
        dict2 = {'deep': {'bar': 2}}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'deep': {'foo': 1, 'bar': 2}, 'extra': True}

    def test_UnionDeepDictWithExtraDataInDict2_KeepExtraData(self):
        # Arrange
        dict1 = {'deep': {'foo': 1}}
        dict2 = {'deep': {'bar': 2}, 'extra': True}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'deep': {'foo': 1, 'bar': 2}, 'extra': True}

    def test_UnionDictImmutateDict_DictsAsOrigin(self):
        # Arrange
        dict1 = {'deep': {'foo': 1}}
        dict2 = {'deep': {'bar': 2}}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert dict1 == {'deep': {'foo': 1}}
        assert dict2 == {'deep': {'bar': 2}}

    def test_UnionDictWithList_ReturnUnionData(self):
        # Arrange
        dict1 = {'deep': [{'foo': 1}, {'foo': 2}]}
        dict2 = {'deep': [{'bar': 3}, {'bar': 4}]}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'deep': [{'foo': 1, 'bar': 3}, {'foo': 2, 'bar': 4}]}

    def test_UnionDictListFromEmpty_ReturnUnionData(self):
        # Arrange
        dict1 = {}
        dict2 = {'deep': [{'bar': 3}, {'bar': 4}]}

        # Act
        result = dict_utils.dict_union(dict1, dict2)

        # Assert
        assert result == {'deep': [{'bar': 3}, {'bar': 4}]}

    def test_IntersectDictSimple_ReturnIntersectData(self):
        # Arrange
        dict1 = {'foo': 1, 'bar': 2}
        dict2 = {'foo': 1}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {'foo': 1}

    def test_IntersectDictDeep_ReturnIntersectData(self):
        # Arrange
        dict1 = {'deep': {'foo': 1, 'bar': 2}}
        dict2 = {'deep': {'foo': 1}}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {'deep': {'foo': 1}}


    def test_IntersectDictToEmpty_ReturnEmptyData(self):
        # Arrange
        dict1 = {'foo': 1, 'bar': 2}
        dict2 = {}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {}

    def test_IntersectDictImmutable_ExpectOriginData(self):
        # Arrange
        dict1 = {'foo': 1, 'bar': 2}
        dict2 = {'foo': 1}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert dict1 == {'foo': 1, 'bar': 2}
        assert dict2 == {'foo': 1}

    def test_IntersectDictDifferentType_ReturnDict2Value(self):
        # Arrange
        dict1 = {'foo': 1}
        dict2 = {'foo': [1, 2, 3]}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {'foo': [1, 2, 3]}

    def test_IntersectDictDifferentPrimitiveValue_ReturnDict2Value(self):
        # Arrange
        dict1 = {'foo': 1}
        dict2 = {'foo': 2}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {'foo': 2}

    def test_IntersectDictWithList_ReturnDeepIntersect(self):
        # Arrange
        dict1 = {'deep': [{'foo': 1}, {'bar': 2}]}
        dict2 = {'deep': [{'foo': 1}]}

        # Act
        result = dict_utils.dict_intersect(dict1, dict2)

        # Assert
        assert result == {'deep': [{'foo': 1}]}
