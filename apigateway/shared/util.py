def find_by_ids(data, ids):
    return [datum for datum in data if datum['_id'] in ids]


def find_by_id(data, entity_id):
    found = find_by_ids(data, [entity_id])
    if found:
        return found[0]
    return None
