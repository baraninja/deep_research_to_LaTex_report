# ChatGPT Deep Research to LaTeX Report Converter

Detta Python-skript konverterar en Markdown-fil genererad av ChatGPT Deep Research till ett LaTeX-dokument. Syftet är att underlätta skapandet av läsbara rapporter från AI-genererat innehåll.

## Funktioner

- **Konvertering av rubriker**: Översätter Markdown-rubriker till motsvarande LaTeX-strukturer.
- **Hantera listor**: Omvandlar listor till LaTeX-underrubriker.
- **Specialtecken**: Ersätter tecken som kan orsaka problem i LaTeX.
- **Tabellhantering**: Identifierar och konverterar Markdown-tabeller till LaTeX-tabeller.
- **Anpassningsbar titel**: Möjlighet att ange rapportens titel via kommandoraden.

## Installation

1. **Klona eller ladda ner** detta repository till din lokala maskin.
2. **Se till att Python 3.x är installerat** på ditt system.

## Användning

1. **Förbered din Markdown-fil**: Se till att din `rapport.md`-fil finns i samma katalog som skriptet.
2. **Kör skriptet**:
   ```bash
   python3 convert_to_latex.py "Din rapporttitel"
   ```
   Om ingen titel anges används standardtiteln "Rapportens titel".

3. **Generera PDF**: Efter att `rapport.tex` har skapats kan du kompilera den till PDF med hjälp av LaTeX:
   ```bash
   pdflatex rapport.tex
   ```

## Begränsningar och utvecklingsområden

- **Källhänvisningar**: För närvarande tas alla källhänvisningar bort under konverteringen. Implementering av fotnoter och en referenslista i slutet av dokumentet är planerad för framtida versioner.
- **Tabellhantering**: Skriptet försöker dynamiskt bestämma kolumnjustering baserat på innehållet, men ytterligare förbättringar kan behövas för komplexa tabeller.

## Bidra

Bidrag är välkomna! Om du har förslag, hittar buggar eller vill förbättra funktionaliteten, vänligen skapa en pull request eller öppna ett ärende i repositoryt.

## Licens

Detta projekt är licensierat under MIT-licensen. Se `LICENSE`-filen för mer information.

---

*Observera: ChatGPT Deep Research är en ny funktion från OpenAI som möjliggör automatiserad, flerstegs forskning på internet för komplexa uppgifter. Den är för närvarande tillgänglig för Pro-prenumeranter och kan generera detaljerade rapporter genom att analysera och syntetisera information från olika onlinekällor.*
