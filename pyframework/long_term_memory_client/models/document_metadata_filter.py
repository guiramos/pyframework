from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.source import Source
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentMetadataFilter")


@attr.s(auto_attribs=True)
class DocumentMetadataFilter:
    """
    Attributes:
        document_id (Union[Unset, str]):
        source (Union[Unset, Source]): An enumeration.
        source_id (Union[Unset, str]):
        author (Union[Unset, str]):
        start_date (Union[Unset, str]):
        end_date (Union[Unset, str]):
    """

    document_id: Union[Unset, str] = UNSET
    source: Union[Unset, Source] = UNSET
    source_id: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    start_date: Union[Unset, str] = UNSET
    end_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_id = self.document_id
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        source_id = self.source_id
        author = self.author
        start_date = self.start_date
        end_date = self.end_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if document_id is not UNSET:
            field_dict["document_id"] = document_id
        if source is not UNSET:
            field_dict["source"] = source
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if author is not UNSET:
            field_dict["author"] = author
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_id = d.pop("document_id", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, Source]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = Source(_source)

        source_id = d.pop("source_id", UNSET)

        author = d.pop("author", UNSET)

        start_date = d.pop("start_date", UNSET)

        end_date = d.pop("end_date", UNSET)

        document_metadata_filter = cls(
            document_id=document_id,
            source=source,
            source_id=source_id,
            author=author,
            start_date=start_date,
            end_date=end_date,
        )

        document_metadata_filter.additional_properties = d
        return document_metadata_filter

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
