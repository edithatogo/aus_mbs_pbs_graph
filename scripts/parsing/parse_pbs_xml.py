import requests
import zipfile
import io
import argparse
from lxml import etree
from collections import defaultdict

# Default configuration
DEFAULT_PBS_URL = "https://m.pbs.gov.au/downloads/2025/07/2025-07-01-xml-V3.zip"
TARGET_XML_PATTERN = "sch-*.xml" # Pattern to identify the main schedule XML
MAX_ITEMS_TO_PRINT = 5

# Define namespaces to make XPath queries cleaner
NS_MAP = {
    'pbs': 'http://schema.pbs.gov.au/',
    'dbk': 'http://docbook.org/ns/docbook',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'ext': 'http://extension.schema.pbs.gov.au/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xml': 'http://www.w3.org/XML/1998/namespace' # For xml:id
}

def parse_pbs_xml_initial(url, max_items_to_print=MAX_ITEMS_TO_PRINT):
    """
    Downloads PBS ZIP, extracts main XML in memory, and parses the first few
    pbs:pharmaceutical-item elements to extract key details using corrected XPaths.
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
    xml_filename = None # Define xml_filename here
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

    print(f"\nStarting parsing of {xml_filename} for first {max_items_to_print} pharmaceutical items...")
    items_parsed_count = 0

    target_tag = "{http://schema.pbs.gov.au/}pharmaceutical-item"

    try:
        context = etree.iterparse(io.BytesIO(xml_content_bytes), events=('end',), tag=target_tag)

        for event, elem in context:
            if items_parsed_count >= max_items_to_print:
                break

            item_data = defaultdict(lambda: "N/A")

            # --- PBS Item Code (xml:id) ---
            item_id = elem.get('{http://www.w3.org/XML/1998/namespace}id')
            if item_id:
                item_data['pbs_item_code'] = item_id

            # --- Drug Name/Description ---
            # Path: ./pbs:block-container/dbk:para/text()
            name_elem = elem.find('./pbs:block-container/dbk:para', namespaces=NS_MAP)
            if name_elem is not None and name_elem.text:
                item_data['drug_name'] = name_elem.text.strip()

            # --- AMT Code(s) ---
            # Path: ./pbs:drug-references-list/pbs:mp-reference/pbs:code
            # This code element's text is likely the AMT ID (as SNOMED CT concept ID)
            # The rdf:resource might contain the SNOMED URI for it.
            amt_codes_info = []
            mp_refs = elem.findall('./pbs:drug-references-list/pbs:mp-reference', namespaces=NS_MAP)
            for mp_ref in mp_refs:
                code_elem = mp_ref.find('./pbs:code', namespaces=NS_MAP)
                if code_elem is not None and code_elem.text:
                    code_text = code_elem.text.strip()
                    rdf_resource = code_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'N/A')
                    # Check if type attribute exists, though not in the sample item
                    code_type = code_elem.get('type', 'Implicit (likely AMT/SNOMED CT ID)')
                    amt_codes_info.append(f"{code_text} (Type: {code_type}, Resource: {rdf_resource})")
            if amt_codes_info:
                item_data['amt_codes_info'] = "; ".join(amt_codes_info)


            # --- ATC Code(s) ---
            # Search for <pbs:code type="ATC"> anywhere within the item.
            # This was not in the single sample, so it's a broader search.
            atc_codes = []
            for code_elem in elem.findall('.//pbs:code[@type="ATC"]', namespaces=NS_MAP):
                if code_elem.text:
                    atc_codes.append(code_elem.text.strip())
            if atc_codes:
                item_data['atc_codes'] = ", ".join(atc_codes)


            print(f"\n--- Item {items_parsed_count + 1} ---")
            print(f"  PBS Item Code (xml:id): {item_data['pbs_item_code']}")
            print(f"  Drug Name/Description: {item_data['drug_name']}")
            print(f"  AMT Codes Info: {item_data['amt_codes_info']}")
            print(f"  ATC Codes: {item_data['atc_codes']}")

            items_parsed_count += 1
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        del context

        if items_parsed_count == 0:
            print(f"No items found with tag '{target_tag}'. This might indicate an issue with the tag name or the XML structure.")
        else:
            print(f"\nFinished parsing. Printed details for {items_parsed_count} item(s).")

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PBS XML (from ZIP URL, in memory) and print initial item details.")
    parser.add_argument("--url", type=str, default=DEFAULT_PBS_URL,
                        help=f"URL of the PBS ZIP file. Defaults to: {DEFAULT_PBS_URL}")
    parser.add_argument("--max_items", type=int, default=MAX_ITEMS_TO_PRINT,
                        help=f"Maximum number of items to parse and print. Defaults to: {MAX_ITEMS_TO_PRINT}")

    args = parser.parse_args()
    parse_pbs_xml_initial(args.url, args.max_items)
```
