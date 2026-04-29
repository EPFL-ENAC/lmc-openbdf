from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import Column, Field, Numeric, SQLModel

from .field_metadata import openbdf_field_metadata


class LCAResultsFullBase(SQLModel):
    gwp_total_a1_a3: Decimal = Field(
        sa_column=Column(Numeric),
        description="Global Warming Potential - Total for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (A1-A3)",
            field_code="gwp_total_a1_a3",
            description="Global Warming Potential - Total for module A1-A3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Required",
        ),
    )

    gwp_total_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (A4)",
            field_code="gwp_total_a4",
            description="Global Warming Potential - Total for module A4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (A5)",
            field_code="gwp_total_a5",
            description="Global Warming Potential - Total for module A5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B1)",
            field_code="gwp_total_b1",
            description="Global Warming Potential - Total for module B1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B2)",
            field_code="gwp_total_b2",
            description="Global Warming Potential - Total for module B2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B3)",
            field_code="gwp_total_b3",
            description="Global Warming Potential - Total for module B3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B4)",
            field_code="gwp_total_b4",
            description="Global Warming Potential - Total for module B4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B5)",
            field_code="gwp_total_b5",
            description="Global Warming Potential - Total for module B5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (B6)",
            field_code="gwp_total_b6",
            description="Global Warming Potential - Total for module B6.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (C1)",
            field_code="gwp_total_c1",
            description="Global Warming Potential - Total for module C1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (C2)",
            field_code="gwp_total_c2",
            description="Global Warming Potential - Total for module C2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (C3)",
            field_code="gwp_total_c3",
            description="Global Warming Potential - Total for module C3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (C4)",
            field_code="gwp_total_c4",
            description="Global Warming Potential - Total for module C4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (D)",
            field_code="gwp_total_d",
            description="Global Warming Potential - Total for module D.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (D1)",
            field_code="gwp_total_d1",
            description="Global Warming Potential - Total for module D1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Total for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Total (D2)",
            field_code="gwp_total_d2",
            description="Global Warming Potential - Total for module D2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_total: Decimal = Field(
        sa_column=Column(Numeric),
        description="Total Global Warming Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Global Warming Potential",
            field_code="gwp_total",
            description="Total Global Warming Potential.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Required",
        ),
    )

    gwp_f_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (A1-A3)",
            field_code="gwp_f_a1_a3",
            description="Global Warming Potential - Fossil for module A1-A3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (A4)",
            field_code="gwp_f_a4",
            description="Global Warming Potential - Fossil for module A4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (A5)",
            field_code="gwp_f_a5",
            description="Global Warming Potential - Fossil for module A5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B1)",
            field_code="gwp_f_b1",
            description="Global Warming Potential - Fossil for module B1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B2)",
            field_code="gwp_f_b2",
            description="Global Warming Potential - Fossil for module B2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B3)",
            field_code="gwp_f_b3",
            description="Global Warming Potential - Fossil for module B3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B4)",
            field_code="gwp_f_b4",
            description="Global Warming Potential - Fossil for module B4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B5)",
            field_code="gwp_f_b5",
            description="Global Warming Potential - Fossil for module B5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (B6)",
            field_code="gwp_f_b6",
            description="Global Warming Potential - Fossil for module B6.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (C1)",
            field_code="gwp_f_c1",
            description="Global Warming Potential - Fossil for module C1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (C2)",
            field_code="gwp_f_c2",
            description="Global Warming Potential - Fossil for module C2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (C3)",
            field_code="gwp_f_c3",
            description="Global Warming Potential - Fossil for module C3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (C4)",
            field_code="gwp_f_c4",
            description="Global Warming Potential - Fossil for module C4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (D)",
            field_code="gwp_f_d",
            description="Global Warming Potential - Fossil for module D.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (D1)",
            field_code="gwp_f_d1",
            description="Global Warming Potential - Fossil for module D1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Fossil for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Fossil (D2)",
            field_code="gwp_f_d2",
            description="Global Warming Potential - Fossil for module D2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_f_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Global Warming Potential - Fossil.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Global Warming Potential - Fossil",
            field_code="gwp_f_total",
            description="Total Global Warming Potential - Fossil.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (A1-A3)",
            field_code="gwp_b_a1_a3",
            description="Global Warming Potential - Biogenic for module A1-A3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (A4)",
            field_code="gwp_b_a4",
            description="Global Warming Potential - Biogenic for module A4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (A5)",
            field_code="gwp_b_a5",
            description="Global Warming Potential - Biogenic for module A5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B1)",
            field_code="gwp_b_b1",
            description="Global Warming Potential - Biogenic for module B1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B2)",
            field_code="gwp_b_b2",
            description="Global Warming Potential - Biogenic for module B2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B3)",
            field_code="gwp_b_b3",
            description="Global Warming Potential - Biogenic for module B3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B4)",
            field_code="gwp_b_b4",
            description="Global Warming Potential - Biogenic for module B4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B5)",
            field_code="gwp_b_b5",
            description="Global Warming Potential - Biogenic for module B5.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (B6)",
            field_code="gwp_b_b6",
            description="Global Warming Potential - Biogenic for module B6.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (C1)",
            field_code="gwp_b_c1",
            description="Global Warming Potential - Biogenic for module C1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (C2)",
            field_code="gwp_b_c2",
            description="Global Warming Potential - Biogenic for module C2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (C3)",
            field_code="gwp_b_c3",
            description="Global Warming Potential - Biogenic for module C3.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (C4)",
            field_code="gwp_b_c4",
            description="Global Warming Potential - Biogenic for module C4.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (D)",
            field_code="gwp_b_d",
            description="Global Warming Potential - Biogenic for module D.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (D1)",
            field_code="gwp_b_d1",
            description="Global Warming Potential - Biogenic for module D1.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Global Warming Potential - Biogenic for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Global Warming Potential - Biogenic (D2)",
            field_code="gwp_b_d2",
            description="Global Warming Potential - Biogenic for module D2.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_b_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Global Warming Potential - Biogenic.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Global Warming Potential - Biogenic",
            field_code="gwp_b_total",
            description="Total Global Warming Potential - Biogenic.",
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module A1-A3."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (A1-A3)"),
            field_code="gwp_luc_a1_a3",
            description=("Global Warming Potential - Land Use and Land Use Change for module A1-A3."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module A4."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (A4)"),
            field_code="gwp_luc_a4",
            description=("Global Warming Potential - Land Use and Land Use Change for module A4."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module A5."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (A5)"),
            field_code="gwp_luc_a5",
            description=("Global Warming Potential - Land Use and Land Use Change for module A5."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B1."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B1)"),
            field_code="gwp_luc_b1",
            description=("Global Warming Potential - Land Use and Land Use Change for module B1."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B2."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B2)"),
            field_code="gwp_luc_b2",
            description=("Global Warming Potential - Land Use and Land Use Change for module B2."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B3."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B3)"),
            field_code="gwp_luc_b3",
            description=("Global Warming Potential - Land Use and Land Use Change for module B3."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B4."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B4)"),
            field_code="gwp_luc_b4",
            description=("Global Warming Potential - Land Use and Land Use Change for module B4."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B5."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B5)"),
            field_code="gwp_luc_b5",
            description=("Global Warming Potential - Land Use and Land Use Change for module B5."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module B6."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (B6)"),
            field_code="gwp_luc_b6",
            description=("Global Warming Potential - Land Use and Land Use Change for module B6."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module C1."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (C1)"),
            field_code="gwp_luc_c1",
            description=("Global Warming Potential - Land Use and Land Use Change for module C1."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module C2."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (C2)"),
            field_code="gwp_luc_c2",
            description=("Global Warming Potential - Land Use and Land Use Change for module C2."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module C3."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (C3)"),
            field_code="gwp_luc_c3",
            description=("Global Warming Potential - Land Use and Land Use Change for module C3."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module C4."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (C4)"),
            field_code="gwp_luc_c4",
            description=("Global Warming Potential - Land Use and Land Use Change for module C4."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module D."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (D)"),
            field_code="gwp_luc_d",
            description=("Global Warming Potential - Land Use and Land Use Change for module D."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module D1."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (D1)"),
            field_code="gwp_luc_d1",
            description=("Global Warming Potential - Land Use and Land Use Change for module D1."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Global Warming Potential - Land Use and Land Use Change for module D2."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Global Warming Potential - Land Use and Land Use Change (D2)"),
            field_code="gwp_luc_d2",
            description=("Global Warming Potential - Land Use and Land Use Change for module D2."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    gwp_luc_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description=("Total Global Warming Potential - Land Use and Land Use Change."),
        schema_extra=openbdf_field_metadata(
            attribute_name=("Total Global Warming Potential - Land Use and Land Use Change"),
            field_code="gwp_luc_total",
            description=("Total Global Warming Potential - Land Use and Land Use Change."),
            constraint="numerical",
            units="kg CO₂ eq",
            requirements="Recommended",
        ),
    )

    odp_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (A1-A3)",
            field_code="odp_a1_a3",
            description="Ozone Depletion Potential for module A1-A3.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (A4)",
            field_code="odp_a4",
            description="Ozone Depletion Potential for module A4.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (A5)",
            field_code="odp_a5",
            description="Ozone Depletion Potential for module A5.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B1)",
            field_code="odp_b1",
            description="Ozone Depletion Potential for module B1.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B2)",
            field_code="odp_b2",
            description="Ozone Depletion Potential for module B2.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B3)",
            field_code="odp_b3",
            description="Ozone Depletion Potential for module B3.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B4)",
            field_code="odp_b4",
            description="Ozone Depletion Potential for module B4.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B5)",
            field_code="odp_b5",
            description="Ozone Depletion Potential for module B5.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (B6)",
            field_code="odp_b6",
            description="Ozone Depletion Potential for module B6.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (C1)",
            field_code="odp_c1",
            description="Ozone Depletion Potential for module C1.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (C2)",
            field_code="odp_c2",
            description="Ozone Depletion Potential for module C2.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (C3)",
            field_code="odp_c3",
            description="Ozone Depletion Potential for module C3.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (C4)",
            field_code="odp_c4",
            description="Ozone Depletion Potential for module C4.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (D)",
            field_code="odp_d",
            description="Ozone Depletion Potential for module D.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (D1)",
            field_code="odp_d1",
            description="Ozone Depletion Potential for module D1.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Ozone Depletion Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Ozone Depletion Potential (D2)",
            field_code="odp_d2",
            description="Ozone Depletion Potential for module D2.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    odp_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Ozone Depletion Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Ozone Depletion Potential",
            field_code="odp_total",
            description="Total Ozone Depletion Potential.",
            constraint="numerical",
            units="kg R11 eq / kg CFC-11 eq.",
            requirements="Optional",
        ),
    )

    ap_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (A1-A3)",
            field_code="ap_a1_a3",
            description="Acidification Potential for module A1-A3.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (A4)",
            field_code="ap_a4",
            description="Acidification Potential for module A4.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (A5)",
            field_code="ap_a5",
            description="Acidification Potential for module A5.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B1)",
            field_code="ap_b1",
            description="Acidification Potential for module B1.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B2)",
            field_code="ap_b2",
            description="Acidification Potential for module B2.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B3)",
            field_code="ap_b3",
            description="Acidification Potential for module B3.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B4)",
            field_code="ap_b4",
            description="Acidification Potential for module B4.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B5)",
            field_code="ap_b5",
            description="Acidification Potential for module B5.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (B6)",
            field_code="ap_b6",
            description="Acidification Potential for module B6.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (C1)",
            field_code="ap_c1",
            description="Acidification Potential for module C1.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (C2)",
            field_code="ap_c2",
            description="Acidification Potential for module C2.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (C3)",
            field_code="ap_c3",
            description="Acidification Potential for module C3.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (C4)",
            field_code="ap_c4",
            description="Acidification Potential for module C4.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (D)",
            field_code="ap_d",
            description="Acidification Potential for module D.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (D1)",
            field_code="ap_d1",
            description="Acidification Potential for module D1.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Acidification Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Acidification Potential (D2)",
            field_code="ap_d2",
            description="Acidification Potential for module D2.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ap_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Acidification Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Acidification Potential",
            field_code="ap_total",
            description="Total Acidification Potential.",
            constraint="numerical",
            units="kg SO₂ eq.",
            requirements="Optional",
        ),
    )

    ep_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (A1-A3)",
            field_code="ep_a1_a3",
            description="Eutrophication Potential for module A1-A3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (A4)",
            field_code="ep_a4",
            description="Eutrophication Potential for module A4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (A5)",
            field_code="ep_a5",
            description="Eutrophication Potential for module A5.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B1)",
            field_code="ep_b1",
            description="Eutrophication Potential for module B1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B2)",
            field_code="ep_b2",
            description="Eutrophication Potential for module B2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B3)",
            field_code="ep_b3",
            description="Eutrophication Potential for module B3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B4)",
            field_code="ep_b4",
            description="Eutrophication Potential for module B4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B5)",
            field_code="ep_b5",
            description="Eutrophication Potential for module B5.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (B6)",
            field_code="ep_b6",
            description="Eutrophication Potential for module B6.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (C1)",
            field_code="ep_c1",
            description="Eutrophication Potential for module C1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )

    ep_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (C2)",
            field_code="ep_c2",
            description="Eutrophication Potential for module C2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (C3)",
            field_code="ep_c3",
            description="Eutrophication Potential for module C3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (C4)",
            field_code="ep_c4",
            description="Eutrophication Potential for module C4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (D)",
            field_code="ep_d",
            description="Eutrophication Potential for module D.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (D1)",
            field_code="ep_d1",
            description="Eutrophication Potential for module D1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential (D2)",
            field_code="ep_d2",
            description="Eutrophication Potential for module D2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Eutrophication Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Eutrophication Potential",
            field_code="ep_total",
            description="Total Eutrophication Potential.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_af_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (A1-A3)",
            field_code="ep_af_a1_a3",
            description="Eutrophication Potential - Aquatic Freshwater for module A1-A3.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (A4)",
            field_code="ep_af_a4",
            description="Eutrophication Potential - Aquatic Freshwater for module A4.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (A5)",
            field_code="ep_af_a5",
            description="Eutrophication Potential - Aquatic Freshwater for module A5.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B1)",
            field_code="ep_af_b1",
            description="Eutrophication Potential - Aquatic Freshwater for module B1.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B2)",
            field_code="ep_af_b2",
            description="Eutrophication Potential - Aquatic Freshwater for module B2.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B3)",
            field_code="ep_af_b3",
            description="Eutrophication Potential - Aquatic Freshwater for module B3.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B4)",
            field_code="ep_af_b4",
            description="Eutrophication Potential - Aquatic Freshwater for module B4.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B5)",
            field_code="ep_af_b5",
            description="Eutrophication Potential - Aquatic Freshwater for module B5.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (B6)",
            field_code="ep_af_b6",
            description="Eutrophication Potential - Aquatic Freshwater for module B6.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (C1)",
            field_code="ep_af_c1",
            description="Eutrophication Potential - Aquatic Freshwater for module C1.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (C2)",
            field_code="ep_af_c2",
            description="Eutrophication Potential - Aquatic Freshwater for module C2.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (C3)",
            field_code="ep_af_c3",
            description="Eutrophication Potential - Aquatic Freshwater for module C3.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (C4)",
            field_code="ep_af_c4",
            description="Eutrophication Potential - Aquatic Freshwater for module C4.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (D)",
            field_code="ep_af_d",
            description="Eutrophication Potential - Aquatic Freshwater for module D.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (D1)",
            field_code="ep_af_d1",
            description="Eutrophication Potential - Aquatic Freshwater for module D1.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Freshwater for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Freshwater (D2)",
            field_code="ep_af_d2",
            description="Eutrophication Potential - Aquatic Freshwater for module D2.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_af_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Eutrophication Potential - Aquatic Freshwater.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Eutrophication Potential - Aquatic Freshwater",
            field_code="ep_af_total",
            description="Total Eutrophication Potential - Aquatic Freshwater.",
            constraint="numerical",
            units="kg PO4 eq",
            requirements="Optional",
        ),
    )
    ep_am_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (A1-A3)",
            field_code="ep_am_a1_a3",
            description="Eutrophication Potential - Aquatic Marine for module A1-A3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (A4)",
            field_code="ep_am_a4",
            description="Eutrophication Potential - Aquatic Marine for module A4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (A5)",
            field_code="ep_am_a5",
            description="Eutrophication Potential - Aquatic Marine for module A5.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B1)",
            field_code="ep_am_b1",
            description="Eutrophication Potential - Aquatic Marine for module B1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B2)",
            field_code="ep_am_b2",
            description="Eutrophication Potential - Aquatic Marine for module B2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B3)",
            field_code="ep_am_b3",
            description="Eutrophication Potential - Aquatic Marine for module B3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B4)",
            field_code="ep_am_b4",
            description="Eutrophication Potential - Aquatic Marine for module B4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B5)",
            field_code="ep_am_b5",
            description="Eutrophication Potential - Aquatic Marine for module B5.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (B6)",
            field_code="ep_am_b6",
            description="Eutrophication Potential - Aquatic Marine for module B6.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (C1)",
            field_code="ep_am_c1",
            description="Eutrophication Potential - Aquatic Marine for module C1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (C2)",
            field_code="ep_am_c2",
            description="Eutrophication Potential - Aquatic Marine for module C2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (C3)",
            field_code="ep_am_c3",
            description="Eutrophication Potential - Aquatic Marine for module C3.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (C4)",
            field_code="ep_am_c4",
            description="Eutrophication Potential - Aquatic Marine for module C4.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (D)",
            field_code="ep_am_d",
            description="Eutrophication Potential - Aquatic Marine for module D.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (D1)",
            field_code="ep_am_d1",
            description="Eutrophication Potential - Aquatic Marine for module D1.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Aquatic Marine for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Aquatic Marine (D2)",
            field_code="ep_am_d2",
            description="Eutrophication Potential - Aquatic Marine for module D2.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_am_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Eutrophication Potential - Aquatic Marine.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Eutrophication Potential - Aquatic Marine",
            field_code="ep_am_total",
            description="Total Eutrophication Potential - Aquatic Marine.",
            constraint="numerical",
            units="kg N eq",
            requirements="Optional",
        ),
    )
    ep_t_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (A1-A3)",
            field_code="ep_t_a1_a3",
            description="Eutrophication Potential - Terrestrial for module A1-A3.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (A4)",
            field_code="ep_t_a4",
            description="Eutrophication Potential - Terrestrial for module A4.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (A5)",
            field_code="ep_t_a5",
            description="Eutrophication Potential - Terrestrial for module A5.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B1)",
            field_code="ep_t_b1",
            description="Eutrophication Potential - Terrestrial for module B1.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B2)",
            field_code="ep_t_b2",
            description="Eutrophication Potential - Terrestrial for module B2.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B3)",
            field_code="ep_t_b3",
            description="Eutrophication Potential - Terrestrial for module B3.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B4)",
            field_code="ep_t_b4",
            description="Eutrophication Potential - Terrestrial for module B4.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B5)",
            field_code="ep_t_b5",
            description="Eutrophication Potential - Terrestrial for module B5.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (B6)",
            field_code="ep_t_b6",
            description="Eutrophication Potential - Terrestrial for module B6.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (C1)",
            field_code="ep_t_c1",
            description="Eutrophication Potential - Terrestrial for module C1.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (C2)",
            field_code="ep_t_c2",
            description="Eutrophication Potential - Terrestrial for module C2.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (C3)",
            field_code="ep_t_c3",
            description="Eutrophication Potential - Terrestrial for module C3.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (C4)",
            field_code="ep_t_c4",
            description="Eutrophication Potential - Terrestrial for module C4.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (D)",
            field_code="ep_t_d",
            description="Eutrophication Potential - Terrestrial for module D.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (D1)",
            field_code="ep_t_d1",
            description="Eutrophication Potential - Terrestrial for module D1.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Eutrophication Potential - Terrestrial for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Eutrophication Potential - Terrestrial (D2)",
            field_code="ep_t_d2",
            description="Eutrophication Potential - Terrestrial for module D2.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    ep_t_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Eutrophication Potential - Terrestrial.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Eutrophication Potential - Terrestrial",
            field_code="ep_t_total",
            description="Total Eutrophication Potential - Terrestrial.",
            constraint="numerical",
            units="mol Ne eq",
            requirements="Optional",
        ),
    )
    pocp_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A1-A3)",
            field_code="pocp_a1_a3",
            description="Photochemical Ozone Formation Potential for module A1-A3.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A4)",
            field_code="pocp_a4",
            description="Photochemical Ozone Formation Potential for module A4.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A5)",
            field_code="pocp_a5",
            description="Photochemical Ozone Formation Potential for module A5.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B1)",
            field_code="pocp_b1",
            description="Photochemical Ozone Formation Potential for module B1.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B2)",
            field_code="pocp_b2",
            description="Photochemical Ozone Formation Potential for module B2.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B3)",
            field_code="pocp_b3",
            description="Photochemical Ozone Formation Potential for module B3.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B4)",
            field_code="pocp_b4",
            description="Photochemical Ozone Formation Potential for module B4.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B5)",
            field_code="pocp_b5",
            description="Photochemical Ozone Formation Potential for module B5.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B6)",
            field_code="pocp_b6",
            description="Photochemical Ozone Formation Potential for module B6.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C1)",
            field_code="pocp_c1",
            description="Photochemical Ozone Formation Potential for module C1.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C2)",
            field_code="pocp_c2",
            description="Photochemical Ozone Formation Potential for module C2.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C3)",
            field_code="pocp_c3",
            description="Photochemical Ozone Formation Potential for module C3.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C4)",
            field_code="pocp_c4",
            description="Photochemical Ozone Formation Potential for module C4.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D)",
            field_code="pocp_d",
            description="Photochemical Ozone Formation Potential for module D.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D1)",
            field_code="pocp_d1",
            description="Photochemical Ozone Formation Potential for module D1.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D2)",
            field_code="pocp_d2",
            description="Photochemical Ozone Formation Potential for module D2.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    pocp_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Photochemical Ozone Formation Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Photochemical Ozone Formation Potential",
            field_code="pocp_total",
            description="Total Photochemical Ozone Formation Potential.",
            constraint="numerical",
            units="kg C2H4 eq",
            requirements="Optional",
        ),
    )
    sfp_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (A1-A3)",
            field_code="sfp_a1_a3",
            description="Smog Forming Potential for module A1-A3.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (A4)",
            field_code="sfp_a4",
            description="Smog Forming Potential for module A4.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (A5)",
            field_code="sfp_a5",
            description="Smog Forming Potential for module A5.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B1)",
            field_code="sfp_b1",
            description="Smog Forming Potential for module B1.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B2)",
            field_code="sfp_b2",
            description="Smog Forming Potential for module B2.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B3)",
            field_code="sfp_b3",
            description="Smog Forming Potential for module B3.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B4)",
            field_code="sfp_b4",
            description="Smog Forming Potential for module B4.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B5)",
            field_code="sfp_b5",
            description="Smog Forming Potential for module B5.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (B6)",
            field_code="sfp_b6",
            description="Smog Forming Potential for module B6.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (C1)",
            field_code="sfp_c1",
            description="Smog Forming Potential for module C1.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (C2)",
            field_code="sfp_c2",
            description="Smog Forming Potential for module C2.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (C3)",
            field_code="sfp_c3",
            description="Smog Forming Potential for module C3.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (C4)",
            field_code="sfp_c4",
            description="Smog Forming Potential for module C4.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (D)",
            field_code="sfp_d",
            description="Smog Forming Potential for module D.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (D1)",
            field_code="sfp_d1",
            description="Smog Forming Potential for module D1.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Smog Forming Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Smog Forming Potential (D2)",
            field_code="sfp_d2",
            description="Smog Forming Potential for module D2.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    sfp_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Smog Forming Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Smog Forming Potential",
            field_code="sfp_total",
            description="Total Smog Forming Potential.",
            constraint="numerical",
            units="kg O3 eq",
            requirements="Optional",
        ),
    )
    pofp_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A1-A3)",
            field_code="pofp_a1_a3",
            description="Photochemical Ozone Formation Potential for module A1-A3.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A4)",
            field_code="pofp_a4",
            description="Photochemical Ozone Formation Potential for module A4.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (A5)",
            field_code="pofp_a5",
            description="Photochemical Ozone Formation Potential for module A5.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B1)",
            field_code="pofp_b1",
            description="Photochemical Ozone Formation Potential for module B1.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B2)",
            field_code="pofp_b2",
            description="Photochemical Ozone Formation Potential for module B2.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B3)",
            field_code="pofp_b3",
            description="Photochemical Ozone Formation Potential for module B3.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B4)",
            field_code="pofp_b4",
            description="Photochemical Ozone Formation Potential for module B4.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B5)",
            field_code="pofp_b5",
            description="Photochemical Ozone Formation Potential for module B5.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (B6)",
            field_code="pofp_b6",
            description="Photochemical Ozone Formation Potential for module B6.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C1)",
            field_code="pofp_c1",
            description="Photochemical Ozone Formation Potential for module C1.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C2)",
            field_code="pofp_c2",
            description="Photochemical Ozone Formation Potential for module C2.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C3)",
            field_code="pofp_c3",
            description="Photochemical Ozone Formation Potential for module C3.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (C4)",
            field_code="pofp_c4",
            description="Photochemical Ozone Formation Potential for module C4.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D)",
            field_code="pofp_d",
            description="Photochemical Ozone Formation Potential for module D.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D1)",
            field_code="pofp_d1",
            description="Photochemical Ozone Formation Potential for module D1.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Photochemical Ozone Formation Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Photochemical Ozone Formation Potential (D2)",
            field_code="pofp_d2",
            description="Photochemical Ozone Formation Potential for module D2.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    pofp_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Photochemical Ozone Formation Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Photochemical Ozone Formation Potential",
            field_code="pofp_total",
            description="Total Photochemical Ozone Formation Potential.",
            constraint="numerical",
            units="kg NMVOC eq",
            requirements="Optional",
        ),
    )
    adpmm_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (A1-A3)",
            field_code="adpmm_a1_a3",
            description="Abiotic Depletion Potential (Minerals and Metals) for module A1-A3.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )
    adpmm_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (A4)",
            field_code="adpmm_a4",
            description="Abiotic Depletion Potential (Minerals and Metals) for module A4.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )
    adpmm_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (A5)",
            field_code="adpmm_a5",
            description="Abiotic Depletion Potential (Minerals and Metals) for module A5.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )
    adpmm_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B1)",
            field_code="adpmm_b1",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B1.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B2)",
            field_code="adpmm_b2",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B2.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B3)",
            field_code="adpmm_b3",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B3.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B4)",
            field_code="adpmm_b4",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B4.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B5)",
            field_code="adpmm_b5",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B5.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (B6)",
            field_code="adpmm_b6",
            description="Abiotic Depletion Potential (Minerals and Metals) for module B6.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (C1)",
            field_code="adpmm_c1",
            description="Abiotic Depletion Potential (Minerals and Metals) for module C1.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (C2)",
            field_code="adpmm_c2",
            description="Abiotic Depletion Potential (Minerals and Metals) for module C2.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (C3)",
            field_code="adpmm_c3",
            description="Abiotic Depletion Potential (Minerals and Metals) for module C3.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (C4)",
            field_code="adpmm_c4",
            description="Abiotic Depletion Potential (Minerals and Metals) for module C4.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (D)",
            field_code="adpmm_d",
            description="Abiotic Depletion Potential (Minerals and Metals) for module D.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (D1)",
            field_code="adpmm_d1",
            description="Abiotic Depletion Potential (Minerals and Metals) for module D1.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Minerals and Metals) for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Minerals and Metals) (D2)",
            field_code="adpmm_d2",
            description="Abiotic Depletion Potential (Minerals and Metals) for module D2.",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpmm_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Abiotic Depletion Potential (Minerals and Metals).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Abiotic Depletion Potential (Minerals and Metals)",
            field_code="adpmm_total",
            description="Total Abiotic Depletion Potential (Minerals and Metals).",
            constraint="numerical",
            units="kg Sb eq",
            requirements="Optional",
        ),
    )

    adpf_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (A1-A3)",
            field_code="adpf_a1_a3",
            description="Abiotic Depletion Potential (Fossil Fuels) for module A1-A3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (A4)",
            field_code="adpf_a4",
            description="Abiotic Depletion Potential (Fossil Fuels) for module A4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (A5)",
            field_code="adpf_a5",
            description="Abiotic Depletion Potential (Fossil Fuels) for module A5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B1)",
            field_code="adpf_b1",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B2)",
            field_code="adpf_b2",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B3)",
            field_code="adpf_b3",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B4)",
            field_code="adpf_b4",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B5)",
            field_code="adpf_b5",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (B6)",
            field_code="adpf_b6",
            description="Abiotic Depletion Potential (Fossil Fuels) for module B6.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (C1)",
            field_code="adpf_c1",
            description="Abiotic Depletion Potential (Fossil Fuels) for module C1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (C2)",
            field_code="adpf_c2",
            description="Abiotic Depletion Potential (Fossil Fuels) for module C2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (C3)",
            field_code="adpf_c3",
            description="Abiotic Depletion Potential (Fossil Fuels) for module C3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (C4)",
            field_code="adpf_c4",
            description="Abiotic Depletion Potential (Fossil Fuels) for module C4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (D)",
            field_code="adpf_d",
            description="Abiotic Depletion Potential (Fossil Fuels) for module D.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (D1)",
            field_code="adpf_d1",
            description="Abiotic Depletion Potential (Fossil Fuels) for module D1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Abiotic Depletion Potential (Fossil Fuels) for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Abiotic Depletion Potential (Fossil Fuels) (D2)",
            field_code="adpf_d2",
            description="Abiotic Depletion Potential (Fossil Fuels) for module D2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    adpf_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Abiotic Depletion Potential (Fossil Fuels).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Abiotic Depletion Potential (Fossil Fuels)",
            field_code="adpf_total",
            description="Total Abiotic Depletion Potential (Fossil Fuels).",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    wdp_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (A1-A3)",
            field_code="wdp_a1_a3",
            description="Water Depletion Potential for module A1-A3.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (A4)",
            field_code="wdp_a4",
            description="Water Depletion Potential for module A4.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (A5)",
            field_code="wdp_a5",
            description="Water Depletion Potential for module A5.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B1)",
            field_code="wdp_b1",
            description="Water Depletion Potential for module B1.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B2)",
            field_code="wdp_b2",
            description="Water Depletion Potential for module B2.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B3)",
            field_code="wdp_b3",
            description="Water Depletion Potential for module B3.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B4)",
            field_code="wdp_b4",
            description="Water Depletion Potential for module B4.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B5)",
            field_code="wdp_b5",
            description="Water Depletion Potential for module B5.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (B6)",
            field_code="wdp_b6",
            description="Water Depletion Potential for module B6.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (C1)",
            field_code="wdp_c1",
            description="Water Depletion Potential for module C1.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (C2)",
            field_code="wdp_c2",
            description="Water Depletion Potential for module C2.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (C3)",
            field_code="wdp_c3",
            description="Water Depletion Potential for module C3.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (C4)",
            field_code="wdp_c4",
            description="Water Depletion Potential for module C4.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (D)",
            field_code="wdp_d",
            description="Water Depletion Potential for module D.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (D1)",
            field_code="wdp_d1",
            description="Water Depletion Potential for module D1.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Water Depletion Potential for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Water Depletion Potential (D2)",
            field_code="wdp_d2",
            description="Water Depletion Potential for module D2.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    wdp_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Water Depletion Potential.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Water Depletion Potential",
            field_code="wdp_total",
            description="Total Water Depletion Potential.",
            constraint="numerical",
            units="m3 world eq",
            requirements="Optional",
        ),
    )

    pere_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (A1-A3)",
            field_code="pere_a1_a3",
            description="Primary Energy Renewable (Energy resources) for module A1-A3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (A4)",
            field_code="pere_a4",
            description="Primary Energy Renewable (Energy resources) for module A4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (A5)",
            field_code="pere_a5",
            description="Primary Energy Renewable (Energy resources) for module A5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B1)",
            field_code="pere_b1",
            description="Primary Energy Renewable (Energy resources) for module B1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B2)",
            field_code="pere_b2",
            description="Primary Energy Renewable (Energy resources) for module B2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B3)",
            field_code="pere_b3",
            description="Primary Energy Renewable (Energy resources) for module B3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B4)",
            field_code="pere_b4",
            description="Primary Energy Renewable (Energy resources) for module B4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B5)",
            field_code="pere_b5",
            description="Primary Energy Renewable (Energy resources) for module B5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (B6)",
            field_code="pere_b6",
            description="Primary Energy Renewable (Energy resources) for module B6.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (C1)",
            field_code="pere_c1",
            description="Primary Energy Renewable (Energy resources) for module C1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (C2)",
            field_code="pere_c2",
            description="Primary Energy Renewable (Energy resources) for module C2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (C3)",
            field_code="pere_c3",
            description="Primary Energy Renewable (Energy resources) for module C3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (C4)",
            field_code="pere_c4",
            description="Primary Energy Renewable (Energy resources) for module C4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (D)",
            field_code="pere_d",
            description="Primary Energy Renewable (Energy resources) for module D.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (D1)",
            field_code="pere_d1",
            description="Primary Energy Renewable (Energy resources) for module D1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable (Energy resources) for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable (Energy resources) (D2)",
            field_code="pere_d2",
            description="Primary Energy Renewable (Energy resources) for module D2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pere_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Primary Energy Renewable (Energy resources).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Primary Energy Renewable (Energy resources)",
            field_code="pere_total",
            description="Total Primary Energy Renewable (Energy resources).",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (A1-A3)",
            field_code="penre_a1_a3",
            description="Primary Energy Non-Renewable (Energy resources) for module A1-A3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (A4)",
            field_code="penre_a4",
            description="Primary Energy Non-Renewable (Energy resources) for module A4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (A5)",
            field_code="penre_a5",
            description="Primary Energy Non-Renewable (Energy resources) for module A5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B1)",
            field_code="penre_b1",
            description="Primary Energy Non-Renewable (Energy resources) for module B1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B2)",
            field_code="penre_b2",
            description="Primary Energy Non-Renewable (Energy resources) for module B2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B3)",
            field_code="penre_b3",
            description="Primary Energy Non-Renewable (Energy resources) for module B3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B4)",
            field_code="penre_b4",
            description="Primary Energy Non-Renewable (Energy resources) for module B4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B5)",
            field_code="penre_b5",
            description="Primary Energy Non-Renewable (Energy resources) for module B5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (B6)",
            field_code="penre_b6",
            description="Primary Energy Non-Renewable (Energy resources) for module B6.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (C1)",
            field_code="penre_c1",
            description="Primary Energy Non-Renewable (Energy resources) for module C1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (C2)",
            field_code="penre_c2",
            description="Primary Energy Non-Renewable (Energy resources) for module C2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (C3)",
            field_code="penre_c3",
            description="Primary Energy Non-Renewable (Energy resources) for module C3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (C4)",
            field_code="penre_c4",
            description="Primary Energy Non-Renewable (Energy resources) for module C4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (D)",
            field_code="penre_d",
            description="Primary Energy Non-Renewable (Energy resources) for module D.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (D1)",
            field_code="penre_d1",
            description="Primary Energy Non-Renewable (Energy resources) for module D1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable (Energy resources) for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable (Energy resources) (D2)",
            field_code="penre_d2",
            description="Primary Energy Non-Renewable (Energy resources) for module D2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penre_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Primary Energy Non-Renewable (Energy resources).",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Primary Energy Non-Renewable (Energy resources)",
            field_code="penre_total",
            description="Total Primary Energy Non-Renewable (Energy resources).",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (A1-A3)",
            field_code="pert_a1_a3",
            description="Primary Energy Renewable Total for module A1-A3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (A4)",
            field_code="pert_a4",
            description="Primary Energy Renewable Total for module A4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (A5)",
            field_code="pert_a5",
            description="Primary Energy Renewable Total for module A5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B1)",
            field_code="pert_b1",
            description="Primary Energy Renewable Total for module B1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B2)",
            field_code="pert_b2",
            description="Primary Energy Renewable Total for module B2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B3)",
            field_code="pert_b3",
            description="Primary Energy Renewable Total for module B3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B4)",
            field_code="pert_b4",
            description="Primary Energy Renewable Total for module B4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B5)",
            field_code="pert_b5",
            description="Primary Energy Renewable Total for module B5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (B6)",
            field_code="pert_b6",
            description="Primary Energy Renewable Total for module B6.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (C1)",
            field_code="pert_c1",
            description="Primary Energy Renewable Total for module C1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (C2)",
            field_code="pert_c2",
            description="Primary Energy Renewable Total for module C2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (C3)",
            field_code="pert_c3",
            description="Primary Energy Renewable Total for module C3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (C4)",
            field_code="pert_c4",
            description="Primary Energy Renewable Total for module C4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (D)",
            field_code="pert_d",
            description="Primary Energy Renewable Total for module D.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (D1)",
            field_code="pert_d1",
            description="Primary Energy Renewable Total for module D1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Renewable Total for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Renewable Total (D2)",
            field_code="pert_d2",
            description="Primary Energy Renewable Total for module D2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    pert_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Primary Energy Renewable Total.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Primary Energy Renewable Total",
            field_code="pert_total",
            description="Total Primary Energy Renewable Total.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_a1_a3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module A1-A3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (A1-A3)",
            field_code="penrt_a1_a3",
            description="Primary Energy Non-Renewable Total for module A1-A3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_a4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module A4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (A4)",
            field_code="penrt_a4",
            description="Primary Energy Non-Renewable Total for module A4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_a5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module A5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (A5)",
            field_code="penrt_a5",
            description="Primary Energy Non-Renewable Total for module A5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B1)",
            field_code="penrt_b1",
            description="Primary Energy Non-Renewable Total for module B1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B2)",
            field_code="penrt_b2",
            description="Primary Energy Non-Renewable Total for module B2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B3)",
            field_code="penrt_b3",
            description="Primary Energy Non-Renewable Total for module B3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B4)",
            field_code="penrt_b4",
            description="Primary Energy Non-Renewable Total for module B4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b5: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B5.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B5)",
            field_code="penrt_b5",
            description="Primary Energy Non-Renewable Total for module B5.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_b6: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module B6.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (B6)",
            field_code="penrt_b6",
            description="Primary Energy Non-Renewable Total for module B6.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_c1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module C1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (C1)",
            field_code="penrt_c1",
            description="Primary Energy Non-Renewable Total for module C1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_c2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module C2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (C2)",
            field_code="penrt_c2",
            description="Primary Energy Non-Renewable Total for module C2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_c3: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module C3.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (C3)",
            field_code="penrt_c3",
            description="Primary Energy Non-Renewable Total for module C3.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_c4: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module C4.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (C4)",
            field_code="penrt_c4",
            description="Primary Energy Non-Renewable Total for module C4.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_d: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module D.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (D)",
            field_code="penrt_d",
            description="Primary Energy Non-Renewable Total for module D.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_d1: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module D1.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (D1)",
            field_code="penrt_d1",
            description="Primary Energy Non-Renewable Total for module D1.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_d2: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Primary Energy Non-Renewable Total for module D2.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Primary Energy Non-Renewable Total (D2)",
            field_code="penrt_d2",
            description="Primary Energy Non-Renewable Total for module D2.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )

    penrt_total: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric, nullable=True),
        description="Total Primary Energy Non-Renewable Total.",
        schema_extra=openbdf_field_metadata(
            attribute_name="Total Primary Energy Non-Renewable Total",
            field_code="penrt_total",
            description="Total Primary Energy Non-Renewable Total.",
            constraint="numerical",
            units="MJ",
            requirements="Optional",
        ),
    )
