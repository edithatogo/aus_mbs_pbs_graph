import argparse
import os
from lxml import etree

# Configuration
DEFAULT_MBS_XML_PATH = "../../temp_mbs_download.xml"
MAX_ITEMS_TO_PRINT = 5

def parse_mbs_xml_initial(xml_file_path, max_items=MAX_ITEMS_TO_PRINT):
    """
    Parses the MBS XML file and prints key details for the first few items.
    Focuses on ItemNum, ItemDesc, and a primary Fee.
    """
    if not os.path.exists(xml_file_path):
        print(f"Error: XML file not found at {xml_file_path}")
        return

    print(f"Starting parsing of {xml_file_path}...")
    items_parsed_count = 0

    try:
        # Use iterparse for memory-efficient parsing
        # We are interested in the 'end' event for 'MBSItem' tags (adjust tag if needed based on actual XML)
        # The actual main item tag might be different, e.g. 'Item' or similar.
        # This needs to be verified by inspecting the XML structure.
        # For now, assuming 'MBSItem' is a wrapper for each item's data.
        # If 'MBSItem' is not the repeating element for each item, this will need adjustment.
        # A common structure is <MBSXML><MBSItem>...</MBSItem><MBSItem>...</MBSItem></MBSXML>
        # Or it could be <MBSXML><Category><SubCategory><Item>...</Item></SubCategory></Category>
        # For this initial script, let's assume a relatively flat structure where items are under a common parent,
        # and 'MBSItem' is a good candidate tag name for an item entry.
        # If the actual item tag is just 'Item', then context should be etree.iterparse(xml_file_path, events=('end',), tag='Item')

        # Let's assume the root is something like 'MBSDownloads' and items are 'MBSItem'
        # This is a guess and needs to be confirmed by looking at the XML.
        # The provided XML filename "MBS-XML-20250701 Version 3.XML" suggests it's the whole MBS.
        # A quick look at sample MBS XML online suggests items might be within <MBSItems><MBSItem> or similar.
        # Let's assume 'MBSItem' is the correct tag for individual items for now.
        # The actual tag for an item might be 'Item', 'Service', etc.
        # For now, I will use 'MBSItem' as a placeholder tag. This is the MOST LIKELY part to need correction
        # after inspecting the actual XML file structure.

        context = etree.iterparse(xml_file_path, events=('end',), tag='MBSItem') # IMPORTANT: 'MBSItem' tag is a guess

        for event, elem in context:
            if items_parsed_count >= max_items:
                break

            item_num_elem = elem.find('ItemNum') # Guessing child tag names
            item_desc_elem = elem.find('ItemDesc')

            # Fee extraction can be complex. There might be multiple fee types.
            # For simplicity, let's try to find a 'FeeAmount' within a 'Fee' element,
            # or a specific type of fee if identifiable.
            # This is a simplified approach for initial parsing.
            fee_amount_str = "N/A"
            fee_elem = elem.find('.//Fee') # Find first Fee element anywhere under MBSItem
            if fee_elem is not None:
                # Try to find a common fee amount tag, e.g. 'Amount', 'FeeAmount'
                # This needs verification from actual XML.
                amount_tag = fee_elem.find('Amount') # Common tag name
                if amount_tag is None:
                    amount_tag = fee_elem.find('FeeAmount') # Alternative

                if amount_tag is not None and amount_tag.text:
                    fee_amount_str = amount_tag.text.strip()
                elif fee_elem.text and fee_elem.text.strip(): # If fee is directly in <Fee> text
                    fee_amount_str = fee_elem.text.strip()


            item_num = item_num_elem.text.strip() if item_num_elem is not None and item_num_elem.text else "N/A"
            item_desc = item_desc_elem.text.strip() if item_desc_elem is not None and item_desc_elem.text else "N/A"

            print(f"Item: {item_num}, Desc: {item_desc}, Fee: {fee_amount_str}")
            items_parsed_count += 1

            # It's crucial to clear the element and its predecessors to free memory
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        del context

        if items_parsed_count == 0:
            print(f"No items found with tag 'MBSItem'. Please verify the item tag in the XML structure.")
        else:
            print(f"\nFinished parsing. Printed details for {items_parsed_count} item(s).")

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse the MBS XML file and print initial item details.")
    parser.add_argument("--file_path", type=str, default=DEFAULT_MBS_XML_PATH,
                        help=f"Path to the MBS XML file. Defaults to: {DEFAULT_MBS_XML_PATH} (relative to script location if not absolute)")
    parser.add_argument("--max_items", type=int, default=MAX_ITEMS_TO_PRINT,
                        help=f"Maximum number of items to parse and print. Defaults to: {MAX_ITEMS_TO_PRINT}")

    args = parser.parse_args()

    # Adjust file_path to be an absolute path from the script's location if it's relative
    # This makes it easier to run the script from any directory if file_path is relative to script
    if not os.path.isabs(args.file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_file_path = os.path.join(script_dir, args.file_path)
        normalized_file_path = os.path.normpath(resolved_file_path)
    else:
        normalized_file_path = args.file_path

    parse_mbs_xml_initial(normalized_file_path, args.max_items)
