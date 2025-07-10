import os
import requests
import argparse
from urllib.parse import urlparse

# Default configuration
DEFAULT_MBS_URL = "https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/650f3eec0dfb990fca25692100069854/0b61e1e80b332754ca258c9e0000c7d8/$FILE/MBS-XML-20250701%20Version%203.XML"
DEFAULT_OUTPUT_DIR = "../../" # Changed: Output to project root relative to this script
DEFAULT_FILENAME = "temp_mbs_download.xml" # Added default temporary filename

def get_filename_from_url(url, default_filename=DEFAULT_FILENAME):
    """Extracts a filename from a URL, or returns a default."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if '%' in filename: # Handle URL encoded filenames like the MBS one
        from urllib.parse import unquote
        filename = unquote(filename)
    return filename if filename else default_filename

def download_file(url, output_dir, filename): # filename is now mandatory for clarity
    """
    Downloads a file from a URL to a specified directory with a specific filename.
    """
    # We expect output_dir to be an absolute path by the time this function is called.
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Attempting to create it.")
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Successfully created output directory {output_dir}")
        except OSError as e:
            print(f"Error: Could not create output directory {output_dir}: {e}")
            return False

    output_path = os.path.join(output_dir, filename)

    try:
        print(f"Downloading MBS XML from {url} to {output_path}...")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded {filename} to {output_dir}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False
    except IOError as e:
        print(f"Error writing file to {output_path}: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MBS XML file.")
    parser.add_argument("--url", type=str, default=DEFAULT_MBS_URL,
                        help=f"URL of the MBS XML file. Defaults to: {DEFAULT_MBS_URL}")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR,
                        help=f"Directory to save the downloaded file. Defaults to: {DEFAULT_OUTPUT_DIR} (project root relative to script).")
    parser.add_argument("--filename", type=str, default=DEFAULT_FILENAME,
                        help=f"Specific filename to save as. Defaults to: {DEFAULT_FILENAME}")

    args = parser.parse_args()

    if os.path.isabs(args.output_dir):
        normalized_output_dir = os.path.normpath(args.output_dir)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_output_dir = os.path.join(script_dir, args.output_dir)
        normalized_output_dir = os.path.normpath(resolved_output_dir)

    # Ensure the target directory (project root in this case) exists.
    # For project root, it should always exist, but good practice if path changes.
    if not os.path.exists(normalized_output_dir):
        print(f"Final output directory {normalized_output_dir} does not exist. Attempting to create it.")
        try:
            os.makedirs(normalized_output_dir, exist_ok=True) # exist_ok=True is important
            print(f"Successfully created output directory {normalized_output_dir}")
        except OSError as e:
            print(f"Critical Error: Could not create output directory {normalized_output_dir}: {e}")
            exit(1) # Exit if we can't create the target dir

    # Use the specific filename from args (which defaults to DEFAULT_FILENAME)
    if download_file(args.url, normalized_output_dir, args.filename):
        print("MBS download script finished successfully.")
    else:
        print("MBS download script encountered an error.")
