import pytest
from biolink_model_pydantic.model import (
    Gene,
    GeneToPhenotypicFeatureAssociation,
    PhenotypicFeature,
)


@pytest.fixture
def entities(mock_koza,):
    row = iter(
        [
            {
                "SUBJECT": "XB-GENE-1000632",
                "SUBJECT_LABEL": "dctn2",
                "SUBJECT_TAXON": "NCBITaxon:8364",
                "SUBJECT_TAXON_LABEL": "Xla",
                "OBJECT": "XPO:0102358",
                "OBJECT_LABEL": "abnormal tail morphology",
                "RELATION": "RO_0002200",
                "RELATION_LABEL": "has_phenotype",
                "EVIDENCE": "",
                "EVIDENCE_LABEL": "",
                "SOURCE": "PMID:17112317",
                "IS_DEFINED_BY": "",
                "QUALIFIER": "",
            }
        ]
    )
    return mock_koza(
        "gene-to-phenotype", row, "./monarch_ingest/xenbase/gene2phenotype.py"
    )


def test_gene2_phenotype_transform(entities):
    assert entities
    assert len(entities) == 3
    genes = [entity for entity in entities if isinstance(entity, Gene)]
    phenotypes = [
        entity for entity in entities if isinstance(entity, PhenotypicFeature)
    ]
    associations = [
        entity
        for entity in entities
        if isinstance(entity, GeneToPhenotypicFeatureAssociation)
    ]
    assert len(genes) == 1
    assert len(phenotypes) == 1
    assert len(associations) == 1


# TODO: can this test be shared across all g2p loads?
@pytest.mark.parametrize(
    "cls", [Gene, PhenotypicFeature, GeneToPhenotypicFeatureAssociation]
)
def confirm_one_of_each_classes(cls, entities):
    class_entities = [entity for entity in entities if isinstance(entity, cls)]
    assert class_entities
    assert len(class_entities) == 1
    assert class_entities[0]


def test_gene2_phenotype_transform_publications(entities):
    associations = [
        entity
        for entity in entities
        if isinstance(entity, GeneToPhenotypicFeatureAssociation)
    ]
    assert associations[0].publications[0] == "PMID:17112317"
