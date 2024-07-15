from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
import ezdxf


def ktima_driver(my_kaek: str):
    """
    Sets up the chrome driver and the directory for saving files.
    :param my_kaek: (str) the given 'KAEK'
    :return: the chrome driver ready to use
    """
    save_path = os.path.join(os.getcwd(), "ΑΡΧΕΙΟ ΚΤΗΜΑΤΟΛΟΓΙΟΥ", my_kaek)
    os.makedirs(save_path, exist_ok=True)

    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps({
            'recentDestinations': [{'id': 'Save as PDF', 'origin': 'local', 'account': ''}],
            'selectedDestinationId': 'Save as PDF',
            'version': 2
        }),
        'savefile.default_directory': save_path,
        'download.default_directory': save_path,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')

    service = Service(executable_path="chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)


def clicker(my_driver, my_xpath: str):
    """
    Clicks the appropriate button of the given xpath.
    :param my_driver: the given driver
    :param my_xpath: (str) the associated xpath of the button
    """
    WebDriverWait(my_driver, 10).until(EC.presence_of_element_located((By.XPATH, my_xpath)))
    my_driver.find_element(By.XPATH, my_xpath).click()


def typewriter(my_driver, my_xpath: str, my_text: str):
    """
    Writes (sends) the given text to the field of the given xpath.
    :param my_driver: the given driver
    :param my_text: (str) the given text
    :param my_xpath: (str) the associated xpath of the field
    """
    WebDriverWait(my_driver, 10).until(EC.presence_of_element_located((By.XPATH, my_xpath)))
    my_driver.find_element(By.XPATH, my_xpath).send_keys(my_text)


def attribute_getter(my_driver, my_xpath: str) -> str:
    """
    Gets the attribute of the element of the given xpath.
    :param my_driver: the given driver
    :param my_xpath: (str) the associated xpath of the element
    :return: (str) the attribute of the element, in this case the 'value'
    """
    WebDriverWait(my_driver, 10).until(EC.presence_of_element_located((By.XPATH, my_xpath)))
    return my_driver.find_element(By.XPATH, my_xpath).get_attribute('value')


def coord_translator(text_of_coord: str) -> list:
    """
    'Translates' text to coordinates.
    The text contains the mixed coordinates and several symbols. By splitting and reorganising the info in the str, it returns the final list with nested tuples of coordinates.
    :param text_of_coord: (str) text of mixed coordinates
    :return: (list) the list of coordinates ready to use
    """
    coords_mixed = text_of_coord.split('@')[4].split('=')
    x_coords = [float(x) for x in coords_mixed[0].split("~")]
    y_coords = [float(y) for y in coords_mixed[1].split("~") if y]
    return zip(x_coords, y_coords)


def polyline_draw(name: str, points: (list, tuple)):
    """
    Creates the polyline from a list of points and then saves the dxf file of the given format, in this case 2007 dxf.
    :param name: (str) the name of the file/path
    :param points: (list/tuple/...) any iterable with the points of the polyline (each point in the iterable is a 'nested' tuple of its 2 coordinates e.g. (x1,y1), (x2,y2), ...)
    """
    doc = ezdxf.new('R2007')  # creates a new DXF drawing in R2007 format
    msp = doc.modelspace()  # adds new entities to the modelspace
    msp.add_lwpolyline(points, close=True)
    doc.saveas(f"{name}.dxf")


def image_loader(my_driver, my_xpath: str):
    """
    Checks if the image is loaded.
    :param my_xpath: (str) the associated xpath of the image
    :param my_driver: the given driver
    :return: (bool) True/False for 'loaded'/'not loaded' image
    """
    image = my_driver.find_element(By.XPATH, my_xpath)
    return my_driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth != 0", image)


def kaek_handler(my_driver, my_kaek: str, cadastre_phase_key: str, cdastre_phase_value: str):
    """
    Handles the KAEK search and saves the results.
    :param my_driver: the given driver
    :param my_kaek: (str) the given 'KAEK'
    :param cadastre_phase_key: (str) the specific cadastre phase name
    :param cdastre_phase_value: (str) the xpath for this cadastre phase results
    """
    try:
        saving_path = f"./ΑΡΧΕΙΟ ΚΤΗΜΑΤΟΛΟΓΙΟΥ/{my_kaek}"
        saving_dxf_name = f"{my_kaek}_{cadastre_phase_key}"
        saving_pdf_name = f"{my_kaek}_{cadastre_phase_key}.pdf"

        clicker(my_driver, cdastre_phase_value)
        clicker(my_driver, '//*[@id="searchGroup"]/a[2]/i')
        WebDriverWait(my_driver, 10).until(EC.number_of_windows_to_be(2))

        # 'gets' and 'translates' the coordinates, then creates the polyline file and saves it
        the_text_with_coords = attribute_getter(my_driver, '//*[@id="KT__ApospasmaForm"]/input[1]')
        final_coord_list = coord_translator(the_text_with_coords)
        polyline_draw(os.path.join(saving_path, saving_dxf_name), final_coord_list)

        # finds the 'pdf' diagram file by navigating through the driver windows
        original_window = my_driver.current_window_handle
        for window_handle in my_driver.window_handles:
            if window_handle != original_window:
                my_driver.switch_to.window(window_handle)
                break

        # waits for the image to load before 'printing' and then saves the pdf
        WebDriverWait(my_driver, 15).until(lambda d: image_loader(d, '/html/body/table/tbody/tr[1]/td/img'))
        my_driver.execute_script('window.print();')
        my_driver.execute_script('window.close();')
        my_driver.switch_to.window(original_window)
        clicker(my_driver, '//*[@id="searchGroup"]/a[1]')

        # renames the saved pdf file accordingly

        if saving_pdf_name in os.listdir(saving_path):
            os.unlink(os.path.join(saving_path, saving_pdf_name))
        if "download.pdf" in os.listdir(saving_path):
            os.rename(os.path.join(saving_path, "download.pdf"), os.path.join(saving_path, saving_pdf_name))
        time.sleep(1)
    except Exception:
        pass


if __name__ == "__main__":

    # kaek = input("Εισαγωγή ΚΑΕΚ:\n")

    kaek = "350246609016"
    driver = ktima_driver(kaek)
    driver.get("https://maps.gov.gr/gis/map/")

    # navigates through the webpage and searches with the given 'KAEK'
    clicker(driver, '//*[@id="searchGroup"]/a[1]/i')
    clicker(driver, '//*[@id="parcelcode-tab"]')
    typewriter(driver, '//*[@id="KT__TxtGPropID"]', kaek)
    clicker(driver, '//*[@id="KT__CmdSearchByGPropID"]')

    # there are 3 types of 'cadastre phases'
    cadastre_phase = {"ΛΕΙΤΟΥΡΓΟΥΝ": '//*[@id="KT__SearchByKAEKResults"]/div[2]/small[2]',
                      "ΑΝΑΡΤΗΣΗ": '//*[@id="KT__SearchByKAEKResults"]/div[4]/small[2]',
                      "ΠΡΟΑΝΑΡΤΗΣΗ": '//*[@id="KT__SearchByKAEKResults"]/div[6]/small[2]'}

    # the algorythm will run for each one and if there is a result will execute all the necessary actions
    for key, value in cadastre_phase.items():
        kaek_handler(my_driver=driver, my_kaek=kaek, cadastre_phase_key=key, cdastre_phase_value=value)

    driver.quit()

    # testing
    # list_of_kaek = ["050912502005", "050095701001", "050912502004", "050321701026", "350246609016", "350310118045"]
    # for kaek in list_of_kaek:
    #     driver_starter(kaek)
