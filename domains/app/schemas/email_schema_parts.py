from pydantic import BaseModel


class XposedLeaf(BaseModel):
    colname: str
    group: str
    name: str
    value: int


class XposedNode(BaseModel):
    name: str
    colname: str
    children: list[XposedLeaf]


class XposedRoot(BaseModel):
    children: list[XposedNode]

XposedData = list[XposedRoot]

IndustryEntry = tuple[str, int]
IndustryGroup = list[IndustryEntry]
IndustryData = list[IndustryGroup]

class RiskItem(BaseModel):
    risk_label: str
    risk_score: int


RiskData = list[RiskItem]

DictWithInts = list[dict[str, int]]