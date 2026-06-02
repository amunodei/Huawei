# CSR Initial Script Generator

A small local web app that generates batch CSR initial scripts from a template + your IP planning workbook.

## What it does

1. You paste a **script template** (with placeholders like `{{csr_id}}`, `{{csr_ip}}`, `{{mask}}`)
2. You paste a list of **ESNs**
3. You upload the **Excel IP planning workbook** (the one with `National CSR List` and `National PTP` tabs)
4. Click **Preview mappings** to verify the ESN -> CSR_ID -> IP resolution
5. Click **Generate & download zip** - you get a zip containing one `CSR-XXXX_ESN.txt` per ESN, under a folder named `<BatchName>_<YYYY-MM-DD_HH-MM>/`

## Setup (Windows)

Requires Python 3.10+ (https://www.python.org/downloads/ - tick "Add to PATH" during install).

Double-click `run.bat`. On first run it creates a local `.venv` and installs Flask + openpyxl, then starts the server and opens your browser.

## Setup (manual / macOS / Linux)

```
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Template placeholders

| Placeholder      | Source                                   |
|------------------|-------------------------------------------|
| `{{csr_id}}`     | National CSR List - `CSR_ID` (looked up by ESN) |
| `{{esn}}`        | The ESN you supplied                      |
| `{{csr_ip}}`     | National PTP - `CSR_IP` (uplink IP)       |
| `{{csr_cidr}}`   | National PTP - `CSR_CIDR` (e.g. `/30`)    |
| `{{mask}}`       | Dotted netmask derived from `{{csr_cidr}}` |
| `{{lo0_ip}}`     | National CSR List - `Lo0_IP` (used for MPLS LSR-ID + BGP router-id) |
| `{{lo0_cidr}}`   | National CSR List - `Lo0_CIDR`            |
| `{{lo0_mask}}`   | Dotted netmask derived from `{{lo0_cidr}}` |
| `{{lo1_ip}}`     | National CSR List - `Lo1_IP` (used for hwtacacs-server source-ip) |
| `{{lo1_cidr}}`   | National CSR List - `Lo1_CIDR`            |
| `{{lo1_mask}}`   | Dotted netmask derived from `{{lo1_cidr}}` |

## Sheet / column overrides

If your workbook renames any of the tabs or columns, edit the fields in section 4 of the form. Defaults:

- CSR list sheet: `National CSR List`
- PTP sheet: `National PTP`
- Header row: `2`
- Columns: `CSR_ID`, `ESN` (CSR list); `CSR_ID`, `CSR_IP`, `CSR_CIDR` (PTP)

## Output

The generated zip contains:

```
<BatchName>_<YYYY-MM-DD_HH-MM>/
    CSR-0404_2102355NEN10S4100026.txt
    CSR-0405_2102355NEN10S4100048.txt
    ...
    _summary.tsv                 <- tab-separated lookup table (ESN, CSR_ID, IP, mask, status)
```

Line endings default to CRLF (Windows); switch to LF in the UI if needed.
