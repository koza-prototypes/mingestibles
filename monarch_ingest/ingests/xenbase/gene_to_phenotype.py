import uuid

from koza.cli_runner import get_koza_app

from biolink.pydanticmodel import (
    Gene,
    GeneToPhenotypicFeatureAssociation,
    PhenotypicFeature
)

koza_app = get_koza_app("xenbase_gene_to_phenotype")

while (row := koza_app.get_row()) is not None:

    # Not including qualifiers, as none are present in the input file. If they show up,
    # we'll want to examine the values before including them in the output of this transform
    if row["QUALIFIER"]:
        raise ValueError("Didn't expect a qualifier value, found: " + row["QUALIFIER"])

    gene = Gene(id=row["SUBJECT"], provided_by=["infores:xenbase"])

    phenotype = PhenotypicFeature(id=row["OBJECT"], provided_by=["infores:xenbase"])

    # relation = row["RELATION"].replace("_", ":"),
    association = GeneToPhenotypicFeatureAssociation(
        id="uuid:" + str(uuid.uuid1()),
        subject=gene.id,
        predicate="biolink:has_phenotype",
        object=phenotype.id,
        publications=[row["SOURCE"]],
        aggregator_knowledge_source=["infores:monarchinitiative"],
        primary_knowledge_source="infores:xenbase"
    )

    if row["SOURCE"]:
        association.publications = [row["SOURCE"]]

    koza_app.write(association)
