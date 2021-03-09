import numpy as np

from Chunks import Chunks

class Dataset:
    name: str
    _chunks: List[Chunks]

    _targets: str # path to npy with targets
    _strays: str # -/\/-
    _train: str
    _test: str

    _main: str # npz

    
