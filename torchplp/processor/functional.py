# -*- coding: utf-8 -*-
"""
functional.py - The collection of process function

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import numpy as np
from torchplp.utils import ASTNode

def standardize(root):
    var_names = []
    fun_names = []
    root.data = 'func_name'
    for node in root.walk():
        if node.kind == 'VAR_DECL':
            var_names.append(node.data)
        if node.kind == 'FUNCTION_DECL':
            fun_names.append(node.data)
    for node in root.walk():
        if node.data in var_names:
            node.data = f'var{var_names.index(node.data)}'
        if node.data in fun_names:
            node.data = f'fun{fun_names.index(node.data)}'
    return root

def tree2seq(data, path='DFS'):
    """transform tree structrue to sequence"""
    assert isinstance(data, ASTNode)
    return list(data.walk(path))

def vectorlize(data, embedder):
    """transform sequence data to its vector representation"""
    vr = []
    for node in data:
        try:
            vec = embedder[node.data] if node.data else embedder[node.kind]
        except Exception:
            vec = np.zeros(embedder.vector_size)
        vr.append(vec.tolist())
    vr = np.array(vr)
    return vr

def tree_slicing(root):
    for node in root.walk():
        if node.kind == 'CALL_EXPR':
            pass
