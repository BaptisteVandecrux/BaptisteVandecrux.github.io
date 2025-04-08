import requests

# output_file = "my_datasets.bib"
# dois = [
#     "10.22008/FK2/VVXGUT",
#     "10.22008/FK2/IW73UU",
#     "10.22008/FK2/SR3O4F",
#     "10.22008/FK2/CQSKLK",
#     "10.22008/FK2/QDND53",
#     "10.22008/FK2/FBIFOX",
#     "10.22008/FK2/OIAJVO",
#     "10.22008/FK2/C24WVN",
#     "10.22008/FK2/9QEOWZ",
#     "10.18739/A2M61BR5M"
# ]
output_file = "my_pubs.bib"
dois = [
    "10.5194/egusphere-2024-2563",
    "10.5194/tc-18-609-2024",
    "10.5194/tc-18-2455-2024",
    "10.5194/essd-15-5467-2023",
    "10.21105/joss.05298",
    "10.1038/s41598-023-33225-9",
    "10.3390/rs15010077",
    "10.1038/s41467-022-34049-3",
    "10.5194/essd-14-955-2022",
    "10.3390/rs14040932",
    "10.5194/tc-14-3785-2020",
    "10.1029/2021JF006295",
    "10.5194/tc-15-4315-2021",
    "10.1029/2021GL092942",
    "10.5194/essd-13-3819-2021",
    "10.3389/feart.2021.578978",
    "10.5194/tc-14-3785-2020",
    "10.1017/jog.2020.30",
    "10.3390/rs12020234",
    "10.1038/s41586-019-1550-3",
    "10.3390/rs11192280",
    "10.5194/tc-14-385-2020",
    "10.5194/tc-13-845-2019",
    "10.1029/2017JF004597",
    "10.3389/feart.2018.00051",
    "10.3390/rs9111144",
    "10.3389/feart.2016.00110"
]



def doi_to_bibtex(doi):
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"❌ Failed: {doi} (status {response.status_code})")
        return None

# 📄 Output BibTeX file

with open(output_file, "w", encoding="utf-8") as f:
    for doi in dois:
        bib = doi_to_bibtex(doi)
        if bib:
            f.write(bib.strip() + "\n\n")

print(f"✅ BibTeX entries saved to: {output_file}")
