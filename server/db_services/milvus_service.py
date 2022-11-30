from pymilvus import (
    connections,
    Collection,
)


def connect_to_milvus(alias, host, port):
    print(f"Connecting to milvus; host: {host}, port: {port}")
    connections.connect(alias=alias, host=host, port=port)


def get_collection(collection_name):
    collection = Collection(collection_name)
    collection.load()

    return Collection(collection_name)


def perform_similarity_search(collection, feature_vector, anns_field,
                              output_fields, offset, limit):
    return collection.search(
        data=[feature_vector],
        anns_field=anns_field,
        param={},
        offset=offset,
        limit=limit,
        output_fields=output_fields,
        consistency_level="Strong"
    )


def query_collection(collection, query_string, output_fields):
    return collection.query(
        expr=query_string,
        output_fields=output_fields,
        consistency_level="Strong"
    )
