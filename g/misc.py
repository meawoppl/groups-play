def pairs(thing):
    assert len(thing) >= 2, "Length is too small :/"
    for first, second in zip(thing[:-1], thing[1:]):
        yield first, second

