import logging
import uuid

from koza.cli_runner import get_koza_app

from biolink.pydanticmodel import GeneToPhenotypicFeatureAssociation

LOG = logging.getLogger(__name__)

koza_app = get_koza_app("zfin_gene_to_phenotype")

row = koza_app.get_row()
eqe2zp = koza_app.get_map("eqe2zp")

if row["Phenotype Tag"] == "abnormal":
    zp_key_elements = [
        row["Affected Structure or Process 1 subterm ID"],
        row["Post-composed Relationship ID"],
        row["Affected Structure or Process 1 superterm ID"],
        row["Phenotype Keyword ID"],
        row["Affected Structure or Process 2 subterm ID"],
        row["Post-composed Relationship (rel) ID"],
        row["Affected Structure or Process 2 superterm ID"],
    ]

    zp_key = "-".join([element or "0" for element in zp_key_elements])

    zp_term = eqe2zp[zp_key]["iri"]

    if not zp_term:
        LOG.debug("ZP concatenation " + zp_key + " did not match a ZP term")
    else:

        gene_id = "ZFIN:" + row["Gene ID"]

        association = GeneToPhenotypicFeatureAssociation(
            id="uuid:" + str(uuid.uuid1()),
            subject=gene_id,
            predicate="biolink:has_phenotype",
            object=zp_term,
            publications=["ZFIN:" + row["Publication ID"]],
            aggregator_knowledge_source=["infores:monarchinitiative"],
            primary_knowledge_source="infores:zfin"
        )

        koza_app.write(association)
