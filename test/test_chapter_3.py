import itertools

import pytest

from chapter_3 import TuringMachine, parse_turing_program
from chapter_3 import \
    source_tp_constant_one, \
    source_tp_ex_3_3, \
    source_tp_ex_3_4
from resources.turing_programs import \
    prog_print_XYZ, \
    prog_compute_constant_1
from resources import turing_sources


@pytest.mark.parametrize("source,start,halt,inp,out", [
    # f(n)=1:
    (source_tp_constant_one, "S", "H", "▶1001", "▶1"),
    (source_tp_constant_one, "S", "H", "▶11", "▶1"),
    (source_tp_constant_one, "S", "H", "▶0", "▶1"),
    # exercise 3.3 (reverse bitstring)
    (source_tp_ex_3_3, "START", "HALT", "▶011", "▶110"),
    (source_tp_ex_3_3, "START", "HALT", "▶101011", "▶110101"),
    (source_tp_ex_3_3, "START", "HALT", "▶1010110000", "▶0000110101"),
    (source_tp_ex_3_3, "START", "HALT", "▶1", "▶1"),
    (source_tp_ex_3_3, "START", "HALT", "▶0", "▶0"),
    (source_tp_ex_3_3, "START", "HALT", "▶", "▶"),  # corner case
    # If at least n+1 (n=length of bitstring) blanks follow the input, then the
    # turing machine is guaranteed "to work" (see its docstring).
    (source_tp_ex_3_3, "START", "HALT", "▶001■■■■xyz", "▶100■■■■xyz"),
    # exercise 3.4 (add modulo 2)
    (source_tp_ex_3_4, "START", "HALT", "▶0■0", "▶0"),
    (source_tp_ex_3_4, "START", "HALT", "▶0■1", "▶1"),
    (source_tp_ex_3_4, "START", "HALT", "▶1■0", "▶1"),
    (source_tp_ex_3_4, "START", "HALT", "▶1■1", "▶0"),
    (source_tp_ex_3_4, "START", "HALT", "▶01■10", "▶11"),
    (source_tp_ex_3_4, "START", "HALT", "▶11■11", "▶00"),
    (source_tp_ex_3_4, "START", "HALT", "▶010■111", "▶101"),
    (source_tp_ex_3_4, "START", "HALT", "▶1100■0101", "▶1001"),
    (source_tp_ex_3_4, "START", "HALT", "▶0111001■1101001", "▶1010000"),
], ids=itertools.count())  # ids set like this since default looks ugly
def test_TuringMachine_fromSource(source, start, halt, inp, out):
    tm = TuringMachine.fromSource(source, start_state=start, halt_state=halt)
    assert tm.run(inp) == out


@pytest.mark.parametrize("program,start,halt,inp,out", [
    # f(n)=1:
    (prog_compute_constant_1, "S", "H", "▶0", "▶1"),
    (prog_compute_constant_1, "S", "H", "▶1", "▶1"),
    (prog_compute_constant_1, "S", "H", "▶1011", "▶1"),
    # print XYZ on an empty tape, leave tape untouched if first cell contains something
    (prog_print_XYZ, "S", "H", "", "XYZ"),
    (prog_print_XYZ, "S", "H", "a", "a"),
    (prog_print_XYZ, "S", "H", "X", "X"),
], ids=itertools.count())
def test_TuringMachine(program, start, halt, inp, out):
    tm = TuringMachine(program, start_state=start, halt_state=halt)
    assert tm.run(inp) == out


@pytest.mark.parametrize("src_and_results", [
    turing_sources.comments_and_indentation,
])
def test_parse_turing_program(src_and_results):
    parsed_prog, source_map = parse_turing_program(src_and_results["source"])
    assert parsed_prog == src_and_results["parsed"]
    assert source_map == src_and_results["source_map"]
