import sys; sys.path.append(".")


def test__normalize_query_patch():
    # This import should patch normalize_query
    from slack_overflow.google_search import search
    # And now we import and check normalize_query to assert
    #  that it has
    import google
    assert google.modules.utils.normalize_query(":+& ") == ":+& "
