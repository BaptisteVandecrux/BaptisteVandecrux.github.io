import matplotlib.pyplot as plt
from scholarly import scholarly
from datetime import datetime
import pandas as pd

# CONFIG
SCHOLAR_NAME = "Baptiste Vandecrux"  # adapt if needed
OUT_MD = "_includes/publication_stats.md"
OUT_PLOT = "assets/img/citations_by_year.png"

# GET AUTHOR DATA
author = scholarly.search_author(SCHOLAR_NAME)
author = scholarly.fill(author)

# GET VALUES
n_papers = len(author['publications'])
first_author_count = sum(1 for pub in author['publications']
                         if pub['bib']['author'].startswith(SCHOLAR_NAME.split()[0]))
total_citations = author['citedby']

# CITATIONS BY YEAR
citations_by_year = author.get('citedby_year', {})
df = pd.Series(citations_by_year).sort_index()

# PLOT
plt.figure(figsize=(6, 4))
df.plot(kind='bar', color='gray')
plt.title("Citations by year")
plt.xlabel("Year")
plt.ylabel("Citations")
plt.tight_layout()
plt.savefig(OUT_PLOT, dpi=150)
plt.close()

# WRITE MARKDOWN
with open(OUT_MD, "w") as f:
    f.write(f"**Total publications:** {n_papers}  \n")
    f.write(f"**First author publications:** {first_author_count}  \n")
    f.write(f"**Total citations:** {total_citations}  \n")
    f.write(f"![Citation barplot](/assets/img/citations_by_year.png)\n")
