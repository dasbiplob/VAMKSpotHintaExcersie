from wsgiref.simple_server import make_server
import requests
import urllib.parse

def application(environ, start_response):
    # Parse the query string
    query_string = environ.get('QUERY_STRING', '')
    params = urllib.parse.parse_qs(query_string)

    # Check if font_size and next_hours are provided
    font_size = params.get('font_size', [None])[0]  # Get font size from parameters
    next_hours = params.get('next_hours', [None])[0]  # Get next hours from parameters

    # Prepare the HTTP response
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html; charset=utf-8')]
    
    if font_size and next_hours:  # If both parameters are provided
        # Prepare the URL for the API request
        url = f'https://api.spot-hinta.fi/Html/{font_size}/{next_hours}'

        try:
            # Make the API request
            response = requests.get(url, headers={'accept': 'text/html'})

            if response.status_code == 200:
                html_content = response.text
            else:
                html_content = f'Error: {response.status_code}, {response.text}'

        except Exception as e:
            html_content = f'An error occurred: {str(e)}'
        
        # Return the HTML content from the API response
        start_response(status, response_headers)
        return [html_content.encode('utf-8')]
    
    else:  # If parameters are not provided, show the input form
        form_html = generate_form()
        start_response(status, response_headers)
        return [form_html]

# HTML form to get user input for font size and next hours
def generate_form():
    return b"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Energy Price Input</title>
        </head>
        <body>
            <h1>Enter Font Size and Next Hours</h1>
            <form action="/" method="get">
                <label for="font_size">Font Size:</label>
                <input type="text" id="font_size" name="font_size" required>
                <br><br>
                <label for="next_hours">Next Hours:</label>
                <input type="number" id="next_hours" name="next_hours" min="1" required>
                <br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    """

# Create a server and run it
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, application)  # Bind to all interfaces
    print("Serving on http://localhost:8000...")
    server.serve_forever()
