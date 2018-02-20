from flask import Flask
from flask import request
from flask import current_app    
from flask import make_response,Response 
from google.cloud import datastore
builtin_list = list
app = Flask(__name__)
def init_app(app):
    pass
def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])
# [START from_datastore]
def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity
# [END from_datastore]

# [START update]
def update(data,keys,id=None):
    ds = get_client()
    if id:
        key = ds.key(keys, int(id))
    else:
        key = ds.key(keys)

    entity = datastore.Entity(key=key)

    entity.update(data)

    ds.put(entity)

    return from_datastore(entity)


create = update
# [END update]

 # [START list]
def list(limit=10, cursor=None,kinds=None,order=None):
    ds = get_client()

    query = ds.query(kind=kinds)
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor
# [END list]

 # [START lookup]
def lookup(kinds,filter):
    ds = get_client()

    query = ds.query(kind=kinds)

    key,value = filter

    query.add_filter(key, '=', value)

    page = query.fetch()

    #print(list(page))

    entities = builtin_list(map(from_datastore, page))

    return entities
# [END lookup]


