from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.document_chunk_with_score import DocumentChunkWithScore


T = TypeVar("T", bound="QueryResult")


@attr.s(auto_attribs=True)
class QueryResult:
    """
    Attributes:
        query (str):
        results (List['DocumentChunkWithScore']):
    """

    query: str
    results: List["DocumentChunkWithScore"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_chunk_with_score import DocumentChunkWithScore

        d = src_dict.copy()
        query = d.pop("query")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = DocumentChunkWithScore.from_dict(results_item_data)

            results.append(results_item)

        query_result = cls(
            query=query,
            results=results,
        )

        query_result.additional_properties = d
        return query_result

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
