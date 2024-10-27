# CBIS-DDSM Server

Flask server that handles data retrieval and processing, interacting with the CBIS-DDSM dataset to serve relevant data to the [Electron app](https://github.com/DDSM-CBIS/ddsm-electron). The backend processes queries, retrieves patient metadata, and returns filtered results.

## Pre-Requisites

To use the following project, please make sure you have the following installed:

- [python](https://www.python.org/downloads/)
- [Client](https://github.com/DDSM-CBIS/ddsm-electron)

- Clone the repository:

```bash
git clone https://github.com/DDSM-CBIS/ddsm-server.git
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

## Project Structure

### config.json

Contains the base configuration for the server.

```json
{
  "series_name": "CBIS-DDSM",
  "base_url": "https://services.cancerimagingarchive.net/nbia-api/services/v1/",
  "calc_file_path": "./data/calc_set.csv",
  "mass_file_path": "./data/mass_set.csv"
}
```

- series_name: The series in which the data should be loaded from. Under this project perspective, the CBIS-DDSM data set is used.
- base_url: The base URL of the server responsible for the APIs of the dataset.
- calc_file_path and mass_file_path: Downloaded directly from the [CBIS-DDSM documentation](https://www.cancerimagingarchive.net/collection/cbis-ddsm/) containing the images data.

### Data

Contains the `calc_set.csv` and `mass_set.csv` files.

### Utils

The utils folder contains the `data_manager` and the `series_manager`.

- `data_manager`: Manages the data under `calc_set.csv` and `mass_set.csv`. Its responsible for:
  - Extracting the unique options for the filtering.
  - Patients data demanded by the client.
  - The filtering functionality.
- `series_manager`: Responsible for sending the API requests to the dataset server.
  - `get_base_url`: Contains all the routes of the requested endpoints. The routes can be found in the [NBIA Search REST API Guide](https://wiki.cancerimagingarchive.net/display/Public/NBIA+Search+REST+API+Guide#NBIASearchRESTAPIGuide-getSingleImage).
  - `get_image_by_uids`: Responsible for the JPEG Conversion, where the DICOM images converted to JPEG for faster transmission to the electron client. In order to get an image from the dataset, the **SeriesInstanceUID** and **StudyInstanceUID** are needed.
    To receive those IDs, the `get_patient_series_instance_uids` and `get_sop_uids` functions are user. This because each **SeriesInstanceUID** can be related to several different images, but the corresponding **StudyInstanceUID** is unique.

### APIs

The server's APIs can be found under `filter`, `image` and `patient` folders.

**filter**

- `filter/options`: Returns the unique filter parameters in the `calc_set.csv`, used in the electron client under the **Filters** column.
- `filter/abnormality-options`: Returns the unique filter parameters in the `mass_set.csv`, used in the electron client under the **Abnormality Params** column.
- `filter/patients-ids`: Returns the unique patients IDs in the `calc_set.csv` and`mass_set.csv`.

**image**

- `images/<patient_id>/images-metadata`: Receives the image format (full, roi or all), and returns the
  - all:
    ```json
    {
      "imageCount": 4,
      "imagesMetadata": [
        {
          "class": "Mass-Training",
          "imageFormat": "all",
          "imageView": "CC",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": [
            "1.3.6.1.4.1.9590.100.1.2.14875889413880494636004673850848948118",
            "1.3.6.1.4.1.9590.100.1.2.279230283311549236005970654043226959450"
          ],
          "uid": "1.3.6.1.4.1.9590.100.1.2.296736403313792599626368780122205399650"
        },
        {
          "class": "Mass-Training",
          "imageFormat": "all",
          "imageView": "MLO",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": [
            "1.3.6.1.4.1.9590.100.1.2.194533277513825438327220734753021300752",
            "1.3.6.1.4.1.9590.100.1.2.76617112412536084713079302880894563967"
          ],
          "uid": "1.3.6.1.4.1.9590.100.1.2.227955274711225756835838775062793186053"
        },
        {
          "class": "Mass-Training",
          "imageFormat": "all",
          "imageView": "CC",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": ["1.3.6.1.4.1.9590.100.1.2.156556873010981646517128874312129349516"],
          "uid": "1.3.6.1.4.1.9590.100.1.2.342386194811267636608694132590482924515"
        },
        {
          "class": "Mass-Training",
          "imageFormat": "all",
          "imageView": "MLO",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": ["1.3.6.1.4.1.9590.100.1.2.16927317613478383512517710492717097139"],
          "uid": "1.3.6.1.4.1.9590.100.1.2.359308329312397897125630708681441180834"
        }
      ]
    }
    ```
  - full:
    ```json
    {
      "imageCount": 2,
      "imagesMetadata": [
        {
          "class": "Mass-Training",
          "imageFormat": "full",
          "imageView": "CC",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": ["1.3.6.1.4.1.9590.100.1.2.156556873010981646517128874312129349516"],
          "uid": "1.3.6.1.4.1.9590.100.1.2.342386194811267636608694132590482924515"
        },
        {
          "class": "Mass-Training",
          "imageFormat": "full",
          "imageView": "MLO",
          "leftOrRightBreast": "LEFT",
          "sopUIDs": ["1.3.6.1.4.1.9590.100.1.2.16927317613478383512517710492717097139"],
          "uid": "1.3.6.1.4.1.9590.100.1.2.359308329312397897125630708681441180834"
        }
      ]
    }
    ```
- `images/full`: Receives the **SeriesInstanceUID** and **StudyInstanceUID** and responds with the corresponding image using the `series_manager`.

**patient**

- `patients/`: Returns all patients data.
- `patients/<patient_id>`: Returns the data of the corresponding patient.
  ```json
  {
    "P_01009": [
      {
        "abnormalityId": 1,
        "abnormalityType": "mass",
        "assessment": 4,
        "breastDensity": 2,
        "imageView": "CC",
        "leftOrRightBreast": "RIGHT",
        "massMargins": "OBSCURED",
        "massShape": "OVAL",
        "pathology": "MALIGNANT",
        "subtlety": 2
      },
      {
        "abnormalityId": 1,
        "abnormalityType": "mass",
        "assessment": 4,
        "breastDensity": 2,
        "imageView": "MLO",
        "leftOrRightBreast": "RIGHT",
        "massMargins": "OBSCURED",
        "massShape": "OVAL",
        "pathology": "MALIGNANT",
        "subtlety": 3
      }
    ]
  }
  ```
- `patients/filter`: Given filters params from the electron client, this endpoint returns all the patients IDs that match the requested query.
