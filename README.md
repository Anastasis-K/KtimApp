KtimApp

KtimApp is a Python script designed to automate the process of retrieving and processing cadastre data from the Greek cadastre website. The script uses Selenium for web automation and ezdxf for creating DXF files from the retrieved coordinates.


Features

- Automates the search for cadastral data using a given KAEK (Κωδικός Αριθμός Εθνικού Κτηματολογίου).
- Retrieves and processes coordinates from the cadastral system.
- Generates DXF files containing polylines created from the coordinates.
- Downloads cadastral diagrams as PDF files.


Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Selenium
- ezdxf library


Installation

1. Clone the repository:

git clone https://github.com/Anastasis-K/ktimapp.git

cd ktimapp

2. Install the required Python libraries:

pip install selenium ezdxf

3. Download and install ChromeDriver and ensure it is in your PATH or specify its location in the script.


Usage

1. Prepare your environment by setting up the directory structure and downloading ChromeDriver.

2. Run the script:

python ktim_app.py

3. Input the kaek variable.


Example

The script is designed to work with the following structure:

.

├── KtimApp.py

├── ΑΡΧΕΙΟ ΚΤΗΜΑΤΟΛΟΓΙΟΥ/

│   └── *-KAEK-*/

│       ├── *-KAEK-*_ΛΕΙΤΟΥΡΓΟΥΝ.dxf

│       ├── *-KAEK-*_ΛΕΙΤΟΥΡΓΟΥΝ.pdf

│       ├── *-KAEK-*_ΑΝΑΡΤΗΣΗ.dxf

│       ├── *-KAEK-*_ΑΝΑΡΤΗΣΗ.pdf

│       ├── *-KAEK-*_ΠΡΟΑΝΑΡΤΗΣΗ.dxf

│       └── *-KAEK-*_ΠΡΟΑΝΑΡΤΗΣΗ.pdf

The script will automatically create the required directories and save the output files in the appropriate locations.


Code Overview


Functions
- 'ktima_driver(my_kaek: str)': Sets up the Chrome driver with the specified preferences.
- 'clicker(my_driver, my_xpath: str)': Clicks the element identified by the given XPath.
- 'typewriter(my_driver, my_xpath: str, my_text: str)': Sends the specified text to the element identified by the given XPath.
- 'attribute_getter(my_driver, my_xpath: str) -> str': Retrieves the value attribute of the element identified by the given XPath.
- 'coord_translator(text_of_coord: str) -> list': Translates text coordinates into a list of tuples.
- 'polyline_draw(name: str, points': (list, tuple))': Creates and saves a DXF file from a list of points.
- 'image_loader(my_driver, my_xpath: str)': Checks if an image is loaded.
- 'kaek_handler(my_driver, my_kaek: str, cadastre_phase_key: str, cdastre_phase_value: str)': Handles the KAEK search and saves the results.


Main Flow

1. Initialize the driver and navigate to the cadastral website.
2. Perform searches for each KAEK and handle the results for different cadastral phases (ΛΕΙΤΟΥΡΓΟΥΝ, ΑΝΑΡΤΗΣΗ, ΠΡΟΑΝΑΡΤΗΣΗ).
3. Retrieve coordinates and save them as DXF files.
4. Download cadastral diagrams as PDF files.


Notes

- Ensure ChromeDriver is compatible with your installed version of Google Chrome.
- The script includes various checks to ensure elements are present before interacting with them, making it robust against changes in page load times and element     availability.


Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.


License

This project is licensed under the MIT License. See the LICENSE file for details.
