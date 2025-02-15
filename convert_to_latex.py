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
    Konverterar Markdown-text till LaTeX-format inklusive rubriker, listor,
    specialtecken och tabeller.
    """

    # 1. Ta bort fetstil (**text**) och kursiv (*text*)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Fetstil
    text = re.sub(r'\*(.+?)\*', r'\1', text)      # Kursiv

    # 2. Ta bort alla markdown-länkar
    text = re.sub(r'\[\[.*?\]\(.*?\)\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text, flags=re.DOTALL)

    # 3. Ta bort eventuella tomma parenteser
    text = re.sub(r'\(\s*\)', '', text)

    # 4. Ersätt narrow no-break space (U+202F) med ett vanligt mellanslag
    text = text.replace("\u202F", " ")

    # 5. Omvandla rubriker: rader som börjar med ett eller flera "#" -> LaTeX-rubriker
    def heading_repl(match):
        hashes = match.group(1)
        title = match.group(2).strip()
        level = len(hashes)
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
    #    Inga dollartecken kring \alpha etc. – vi sätter in dem separat i steg 10.
    special_chars = {
        "%": "\\%",
        "−": "-",        # Unicode-minus -> vanligt minus
        "≥": "$\\ge$",
        "≤": "$\\le$",
        "_": "\\_",
        "α": "\\alpha",
        "β": "\\beta",
        "γ": "\\gamma",
        "δ": "\\delta",
        "Δ": "\\Delta",
        "<sub>": "_{",  # \alpha<sub>2</sub> -> \alpha_{2}
        "</sub>": "}",
        "<sup>": "^{",
        "</sup>": "}",
        "【": "[", "】": "]"
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)

    # 8. Ta bort extra mellanslag innan punkt och komma
    text = re.sub(r'\s+([.,])', r'\1', text)

    # 9. Konvertera tabeller (Markdown -> LaTeX)
    def table_repl(match):
        header = match.group(1).strip()
        rows = match.group(2).strip().split("\n")

        # Extrahera tabellhuvudet och kolumner
        columns = [col.strip() for col in header.split("|")[1:-1]]
        num_columns = len(columns)

        # Dynamiskt bestämma kolumnjustering
        col_format = []
        for col in columns:
            if re.search(r"[\d\.\%]", col):
                col_format.append("r")  # högerjustering
            else:
                col_format.append("p{6cm}")
        col_format_str = "|".join(col_format)

        latex_table = (
            "\\begin{table}[h]\n"
            "    \\centering\n"
            "    \\renewcommand{\\arraystretch}{1.2}\n"
        )
        latex_table += f"    \\begin{{tabular}}{{|{col_format_str}|}}\n        \\hline\n"

        # Rubriker
        latex_table += " & ".join(columns) + " \\\\\n        \\hline\n"

        # Rader
        for row in rows[1:]:
            row_data = [col.strip() for col in row.split("|")[1:-1]]
            if len(row_data) < num_columns:
                row_data += [""] * (num_columns - len(row_data))
            elif len(row_data) > num_columns:
                row_data = row_data[:num_columns]
            latex_table += " & ".join(row_data) + " \\\\\n        \\hline\n"

        latex_table += (
            "    \\end{tabular}\n"
            "    \\caption{Tabell: Automatisk konverterad tabell}\n"
            "    \\label{tab:dynamic_table}\n"
            "\\end{table}\n"
        )
        return latex_table

    text = re.sub(
        r"^\|(.+)\|\n\|[-:\s|]+\|\n((?:\|.+\|\n)+)",
        table_repl,
        text,
        flags=re.MULTILINE
    )

    # 10. Lägg in '$...$' runt \alpha_{2}\delta – oavsett efterföljande text
    #     I exemplet nedan fångas "(\alpha_{2}\delta-subenheter)" => "($\alpha_{2}\delta$-subenheter)"
    #
    #     Vill du göra det ännu mer generellt (fler siffror/andra bokstäver)
    #     kan du justera regexen, t.ex. r'(\\alpha_\{\d+\}\\delta)' etc.
    text = re.sub(
        r'(\\alpha_\{\d+\}\\delta)([^\s)]*)',  # fångar ev. bindestreck + ord, men stannar om mellanslag/parentes etc.
        r'$\1$\2',                             # lägger in inline math runt \alpha_{2}\delta
        text
    )

    return text


converted_text = convert_to_latex(input_text)

latex_template = f"""
\\documentclass[a4paper,12pt]{{report}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[swedish]{{babel}}
\\usepackage{{lmodern}}
\\usepackage{{textcomp}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=2.5cm}}
\\usepackage{{graphicx}}
\\usepackage{{fancyhdr}}
\\usepackage{{hyperref}}
\\hypersetup{{pageanchor=false}}
\\usepackage{{setspace}}
\\usepackage{{titling}}
\\usepackage{{parskip}}
\\sloppy
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\lhead{{\\textbf{{ChatGPT Deep Research}}}}
\\rhead{{\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.5pt}}
\\setlength{{\\headheight}}{{15pt}}

\\begin{{document}}

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
