from cargo import Cargo
from main import stringify_options_list, is_float


def test_get_edited_list():
    ...


def test_cargo_grid_size_and_type_are_calculated():
    cargo = Cargo(ID="La_Sm", name="a", space=0, weight=0)
    assert cargo.grid_size == "La" and cargo.type == "Sm"


def test_stringify_options_list_with_two_options():
    assert stringify_options_list(["a", "b"]) == "'a' or 'b'"


def test_stringify_options_list_with_three_options():
    assert stringify_options_list(["a", "b", "c"]) == "'a', 'b', or 'c'"


def test_is_float():
    assert is_float("5")
    assert not is_float("a")
    assert not is_float("1..5")
    assert is_float("1.5")
