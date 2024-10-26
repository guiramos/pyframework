from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_chunk_metadata import DocumentChunkMetadata


T = TypeVar("T", bound="DocumentChunkWithScore")


@attr.s(auto_attribs=True)
class DocumentChunkWithScore:
    """
    Attributes:
        text (str):
        metadata (DocumentChunkMetadata):
        score (float):
        id (Union[Unset, str]):
        embedding (Union[Unset, List[float]]):
    """

    text: str
    metadata: "DocumentChunkMetadata"
    score: float
    id: Union[Unset, str] = UNSET
    embedding: Union[Unset, List[float]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        metadata = self.metadata.to_dict()

        score = self.score
        id = self.id
        embedding: Union[Unset, List[float]] = UNSET
        if not isinstance(self.embedding, Unset):
            embedding = self.embedding

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "metadata": metadata,
                "score": score,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if embedding is not UNSET:
            field_dict["embedding"] = embedding

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_chunk_metadata import DocumentChunkMetadata

        d = src_dict.copy()
        text = d.pop("text")

        metadata = DocumentChunkMetadata.from_dict(d.pop("metadata"))

        score = d.pop("score")

        id = d.pop("id", UNSET)

        embedding = cast(List[float], d.pop("embedding", UNSET))

        document_chunk_with_score = cls(
            text=text,
            metadata=metadata,
            score=score,
            id=id,
            embedding=embedding,
        )

        document_chunk_with_score.additional_properties = d
        return document_chunk_with_score

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
