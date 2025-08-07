import requests
from bs4 import BeautifulSoup

def decode_unicode_grid(doc_url):
    # Fetch the content of the published Google Doc
    response = requests.get(doc_url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the data
    table = soup.find('table')
    if not table:
        print("No table found in the document.")
        return

    # Extract rows from the table, skipping the header
    rows = table.find_all('tr')[1:]  # Skip header row

    # Parse the data into a list of (x, y, char) tuples
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 3:
            continue  # Skip malformed rows
        try:
            x = int(cols[0].get_text(strip=True))
            char = cols[1].get_text(strip=True)
            y = int(cols[2].get_text(strip=True))
            data.append((x, y, char))
        except ValueError:
            continue  # Skip rows with invalid integer values

    if not data:
        print("No valid data found in the table.")
        return

    # Determine the size of the grid
    max_x = max(x for x, y, ch in data)
    max_y = max(y for x, y, ch in data)

    # Initialize the grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Populate the grid with characters
    for x, y, ch in data:
        grid[y][x] = ch

    # Print the grid row by row
    for row in grid:
        print(''.join(row))

# Example usage
doc_url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
decode_unicode_grid(doc_url)
