import matplotlib.pyplot as plt
from scholarly import scholarly
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# CONFIG
AUTHOR_ID = "Mt24kfgAAAAJ"
OUT_MD = "../_includes/publication_stats.md"
OUT_PLOT_HTML = "../_includes/citations_plot.html"

# GET AUTHOR DATA
author = scholarly.search_author_id(AUTHOR_ID, filled=True)
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
        2024: 244,
        2025: 96
    }
    # known_sum = sum(citations_by_year.values())
    # citations_by_year[2025] = max(0, total_citations - known_sum)

df = pd.Series(citations_by_year).sort_index()

# Plotly figure
fig = go.Figure(data=[go.Bar(x=df.index, y=df.values, marker_color='gray')])
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Citations",
    height=180,
    width=400,
    margin=dict(l=40, r=20, t=10, b=40)
)

# Save interactive plot as snippet
pio.write_html(fig, file=OUT_PLOT_HTML, full_html=False, include_plotlyjs='cdn')

# Publication stats (manual fallback if parsing fails)
n_papers = 22
first_author_count = 8

# WRITE MARKDOWN BOX
with open(OUT_MD, "w") as f:
    f.write('<div style="border: 1px solid #ccc; border-radius: 6px; padding: 12px 16px; background: #f9f9f9; max-width: 560px; margin: 0 auto 2em;">\n')
    f.write('<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5em;">\n')
    f.write('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png" alt="Google Scholar" width="28" height="28" />\n')
    f.write('<a href="https://scholar.google.dk/citations?user=Mt24kfgAAAAJ" target="_blank"><strong>View my Google Scholar profile</strong></a>\n')
    f.write('</div>\n')
    f.write(f"<strong>Total publications:</strong> {n_papers}<br/>\n")
    f.write(f"<strong>First author publications:</strong> {first_author_count}<br/>\n")
    f.write(f"<strong>Total citations:</strong> {total_citations}<br/>\n")
    f.write('{% include citations_plot.html %}\n')
    f.write('</div>\n')
