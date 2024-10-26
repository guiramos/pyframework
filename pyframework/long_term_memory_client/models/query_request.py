from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.query import Query


T = TypeVar("T", bound="QueryRequest")


@attr.s(auto_attribs=True)
class QueryRequest:
    """
    Attributes:
        queries (List['Query']):
    """

    queries: List["Query"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queries = []
        for queries_item_data in self.queries:
            queries_item = queries_item_data.to_dict()

            queries.append(queries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queries": queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query import Query

        d = src_dict.copy()
        queries = []
        _queries = d.pop("queries")
        for queries_item_data in _queries:
            queries_item = Query.from_dict(queries_item_data)

            queries.append(queries_item)

        query_request = cls(
            queries=queries,
        )

        query_request.additional_properties = d
        return query_request

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
