import os

from pytest import fixture

from genderbias.document import Document

example_dir = os.path.dirname(__file__) + "/../example_letters/"

examples = {
    "m": dict(file=example_dir + "letterofRecM", sentences=16, words=478),
    "f": dict(file=example_dir + "letterofRecW", sentences=27, words=703),
}


@fixture(params=examples.values())
def example_doc(request):
    with open(request.param["file"]) as stream:
        return dict(
            request.param,
            document=Document(request.param["file"]),
            document_string=Document(stream.read()),
        )


def test_can_read_examples(example_doc):
    with open(example_doc["file"], "r") as stream:
        assert stream.readable()


def test_document_from_file_equals_document_from_string(example_doc):
    file = example_doc["document"]
    string = example_doc["document_string"]
    assert file.sentences() == string.sentences()
    assert file.words() == string.words()
    assert file.words_with_indices() == string.words_with_indices()
    assert file.words_with_indices() == string.words_with_indices()


def test_words(example_doc):
    words = example_doc["document"].words()
    assert isinstance(words, list)
    assert len(words) == example_doc["words"]


def test_words_with_indices(example_doc):
    words_with_indices = example_doc["document"].words_with_indices()
    assert len(words_with_indices) == example_doc["words"]
    latest_start = -1
    latest_stop = 0
    for word, start, stop in words_with_indices:
        assert stop >= start
        assert stop >= latest_stop
        latest_stop = stop
        assert start >= latest_start
        latest_start = start


def test_sentence(example_doc):
    s = example_doc["document"].sentences()
    for ss in s:
        assert "\n" not in ss
