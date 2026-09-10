from ideas.examples import export_keyword
from tests.export_keyword import sources

def test_single_line_transformations():
    assert export_keyword.transform_source(sources.source_1) == sources.expected_1
    assert export_keyword.transform_source(sources.source_2) == sources.expected_2
    assert export_keyword.transform_source(sources.source_3) == sources.expected_3

    assert export_keyword.transform_source(sources.source_4) == sources.expected_4
    assert export_keyword.transform_source(sources.source_5) == sources.expected_5
    assert export_keyword.transform_source(sources.source_6) == sources.expected_6

    assert export_keyword.transform_source(sources.source_7) == sources.expected_7
    assert export_keyword.transform_source(sources.source_8) == sources.expected_8
    assert export_keyword.transform_source(sources.source_9) == sources.expected_9

def test_ignore_export_inside_class_or_def():
    assert export_keyword.transform_source(sources.source_10) == sources.expected_10

def test_indented_export_var():
    assert export_keyword.transform_source(sources.source_11) == sources.expected_11

def test_indented_class_or_def():
    assert export_keyword.transform_source(sources.source_12) == sources.expected_12

