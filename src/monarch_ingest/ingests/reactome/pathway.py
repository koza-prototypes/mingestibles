from biolink.pydanticmodel import Pathway
from koza.cli_runner import get_koza_app

koza_app = get_koza_app('reactome_pathway')

while (row := koza_app.get_row()) is not None:

    species = row['species']

    try:
        taxon_id = koza_app.translation_table.local_table[species]
    except KeyError:
        # Move on if the taxon name isn't in the translation table
        continue

    # We only continue of the species is in our local reactome_id_mapping table
    if taxon_id:
        pathway = Pathway(
            id="REACT:" + row["ID"],
            name=row["Name"],
            in_taxon=[taxon_id],
            provided_by=["infores:reactome"]
        )

        koza_app.write(pathway)
