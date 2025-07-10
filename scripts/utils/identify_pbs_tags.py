import requests
import zipfile
import io
import argparse
from lxml import etree

# Default configuration
DEFAULT_PBS_URL = "https://m.pbs.gov.au/downloads/2025/07/2025-07-01-xml-V3.zip"
TARGET_XML_PATTERN = "sch-*.xml" # Pattern to identify the main schedule XML
PHARMACEUTICAL_ITEM_TAG = "{http://schema.pbs.gov.au/}pharmaceutical-item"

def get_first_pharmaceutical_item_xml(url):
    """
    Downloads PBS ZIP, extracts the main XML in memory, finds the first
    <pbs:pharmaceutical-item> element and prints its XML structure.
    """
    print(f"Attempting to download PBS ZIP archive from {url}...")
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        print("Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading ZIP file: {e}")
        return

    print("Attempting to process ZIP in memory...")
    xml_content_bytes = None
    xml_filename = None
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            import fnmatch
            for member_name in zf.namelist():
                if fnmatch.fnmatch(member_name.lower(), TARGET_XML_PATTERN):
                    xml_filename = member_name
                    break

            if not xml_filename:
                print(f"No XML file matching pattern '{TARGET_XML_PATTERN}' found in the ZIP.")
                return

            print(f"Found XML file in ZIP: {xml_filename}. Reading its content into memory...")
            xml_content_bytes = zf.read(xml_filename)
            print(f"XML content size: {len(xml_content_bytes)} bytes.")

    except zipfile.BadZipFile:
        print("Error: Downloaded content is not a valid ZIP archive or is corrupted.")
        return
    except Exception as e:
        print(f"An error occurred during ZIP processing: {e}")
        return

    if not xml_content_bytes:
        print("Failed to get XML content from ZIP.")
        return

    print(f"\nSearching for the first '{PHARMACEUTICAL_ITEM_TAG}' in {xml_filename}...")

    try:
        context = etree.iterparse(io.BytesIO(xml_content_bytes), events=('end',), tag=PHARMACEUTICAL_ITEM_TAG)

        first_item_found = False
        for event, elem in context:
            # We found the first item, print its structure and stop
            print(f"\n--- XML Structure of the first '{PHARMACEUTICAL_ITEM_TAG}' ---")
            # Using tostring to get the XML of this specific element
            # Add XML declaration and ensure UTF-8 encoding for print
            xml_string = etree.tostring(elem, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')
            print(xml_string)
            first_item_found = True

            # Clear element and break since we only need the first one
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            break

        del context

        if not first_item_found:
            print(f"No '{PHARMACEUTICAL_ITEM_TAG}' element found in the parsed portion of the XML.")
            print("This could be because the tag name is incorrect, it appears very late in the document,")
            print("or the document structure is different than expected.")

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error while parsing: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and print the first pbs:pharmaceutical-item from PBS XML.")
    parser.add_argument("--url", type=str, default=DEFAULT_PBS_URL,
                        help=f"URL of the PBS ZIP file. Defaults to: {DEFAULT_PBS_URL}")

    args = parser.parse_args()
    get_first_pharmaceutical_item_xml(args.url)
