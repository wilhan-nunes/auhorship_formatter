import pandas as pd
import streamlit as st


# Function to format authors and affiliations
def format_authors_affiliations(df):
    authors = []
    affiliations_dict = {}
    affiliation_counter = 1

    for _, row in df.iterrows():
        full_name = f"{row['First Name']} {row['Middle Name'] if pd.notna(row['Middle Name']) else ''} {row['Surname']}".strip()
        affiliations = [row[f'Affiliation{i}'] for i in range(1, 5) if pd.notna(row[f'Affiliation{i}'])]

        affiliation_indices = []
        for affiliation in affiliations:
            if affiliation not in affiliations_dict:
                affiliations_dict[affiliation] = affiliation_counter
                affiliation_counter += 1
            affiliation_indices.append(affiliations_dict[affiliation])

        authors.append(f"{full_name}<sup>{','.join(map(str, affiliation_indices))}</sup>")

    affiliation_list = [f"{num}. {aff}" for aff, num in sorted(affiliations_dict.items(), key=lambda item: item[1])]

    return authors, affiliation_list


# Function to create HTML content
def create_html_authors_file(authors, affiliations):
    html_content = """
    <html>
    <head>
        <title>Authors and Affiliations</title>
        <style>
            sup {{
                font-size: smaller;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <h2>Authors</h2>
        <p>{authors_list}</p>
        <h2>Affiliations</h2>
        <ul>
        {affiliations_list}
        </ul>
    </body>
    </html>
    """
    authors_list = ', '.join([author for author in authors])
    # authors_list = ', '.join([f"{author[:-1]}<sup>{author[-1]}</sup>" for author in authors])
    affiliations_list = ''.join([f"<li><sup>{i.split('.')[0]}</sup> {i.split('.')[1]}</li>" for i in affiliations])
    html_content = html_content.format(authors_list=authors_list, affiliations_list=affiliations_list)
    return html_content

column_names = ['Order', 'First Name', 'Middle Name', 'Surname', 'Affiliation1', 'Affiliation2']
df = pd.DataFrame(columns=column_names)

st.title("Authors and Affiliations Formatter")
st.write('The TSV should contain the following headers. Add as much affiliations as you need, numbering them sequentially.')
st.table(df)

uploaded_file = st.file_uploader("Choose a TSV file with author details", type="tsv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep='\t')
    authors_list, affiliations_list = format_authors_affiliations(df)

    if st.button('Generate HTML'):
        html_content = create_html_authors_file(authors_list, affiliations_list)

        st.markdown("### Output:")
        st.markdown(html_content, unsafe_allow_html=True)
