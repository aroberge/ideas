from ideas.examples import export_keyword
from tests.export_keyword import sources

def test_single_line_transformations():
    assert export_keyword.transform_source(sources.source_1) == sources.expected_1
    assert export_keyword.transform_source(sources.source_2) == sources.expected_2
    assert export_keyword.transform_source(sources.source_3) == sources.expected_3
