from typing import List
import numpy as np

from Matrix import Matrix

class Chunk:
    _origin: boolean
    _value: str # path to npy

class Chunks:
    _chunks: List[Chunk]
    _is_target: boolean # target or stray

    _width: int
    _length: int

    _motherMatrix: Matrix
    _coordinates: List[int] # azimuth & distance
