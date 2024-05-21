# cython: language_level=3
from cython cimport boundscheck, wraparound
import os

@boundscheck(False)
@wraparound(False)
cdef void save_states_impl(str path):
    cdef str root, file
    cdef unsigned long s
    cdef list states = []
    cdef FILE* f
    f = fopen("states.txt", "w")
    if not f:
        raise FileNotFoundError("Failed to open file")
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                s = os.path.getmtime(os.path.join(root, file))
                states.append(s)
                fprintf(f, "%f\n", s)
    finally:
        fclose(f)

def save_states(path):
    save_states_impl(path.encode())

@boundscheck(False)
@wraparound(False)
cdef void detect_changed_state_impl(str path):
    cdef list states = []
    cdef list modified = []
    cdef FILE* f
    cdef str line, abs_path, file
    cdef unsigned long s
    f = fopen("states.txt", "r")
    if not f:
        raise FileNotFoundError("Failed to open file")
    try:
        for line in f:
            states.append(float(line.strip()))
        for root, dirs, files in os.walk(path):
            for file in files:
                abs_path = os.path.join(root, file)
                s = os.path.getmtime(abs_path)
                if s not in states:
                    modified.append(abs_path)
    finally:
        fclose(f)
    return modified

def detect_changed_state(path):
    return detect_changed_state_impl(path.encode())
