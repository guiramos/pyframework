from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_metadata_filter import DocumentMetadataFilter


T = TypeVar("T", bound="DeleteRequest")


@attr.s(auto_attribs=True)
class DeleteRequest:
    """
    Attributes:
        ids (Union[Unset, List[str]]):
        filter_ (Union[Unset, DocumentMetadataFilter]):
        delete_all (Union[Unset, None, bool]):
    """

    ids: Union[Unset, List[str]] = UNSET
    filter_: Union[Unset, "DocumentMetadataFilter"] = UNSET
    delete_all: Union[Unset, None, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        delete_all = self.delete_all

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ids is not UNSET:
            field_dict["ids"] = ids
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if delete_all is not UNSET:
            field_dict["delete_all"] = delete_all

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_metadata_filter import DocumentMetadataFilter

        d = src_dict.copy()
        ids = cast(List[str], d.pop("ids", UNSET))

        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, DocumentMetadataFilter]
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = DocumentMetadataFilter.from_dict(_filter_)

        delete_all = d.pop("delete_all", UNSET)

        delete_request = cls(
            ids=ids,
            filter_=filter_,
            delete_all=delete_all,
        )

        delete_request.additional_properties = d
        return delete_request

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
