import matplotlib.pyplot as plt
from scholarly import scholarly
from datetime import datetime
import pandas as pd

# CONFIG
AUTHOR_ID = "Mt24kfgAAAAJ"
OUT_MD = "../_includes/publication_stats.md"
OUT_PLOT = "../images/citations_by_year.png"

# GET AUTHOR DATA
author = scholarly.search_author_id(AUTHOR_ID, filled=True)

# GET VALUES
n_papers = len(author['publications'])
first_author_count = sum(1 for pub in author['publications']
                         if 'Baptiste Vandecrux' in pub['bib'].get('author', '').split(',')[0])
total_citations = author.get('citedby', 0)

# CITATIONS BY YEAR
citations_by_year = author.get('citedby_year', {})
if not citations_by_year:
    citations_by_year = {
        2018: 30,
        2019: 49,
        2020: 107,
        2021: 170,
        2022: 212,
        2023: 217,
        2024: 244
    }
    total_citations = author.get('citedby', 0)
    known_sum = sum(citations_by_year.values())
    citations_by_year[2025] = total_citations - known_sum

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

n_papers = 28
first_author_count = 8
# WRITE MARKDOWN
with open(OUT_MD, "w") as f:
    f.write('<div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; background: #f9f9f9; margin-bottom: 2em;">\n')
    f.write('<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1em;">\n')
    f.write('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png" alt="Google Scholar" width="32" height="32" />\n')
    f.write('<a href="https://scholar.google.dk/citations?user=Mt24kfgAAAAJ" target="_blank"><strong>View my Google Scholar profile</strong></a>\n')
    f.write('</div>\n')
    f.write(f"<strong>Total publications:</strong> {n_papers}<br/>\n")
    f.write(f"<strong>First author publications:</strong> {first_author_count}<br/>\n")
    f.write(f"<strong>Total citations:</strong> {total_citations}<br/>\n")
    f.write(f'<img src="/images/citations_by_year.png" alt="Citation barplot" style="width: 150px; height: 190px; margin-top: 1em;" />\n')
    f.write('</div>\n')