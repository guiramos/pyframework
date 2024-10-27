from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.source import Source
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentChunkMetadata")


@attr.s(auto_attribs=True)
class DocumentChunkMetadata:
    """
    Attributes:
        source (Union[Unset, Source]): An enumeration.
        source_id (Union[Unset, str]):
        url (Union[Unset, str]):
        created_at (Union[Unset, str]):
        author (Union[Unset, str]):
        document_id (Union[Unset, str]):
    """

    source: Union[Unset, Source] = UNSET
    source_id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    document_id: Union[Unset, str] = UNSET
    doc_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        source_id = self.source_id
        url = self.url
        created_at = self.created_at
        author = self.author
        document_id = self.document_id
        doc_type = self.doc_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if url is not UNSET:
            field_dict["url"] = url
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if author is not UNSET:
            field_dict["author"] = author
        if document_id is not UNSET:
            field_dict["document_id"] = document_id
        if doc_type is not UNSET:
            field_dict["doc_type"] = doc_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _source = d.pop("source", UNSET)
        source: Union[Unset, Source]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = Source(_source)

        source_id = d.pop("source_id", UNSET)

        url = d.pop("url", UNSET)

        created_at = d.pop("created_at", UNSET)

        author = d.pop("author", UNSET)

        document_id = d.pop("document_id", UNSET)

        doc_type = d.pop("doc_type", UNSET)

        document_chunk_metadata = cls(
            source=source,
            source_id=source_id,
            url=url,
            created_at=created_at,
            author=author,
            document_id=document_id,
            doc_type=doc_type,
        )

        document_chunk_metadata.additional_properties = d
        return document_chunk_metadata

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
