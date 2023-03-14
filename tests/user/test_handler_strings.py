from webapp.utils.handler_strings import split_row_book_delete


def test__split_row_book_delete__return_correct_tuple_with_space():
    assert split_row_book_delete('test1 / test2') == ('test1', 'test2')


def test__split_row_book_delete__return_correct_tuple_without_space():
    assert split_row_book_delete('test1/test2') == ('test1', 'test2')
