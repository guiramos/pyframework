from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.document import Document


T = TypeVar("T", bound="UpsertRequest")


@attr.s(auto_attribs=True)
class UpsertRequest:
    """
    Attributes:
        documents (List['Document']):
    """

    documents: List["Document"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()

            documents.append(documents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documents": documents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document import Document

        d = src_dict.copy()
        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = Document.from_dict(documents_item_data)

            documents.append(documents_item)

        upsert_request = cls(
            documents=documents,
        )

        upsert_request.additional_properties = d
        return upsert_request

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
