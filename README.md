# DDSM_CBIS_photos_server

Flask server that handles data retrieval and processing, interacting with the CBIS-DDSM dataset to serve relevant data to the [Electron app](https://github.com/DDSM-CBIS/ddss-electron). The backend processes queries, retrieves patient metadata, and returns filtered results.

## Pre-Requisites

To use the following project, please make sure you have the following installed:

- [python](https://www.python.org/downloads/)
- [Client](https://github.com/DDSM-CBIS/ddss-electron)

- Clone the repository:

```bash
git clone https://github.com/DDSM-CBIS/ddss-server.git
```

## Usage

Install requirements:

```bash
pip install -r ./requierments.txt
```

Run the server:

```bash
python3 run.py
```
