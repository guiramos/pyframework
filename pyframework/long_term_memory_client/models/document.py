from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_metadata import DocumentMetadata


T = TypeVar("T", bound="Document")


@attr.s(auto_attribs=True)
class Document:
    """
    Attributes:
        text (str):
        id (Union[Unset, str]):
        metadata (Union[Unset, DocumentMetadata]):
    """

    text: str
    id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "DocumentMetadata"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        id = self.id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_metadata import DocumentMetadata

        d = src_dict.copy()
        text = d.pop("text")

        id = d.pop("id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, DocumentMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = DocumentMetadata.from_dict(_metadata)

        document = cls(
            text=text,
            id=id,
            metadata=metadata,
        )

        document.additional_properties = d
        return document

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
