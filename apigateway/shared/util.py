def find_by_ids(data, ids):
    return [datum for datum in data if datum['_id'] in ids]
