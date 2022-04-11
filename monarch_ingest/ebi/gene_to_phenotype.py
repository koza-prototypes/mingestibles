from biolink_model_pydantic.model import Gene
from koza.cli_runner import koza_app

# You've got 'NCBI_Gene:' and you want 'NCBIGene:'? clean it up.
curie_cleaner = koza_app.curie_cleaner

# The source name is used for reading and writing
source_name = "gene-information"

# inject a single row from the source
row = koza_app.get_row(source_name)
# create your entities
gene = Gene(
    id='somethingbase:'+row['ID'],
    name=row['Name']
)

# populate any additional optional properties
if row['xrefs']:
    gene.xrefs = [curie_cleaner.clean(xref) for xref in row['xrefs']]

# remember to supply the source name as the first argument, followed by entities
koza_app.write(gene)
