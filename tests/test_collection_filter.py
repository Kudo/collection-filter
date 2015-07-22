# flake8: noqa for E501
import pytest

from collection_filter import collection_filter


class Test_CollectionFilter(object):

    # ################################################################
    # Input data as dict
    # ################################################################
    def test_PartialDataFilter_DataDictWithFieldsEmpty_ReturnOriginalData(self):
        # Arrange
        data = {'foo': 'bar'}
        fields = None

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert data == result

    def test_PartialDataFilter_DataDictWithFieldsEmptyString_ReturnOriginalData(self):
        # Arrange
        data = {'foo': 'bar'}
        fields = ''

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert data == result

    def test_PartialDataFilter_DataDictWithFieldsOneElement_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'bar': 2}
        fields = 'foo'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'foo': 1}

    def test_PartialDataFilter_DataDictWithFieldsTwoElement_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'bar': 2, 'Alice': 'someone', 'Bob': 'Say Hi!'}
        fields = 'foo,Alice'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'foo': 1, 'Alice': 'someone'}

    def test_PartialDataFilter_DataDictTwoLevelWithFieldsTwoElement_ReturnSubsetData(self):
        # Arrange
        data = {'foo': {'Alice': 'someone', 'Bob': 'Say Hi!', 'orange': 'banana'}}
        fields = 'foo.Alice,foo.orange'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'foo': {'Alice': 'someone', 'orange': 'banana'}}

    def test_PartialDataFilter_DataDictIncludeListWithFieldsSimpleKeyQuery_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'aList': [{'elem1': 1}, {'elem2': 2}, {'elem3': 3}]}
        fields = 'aList'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'aList': [{'elem1': 1}, {'elem2': 2}, {'elem3': 3}]}

    def test_PartialDataFilter_DataDictIncludeListWithFieldsArrayKeyQuery_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'aList': [{'elem1': 1}, {'elem2': 2}, {'elem3': 3}]}
        fields = 'aList[*]'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'aList': [{'elem1': 1}, {'elem2': 2}, {'elem3': 3}]}

    def test_PartialDataFilter_DataDictIncludeListWithFieldsDeepKeyQuery_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'aList': [{'elem1': 1}, {'elem2': 2}, {'elem3': 3}]}
        fields = 'aList[*].elem1'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'aList': [{'elem1': 1}, {}, {}]}

    def test_PartialDataFilter_DataDictIncludeListComplexWithFieldsDeepKeyQuery_ReturnSubsetData(self):
        # Arrange
        data = {'foo': 1, 'aList': [{'elem1': {'foo': 1, 'bar': 2}}, {'elem2': {'foo': 'bar'}}, {'elem3': {'foo': 'bar'}}]}
        fields = 'aList[*].elem1.foo'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'aList': [{'elem1': {'foo': 1, 'bar': 2}}, {}, {}]}

    def test_PartialDataFilter_DataDictWithFieldsTwoLevelQuery_ReturnDeepData(self):
        # Arrange
        data = {'aDict': {'bar': 2, 'Alice': 'someone', 'Bob': 'Say Hi!'}}
        fields = 'aDict.Alice'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == {'aDict': {'Alice': 'someone'}}

    def test_PartialDataFilter_DataDictWithFieldsArrayQuery_RaiseException(self):
        # Arrange
        data = {'foo': 1, 'bar': 2}
        fields = '[*].foo'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)

    def test_PartialDataFilter_DataDictWithFieldsInvalidArrayQuerySyntax_RaiseException(self):
        # Arrange
        data = [{'foo': 1}, {'bar': 2}]
        fields = '[*]'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)


    # ################################################################
    # Input data as list
    # ################################################################

    def test_PartialDataFilter_DataListOfObjectWithFieldsEmpty_ReturnOriginalData(self):
        # Arrange
        data = [{'foo': 1}, {'bar': 2}]
        fields = None

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert data == result

    def test_PartialDataFilter_DataListOfObjectWithFieldsEmptyString_ReturnOriginalData(self):
        # Arrange
        data = [{'foo': 1}, {'bar': 2}]
        fields = ''

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert data == result

    def test_PartialDataFilter_DataListWithFieldsArrayQuery_ReturnSubsetOfListData(self):
        # Arrange
        data = [{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4, 'orange': 'banana'}]
        fields = '[*].foo'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == [{'foo': 1}, {'foo': 3}]

    def test_PartialDataFilter_DataListWithFieldsTwoArrayQuery_ReturnSubsetOfListData(self):
        # Arrange
        data = [{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4, 'orange': 'banana'}]
        fields = '[*].foo,[*].bar'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == [{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4}]

    def test_PartialDataFilter_DataListWithFieldsNonexistingArrayQuery_ReturnEmptyListData(self):
        # Arrange
        data = [{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4, 'orange': 'banana'}]
        fields = '[*].nonexisted'

        # Act
        result = collection_filter(data, fields)

        # Assert
        assert result == [{}, {}]

    def test_PartialDataFilter_DataListWithFieldOneKey_RaiseException(self):
        # Arrange
        data = [{'foo': 1}, {'bar': 2}]
        fields = 'foo'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)


    # ################################################################
    # Input data which is NOT supported
    # ################################################################

    def test_PartialDataFilter_DataPrimitiveTypeWithFieldsDontCare_RaiseException(self):
        # Arrange
        data = 1
        fields = 'foo'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)

    def test_PartialDataFilter_DataListOfPrimitiveTypeWithFieldsDontCare_RaiseException(self):
        # Arrange
        data = [1, 2, 3]
        fields = 'foo'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)

    def test_PartialDataFilter_DataListOfListWithFieldsDontCare_RaiseException(self):
        # Arrange
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        fields = 'foo'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)

    def test_PartialDataFilter_DataListOfPrimitiveTypeWithFieldsArrayQuery_RaiseException(self):
        # Arrange
        data = [1, 2, 3]
        fields = '[*].address'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)

    def test_PartialDataFilter_DataListOfListWithFieldsArrayQuery_RaiseException(self):
        # Arrange
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        fields = '[*].address'

        # Act & Assert
        with pytest.raises(AssertionError):
            result = collection_filter(data, fields)
