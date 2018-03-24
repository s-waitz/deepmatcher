import io
import os

import torchtext
from torchtext import data
from torchtext.utils import unicode_csv_reader

from . import torchtext_extensions as text


def _check_header(header, id_attr, left_prefix, right_prefix, label_attr):
    # assert id_attr in header
    assert label_attr in header

    for attr in header:
        if attr not in (id_attr, label_attr):
            assert attr.startswith(left_prefix) or attr.startswith(right_prefix)

    num_left = sum(attr.startswith(left_prefix) for attr in header)
    num_right = sum(attr.startswith(right_prefix) for attr in header)
    assert num_left == num_right


def _make_fields(header, id_attr, label_attr, lower):
    text_field = text.MatchingField(
        lower=lower, init_token='<<<', eos_token='>>>', batch_first=True, device=-1)
    numeric_field = text.MatchingField(
        sequential=False, preprocessing=lambda x: int(x), use_vocab=False)

    fields = []
    for attr in header:
        if attr == id_attr:
            fields.append((attr, None))
        elif attr == label_attr:
            fields.append((attr, numeric_field))
        else:
            fields.append((attr, text_field))
    return fields


def process(path,
            train,
            validation=None,
            test=None,
            unlabeled=None,
            cache='cacheddata.pth',
            check_cached_data=True,
            auto_rebuild_cache=False,
            shuffle_style='bucket',
            lower=True,
            embeddings='fasttext.en.bin',
            embeddings_cache_path='~/.vector_cache',
            id_attr='id',
            left_prefix='left_',
            right_prefix='right_',
            label_attr='label'):

    with io.open(os.path.expanduser(os.path.join(path, train)), encoding="utf8") as f:
        header = next(unicode_csv_reader(f))

    _check_header(header, id_attr, left_prefix, right_prefix, label_attr)
    fields = _make_fields(header, id_attr, label_attr, lower)
    column_naming = {
        'left_prefix': left_prefix,
        'right_prefix': right_prefix,
        'label': label_attr
    }

    return text.MatchingDataset.splits(path, train, validation, test, unlabeled, fields,
                                       embeddings, embeddings_cache_path, column_naming, cache, check_cached_data,
                                       auto_rebuild_cache)
