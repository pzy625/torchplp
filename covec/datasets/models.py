# -*- coding: utf-8 -*-
"""
models.py - The covec dataset model defination

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import os
import pathlib
import pickle
import numpy as np
import torch
from torch.utils import data


class Dataset(object):
    """Upper dataset class"""

    def __init__(self, root):
        # expand given path
        self._rootp = pathlib.Path(root).expanduser()
        # create unique directory in datapath to save datasets
        self._rootp = self._rootp / str(self)
        self._rootp.mkdir(parents=True, exist_ok=True)
        # create raw path to save raw datasets
        self._rawp = self._rootp / 'raw'
        self._rawp.mkdir(parents=True, exist_ok=True)
        # create cooked path to save processed datasets (vector data)
        self._cookp = self._rootp / 'cook'
        self._cookp.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return self.__class__.__name__

class TorchSet(data.Dataset):
    """The Pytorch Dataset"""

    def __init__(self, X, Y):
        self._X = torch.Tensor(self.padding(X)).float()
        self._Y = torch.Tensor(Y).long()

    def __getitem__(self, index):
        return self._X[index], self._Y[index]

    def __len__(self):
        return len(self._X)

class TorchPathSet(data.Dataset):
    def __init__(self, path):
        self._X = list(path.glob('**/*.p')).sort()
        self._Y = pickle.load(str(path / 'Y.p'))
        assert len(self._X) == len(self._Y)

    def __getitem__(self, index):
        x = self._X[index]
        y = self._Y[index]
        x = pickle.load(str(x))
        x = torch.as_tensor(x).float()
        y = torch.as_tensor(y).long()
        return x, y

    def __len__(self):
        return len(self._Y)
