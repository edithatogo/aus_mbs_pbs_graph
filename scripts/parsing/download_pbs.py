import os
import requests
import zipfile
import io
import argparse
from urllib.parse import urlparse

# Default configuration
DEFAULT_PBS_URL = "https://m.pbs.gov.au/downloads/2025/07/2025-07-01-xml-V3.zip"
DEFAULT_OUTPUT_DIR = "../../" # Changed: Output to project root relative to this script

def get_filename_from_url(url):
    """Extracts a filename from a URL."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_pbs_archive.zip"

def download_and_unzip_pbs(url, output_dir):
    """
    Downloads a ZIP file from a URL, extracts its XML contents to a specified directory.
    """
    # output_dir is expected to be an absolute path when this function is called.
    if not os.path.exists(output_dir):
        # This should ideally be handled before calling, but as a safeguard:
        print(f"Output directory {output_dir} does not exist. Attempting to create it.")
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Successfully created output directory {output_dir}")
        except OSError as e:
            print(f"Error: Could not create output directory {output_dir}: {e}")
            return False

    try:
        print(f"Downloading PBS ZIP archive from {url}...")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        print("Download complete. Attempting to extract XML files in memory...")

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            extracted_files_count = 0
            extracted_file_names = []
            for member in zf.namelist():
                if member.lower().endswith('.xml'):
                    target_filename = os.path.basename(member)
                    target_path = os.path.join(output_dir, target_filename)

                    print(f"Extracting {member} to {target_path}...")
                    with open(target_path, 'wb') as outfile:
                        outfile.write(zf.read(member))
                    extracted_files_count += 1
                    extracted_file_names.append(target_filename)
                    print(f"Successfully extracted {target_filename}.")

            if extracted_files_count > 0:
                print(f"Successfully extracted {extracted_files_count} XML file(s) to {output_dir}: {', '.join(extracted_file_names)}")
                return True
            else:
                print("No XML files found in the ZIP archive.")
                return False

    except requests.exceptions.RequestException as e:
        print(f"Error downloading ZIP file: {e}")
        return False
    except zipfile.BadZipFile:
        print(f"Error: Downloaded file is not a valid ZIP archive or is corrupted.")
        return False
    except IOError as e:
        print(f"Error writing extracted file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and unzip PBS XML files.")
    parser.add_argument("--url", type=str, default=DEFAULT_PBS_URL,
                        help=f"URL of the PBS ZIP file. Defaults to: {DEFAULT_PBS_URL}")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR,
                        help=f"Directory to save the extracted XML files. Defaults to: {DEFAULT_OUTPUT_DIR} (project root relative to script).")

    args = parser.parse_args()

    if os.path.isabs(args.output_dir):
        normalized_output_dir = os.path.normpath(args.output_dir)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_output_dir = os.path.join(script_dir, args.output_dir)
        normalized_output_dir = os.path.normpath(resolved_output_dir)

    # Ensure the target directory exists
    if not os.path.exists(normalized_output_dir):
        print(f"Final output directory {normalized_output_dir} does not exist. Attempting to create it.")
        try:
            os.makedirs(normalized_output_dir, exist_ok=True)
            print(f"Successfully created output directory {normalized_output_dir}")
        except OSError as e:
            print(f"Critical Error: Could not create output directory {normalized_output_dir}: {e}")
            exit(1) # Exit if we can't create the target dir

    if download_and_unzip_pbs(args.url, normalized_output_dir):
        print("PBS download and extraction script finished successfully.")
    else:
        print("PBS download and extraction script encountered an error.")
