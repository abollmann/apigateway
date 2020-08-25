def find_by_ids(data, ids):
    return [datum for datum in data if data['_id'] in ids]
