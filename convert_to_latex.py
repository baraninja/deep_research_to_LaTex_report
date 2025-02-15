import re
import sys

def normalize_url(url):
    # Tar bort alla whitespace-tecken och newline, konverterar till gemener
    return re.sub(r'\s+', '', url).lower()

# Hämta rapportens titel från kommandoraden (standard om inget anges)
if len(sys.argv) > 1:
    report_title = " ".join(sys.argv[1:])
else:
    report_title = "Rapportens titel"

# Läs in markdown-texten från filen "rapport.md"
with open("rapport.md", "r", encoding="utf-8") as f:
    input_text = f.read()

def convert_to_latex(text):
    """
    Konverterar Markdown-text till LaTeX-format inklusive rubriker, listor, specialtecken och tabeller.
    """

    # 1. Ta bort fetstil (**text**) och kursiv (*text*)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Fetstil
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Kursiv

    # 2. Ta bort alla markdown-länkar
    text = re.sub(r'\[\[.*?\]\(.*?\)\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text, flags=re.DOTALL)

    # 3. Ta bort eventuella tomma parenteser
    text = re.sub(r'\(\s*\)', '', text)

    # 4. Ersätt narrow no-break space (U+202F) med ett vanligt mellanslag
    text = text.replace("\u202F", " ")

    # 5. Omvandla rubriker: rader som börjar med ett eller flera "#" blir LaTeX-rubriker
    def heading_repl(match):
        hashes = match.group(1)
        title = match.group(2).strip()
        level = len(hashes)

        # Alla rubriker blir icke-numrerade (* används för att ta bort numrering)
        if level == 1:
            return "\\chapter*{" + title + "}"
        elif level == 2:
            return "\\section*{" + title + "}"
        elif level == 3:
            return "\\subsection*{" + title + "}"
        else:
            return "\\subsubsection*{" + title + "}"

    text = re.sub(r'^(#{1,})\s*(.+)', heading_repl, text, flags=re.MULTILINE)

    # 6. Omvandla listor som börjar med "- " till LaTeX-underrubriker
    text = re.sub(r'^\s*-\s*(.+?):\s*(.*)', r'\\subsection*{\1}\n\2', text, flags=re.MULTILINE)

    # 7. Ersätt specialtecken som kan orsaka problem i LaTeX
    special_chars = {
        "%": "\\%",
        "−": "-",  # Unicode-minus till vanligt minus
        "≥": "$\\ge$",
        "≤": "$\\le$",
        "_": "\\_",
        "【": "[", "】": "]"  # Specialhakparenteser
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)

    # 8. Ta bort extra mellanslag innan punkt och komma
    text = re.sub(r'\s+([.,])', r'\1', text)

    # 9. Identifiera och konvertera tabeller
    def table_repl(match):
        header = match.group(1).strip()
        rows = match.group(2).strip().split("\n")

        # Extrahera tabellhuvudet och kolumner
        columns = [col.strip() for col in header.split("|")[1:-1]]
        num_columns = len(columns)  # Dynamiskt antal kolumner

        # Dynamiskt bestämma kolumnjustering
        col_format = []
        for col in columns:
            if re.search(r"[\d\.\%]", col):  # Om kolumnen innehåller siffror eller %
                col_format.append("r")  # Högerjustering
            else:
                col_format.append("p{6cm}")  # Textkolumner får bredare layout

        col_format_str = "|".join(col_format)

        # Skapa LaTeX-tabellens header
        latex_table = "\\begin{table}[h]\n    \\centering\n    \\renewcommand{\\arraystretch}{1.2}\n"
        latex_table += f"    \\begin{{tabular}}{{|{col_format_str}|}}\n        \\hline\n"

        # Lägg till rubriker
        latex_table += " & ".join(columns) + " \\\\\n        \\hline\n"

        # Lägg till rader och säkerställ att de har rätt antal kolumner
        for row in rows[1:]:  # Hoppa över formatraden
            row_data = [col.strip() for col in row.split("|")[1:-1]]

            # Om antalet kolumner är fel, fyll på eller trunkera raden
            if len(row_data) < num_columns:
                row_data += [""] * (num_columns - len(row_data))  # Lägg till tomma fält
            elif len(row_data) > num_columns:
                row_data = row_data[:num_columns]  # Ta bort överskott

            latex_table += " & ".join(row_data) + " \\\\\n        \\hline\n"

        latex_table += "    \\end{tabular}\n    \\caption{Tabell: Automatisk konverterad tabell}\n    \\label{tab:dynamic_table}\n\\end{table}\n"

        return latex_table

    text = re.sub(r"^\|(.+)\|\n\|[-:\s|]+\|\n((?:\|.+\|\n)+)", table_repl, text, flags=re.MULTILINE)

    return text


converted_text = convert_to_latex(input_text)

latex_template = f"""
\\documentclass[a4paper,12pt]{{report}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[swedish]{{babel}}
\\usepackage{{lmodern}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=2.5cm}}
\\usepackage{{graphicx}}
\\usepackage{{fancyhdr}}
\\usepackage{{hyperref}}
\\usepackage{{setspace}}
\\usepackage{{titling}}
\\usepackage{{parskip}}

% Sidhuvud och sidfot
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\lhead{{\\textbf{{ChatGPT Deep Research}}}}
\\rhead{{\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.5pt}}
\\setlength{{\\headheight}}{{15pt}}

% Titelinställningar
\\pretitle{{\\centering\\Huge\\bfseries}}
\\posttitle{{\\par\\vskip 2em}}
\\preauthor{{\\centering\\Large}}
\\postauthor{{\\par}}
\\predate{{\\centering\\Large}}
\\postdate{{\\par}}

\\begin{{document}}

% Titelsida
\\begin{{titlepage}}
  \\centering
  \\vspace*{{5cm}}
  {{\\Huge \\bfseries {report_title}}}\\par
  \\vspace{{2cm}}
  {{\\Large ChatGPT Deep Research}}\\par
  \\vspace{{1cm}}
  {{\\Large Underlag framtagen av AI}}\\par
  \\vspace{{2cm}}
  {{\\Large \\today}}
\\end{{titlepage}}

\\clearpage

{converted_text}

\\end{{document}}
"""

with open("rapport.tex", "w", encoding="utf-8") as file:
    file.write(latex_template)

print("LaTeX-dokumentet har skapats: rapport.tex")
