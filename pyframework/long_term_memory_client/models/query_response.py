from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from . import DocumentChunkWithScore

if TYPE_CHECKING:
    from ..models.query_result import QueryResult


T = TypeVar("T", bound="QueryResponse")


@attr.s(auto_attribs=True)
class QueryResponse:
    """
    Attributes:
        results (List['QueryResult']):
    """

    results: List["QueryResult"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query_result import QueryResult

        d = src_dict.copy()
        if "detail" in src_dict:
            query_response = cls(
                results=[]
            )
            query_response.additional_properties = d
            return query_response

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = QueryResult.from_dict(results_item_data)

            results.append(results_item)

        query_response = cls(
            results=results,
        )

        query_response.additional_properties = d
        return query_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


def concatenate_query_response_texts(results: List[DocumentChunkWithScore]) -> str:
    top_results_sorted_by_id = sorted(results, key=lambda result: result.id)

    all_texts = []
    for document in top_results_sorted_by_id:
        all_texts.append(document.text + f"   Stored at {document.metadata.created_at}")

    return '\n'.join(all_texts)


def create_json_payload_from_results(results: List[DocumentChunkWithScore]):
    # Sort the results by score in descending order
    sorted_results = sorted(results, key=lambda result: result.score, reverse=True)

    payload = []

    document_ids = set()
    for document in sorted_results:
        if document.metadata.document_id not in document_ids:
            doc_dict = {
                'document_id': document.metadata.document_id,
                'text': document.text,
                'created_at': document.metadata.created_at,
                'source_id': document.metadata.source_id,
                'doc_type': document.metadata.doc_type,
                'score': document.score
            }
            payload.append(doc_dict)
            document_ids.add(document.metadata.document_id)

    return payload


def get_top_results_above_threshold(query_response: QueryResponse, threshold: float, n: 100) -> List[DocumentChunkWithScore]:
    # Combine all results from all queries
    combined_results = [result for query_result in query_response.results for result in query_result.results]

    # Filter results with scores above the threshold
    filtered_results = [result for result in combined_results if result.score > threshold]

    # Sort the filtered results by score (in descending order)
    sorted_results = sorted(filtered_results, key=lambda result: result.score, reverse=True)
    # sorted_results = sorted(filtered_results, key=lambda result: result.id)

    # Get the top N results
    top_results = sorted_results[:n]

    return top_results
