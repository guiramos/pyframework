from typing import Optional

from agent.long_term_memory_client.api.default.upsert_post import sync
from agent.long_term_memory_client.models import UpsertRequest
from agent.long_term_memory_client.api.default.query_post import query_long_term_memory
from agent.long_term_memory_client.models.query_response import get_top_results_above_threshold


def query_information(
    client,
    query: str, user_id=None,  document_id=None, source_id=None, source=None, k=10,
    threshold: Optional[float] = None,
):
    query_response = query_long_term_memory(client=client,
                                            user_id=user_id,
                                            query=query,
                                            document_id=document_id,
                                            source_id=source_id,
                                            source=source, k=k)
    if threshold is None:
        return query_response
    else:
        return get_top_results_above_threshold(query_response, threshold, 100)


def upsert_information(client, document_id, text, source_id, created_at, author, source="chat"):
    upsert_payload = {
        "documents": [
            {
                "text": text,
                "metadata": {
                    "source": source,
                    "source_id": source_id,
                    "created_at": created_at,
                    "author": author,
                }
            }
        ]
    }

    if document_id is not None:
        upsert_payload["documents"][0]["id"] = document_id
        upsert_payload["documents"][0]["metadata"]["document_id"] = document_id

    upsert_request = UpsertRequest.from_dict(upsert_payload)
    return sync(client=client, json_body=upsert_request)
