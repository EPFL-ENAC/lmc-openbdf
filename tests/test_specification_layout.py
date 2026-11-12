from __future__ import annotations

from openbdf.model.enums.element_classifications import OpenBDFBuildingElementClassification


def test_a_whole_number_cell_finds_its_element_code():
    # pandas reads a whole-number cell as an int, and any other number cell as a float.
    assert OpenBDFBuildingElementClassification.find_value(2.1).value == "2.1"
    assert OpenBDFBuildingElementClassification.find_value(2).value == "2"
