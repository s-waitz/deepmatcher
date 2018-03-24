import pdb

import six

import deepmatcher as dm
import torch

from ..data import AttrTensor

# From onmt-py
def sequence_mask(lengths, max_len=None):
    """
    Creates a boolean mask from sequence lengths.
    """
    batch_size = lengths.numel()
    max_len = max_len or lengths.max()
    mask = (torch.arange(0, max_len).type_as(lengths).repeat(batch_size, 1).lt(
        lengths.unsqueeze(1)))
    pdb.set_trace()
    return mask


def get_module(cls, op, required=False, op_kwarg=None, **kwargs):
    if op is None and not required or isinstance(op, cls):
        return op
    elif required:
        return cls(**kwargs)
    elif isinstance(op, six.string_types):
        if op_kwarg is not None:
            kwargs[op_kwarg] = op
            return cls(**kwargs)
        else:
            return cls(op, **kwargs)
    elif six.callable(op):
        return dm.modules.LazyModuleFn(op)
    else:
        raise ValueError(
            str(cls) + ' arg must be a valid string, a ' + str(cls) + ' object, or a '
            'callable.')


def check_nan(*values):
    for value in values:
        if isinstance(value, AttrTensor):
            value = value.data
        if isinstance(value, torch.Tensor) and (tensor != tensor).any():
            print('NaN detected!!!')
            pdb.set_trace()
