import requests
import os

# --- Configuration ---
TARGET_URL = "https://05command.wikidot.com/tech-hub-tag-list"
OUTPUT_FILENAME = "en_source.html"
REQUEST_TIMEOUT = 15  # seconds (connection and read)
USER_AGENT = "TagMappingBot/1.0 (Learning exercise; +http://example.com/contact)" # Be polite - customize if you have a contact page

# --- Main Logic ---
def fetch_and_save_content(url, filename, timeout, headers):
    """
    Fetches content from a URL and saves it to a local file.

    Args:
        url (str): The URL to fetch.
        filename (str): The path to save the HTML content.
        timeout (int): Request timeout in seconds.
        headers (dict): Dictionary of request headers (e.g., for User-Agent).
    """
    print(f"Attempting to fetch content from: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        # Check for HTTP errors (4xx or 5xx)
        response.raise_for_status() # Raises an HTTPError if the status is 4xx or 5xx

        print(f"Successfully fetched content (Status code: {response.status_code}).")
        # requests usually detects encoding well, response.text provides decoded string
        html_content = response.text

        # Save the content to a file using UTF-8 encoding
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Content successfully saved to: {os.path.abspath(filename)}")
        except IOError as e:
            print(f"Error: Failed to write content to file '{filename}'. Reason: {e}")

    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds.")
    except requests.exceptions.HTTPError as e:
        # Error already raised by raise_for_status()
        print(f"Error: HTTP Error occurred: {e}")
    except requests.exceptions.RequestException as e:
        # Catch other potential errors (DNS failure, connection refused, etc.)
        print(f"Error: An error occurred during the request: {e}")
    except Exception as e:
        # Catch any other unexpected errors during processing
        print(f"An unexpected error occurred: {e}")

# --- Execution ---
if __name__ == "__main__":
    request_headers = {'User-Agent': USER_AGENT}
    fetch_and_save_content(TARGET_URL, OUTPUT_FILENAME, REQUEST_TIMEOUT, request_headers)