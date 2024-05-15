from dto.base import BaseDTO, ConfigDict

InstrumentID = str

class ResultBaseDTO(BaseDTO):
    model_config = ConfigDict(
        from_attributes=True
    )

class ResultProfileStructureDTO(ResultBaseDTO):
    total: int

    share_percentage: int
    share_total: int

    bond_percentage: int
    bond_total: int