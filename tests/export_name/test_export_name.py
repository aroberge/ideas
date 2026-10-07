from ideas.included import export_name
from tests.export_name import sources


def test_single_line_transformations():
    assert (
        export_name.transform_source(sources.source_1).strip()
        == sources.expected_1.strip()
    )
    assert (
        export_name.transform_source(sources.source_2).strip()
        == sources.expected_2.strip()
    )
    assert (
        export_name.transform_source(sources.source_3).strip()
        == sources.expected_3.strip()
    )

    assert (
        export_name.transform_source(sources.source_4).strip()
        == sources.expected_4.strip()
    )
    assert (
        export_name.transform_source(sources.source_5).strip()
        == sources.expected_5.strip()
    )
    assert export_name.transform_source(sources.source_6) == sources.expected_6

    assert (
        export_name.transform_source(sources.source_7).strip()
        == sources.expected_7.strip()
    )
    assert (
        export_name.transform_source(sources.source_8).strip()
        == sources.expected_8.strip()
    )
    assert (
        export_name.transform_source(sources.source_9).strip()
        == sources.expected_9.strip()
    )


def test_ignore_export_inside_class_or_def():
    assert (
        export_name.transform_source(sources.source_10).strip()
        == sources.expected_10.strip()
    )


def test_indented_export_var():
    assert (
        export_name.transform_source(sources.source_11).strip()
        == sources.expected_11.strip()
    )


def test_indented_class_or_def():
    assert (
        export_name.transform_source(sources.source_12).strip()
        == sources.expected_12.strip()
    )


def test_weird_indentation():
    assert (
        export_name.transform_source(sources.source_13).strip()
        == sources.expected_13.strip()
    )
