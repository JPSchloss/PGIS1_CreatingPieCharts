# Jonathan Schlosser
# Assignment 6 Chart Creation from JSON Data
# INLS 560 Fall 2019
# April 1, 2020

# The purpose of this program is to load character data from the Rick and Morty API
# (https://rickandmortyapi.com/documentation), to parse the loaded JSON file, and to
# create pie charts from the data of interest. In particular, this program identifes:
    # the number of characters per each species.
    # the genders of each of the characters
    # the number of characters from each origin location
    # and the number of characters shown at a location.

# The output of this program is four Google chart html files. They can be opened in a browser.

# Note: the program may take a minute to run as the api only delivers results one page at a time.
# To collect all the data, iterative API calls need to be conducted and processed and that can take a second.
# Also, the code should be more concise since the code repeats. If this is a problem, please let me know and
# I can work to fix it. I tried to keep the code as consistent with the demo as possible, because I thought
# that was expected. Rather than presenting drastic differences in the code. If I am wrong in this assumption,
# please let me know and I can correct it. And, as a fun note, the locations pie chart kinda looks like the portal
# from the show and I hoped that one of the charts would come out like that.

# Importing necessary packages.
import urllib.request
import urllib.error
from urllib.error import URLError, HTTPError
import json
import gviz_api
import webbrowser

# Calling the main function.
def main():
    # Calling a function to load the data and parse it into a usable form
    # which is then loaded to the appropriate variable.
    data = parse_rick_morty_characters()
    species_dict = data[0]
    gender_dict = data[1]
    origin_dict = data[2]
    location_dict = data[3]

    # Calling respective functions for the creation of the different charts.
    create_species_chart(species_dict)
    create_gender_chart(gender_dict)
    create_origin_chart(origin_dict)
    create_location_chart(location_dict)


# This function loads and parses the data.
def parse_rick_morty_characters():
    # Creating the dictionaries to store results for each chart.
    species_dict = {}
    gender_dict = {}
    origin_dict = {}
    location_dict = {}

    # Establishing control variables for the while loop.
    # "pages" start at one as it makes the most sense for the first call.
    pages = 1
    i = 1
    while i <= pages:
        # Including a try statement to handle errors and exceptions.
        try:
            # Setting the url and running the API call.
            url = "https://rickandmortyapi.com/api/character/?page="+str(i)
            load = urllib.request.urlopen(url).read().decode('utf8')

            # Parsing the json data, extracting and outputting information of interest
            load_dictionary = json.loads(load)

            # Placing results into variables.
            load_info = load_dictionary['info']
            load_results = load_dictionary['results']

            # Iterating over the results and putting the information into variables.
            for result in load_results:
                speciesType = result['species']
                gender = result['gender']
                origin = result['origin']['name']
                location = result['location']['name']

                # For each variable, if it is in the appropriate dictionary,
                # the frequency is increased, if not, the frequency is initiated at 1.
                if speciesType not in species_dict:
                    species_dict[speciesType] = 1
                else:
                    species_dict[speciesType] += 1

                if gender not in gender_dict:
                    gender_dict[gender] = 1
                else:
                    gender_dict[gender] += 1

                if origin not in origin_dict:
                    origin_dict[origin] = 1
                else:
                    origin_dict[origin] += 1

                if location not in location_dict:
                    location_dict[location] = 1
                else:
                    location_dict[location] += 1

            # Updating the loop info - since pages is in the infor from the search,
            # and doesnt change from page to page, it is employed, but this would not be
            # stable for an API call that varied that result.
            pages = load_info['pages']
            i += 1

        # Exception handlers.
        except ValueError as err:
            print('An error occurred trying to decode the json text')
            print(err)
        except HTTPError as err:
            print('Server could not fulfill the request.')
            print(err)
        except URLError as err:
            print('Failed to reach a server.')
            print(err)
        except Exception as err:
            print('An error occurred: ', err)
        except IndexError:
            continue

    # Returning each of the dictionaries created. All have a general {term: frequency} form.
    return species_dict, gender_dict, origin_dict, location_dict


# Defining the function to create the pie chart representing the frequencies of each species.
def create_species_chart(species_dict):
    # Setting the html and javascript template for the google chart.
    species_piechart_template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = new google.visualization.DataTable(%(species_json_text)s);

            var options = {
              title: 'Character Species in Rick and Morty',
              colors: ["#65C1E8", "#69ad53", "#314e1c", "#365829", "#c7fa6c", "#62a4ab"]
            };

            var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="chart_div" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """
    # Setting the description for the data.
    species_description = [("Species", "string"), ("Frequency", "number")]

    try:
        # Creating key, value tuples for each row in the data
        species_data = []

        for key, value in species_dict.items():
            species_data.append((key, value))
    except KeyError as err:
        print(err)
    except Exception as err:
        print(err)

    # Creating the data table object from the description and tuples.
    species_data_table = gviz_api.DataTable(species_description)
    species_data_table.LoadData(species_data)

    # Converting to JSON - called in the html template.
    species_json_text = species_data_table.ToJSon()

    # Setting the output filename.
    filename = 'species_piechart.html'

    #Creating the chart and html file.
    try:
        # Creating the HTML file
        html_file = open(filename, 'w', encoding='utf8')

        # Writing the pie chart template and substituting in the JSON text
        html_file.write(species_piechart_template % vars())

        # Opening the HTML file in a browser
        webbrowser.open_new_tab(filename)

        # Closing the file
        html_file.close()

    # Exception handlers.
    except ValueError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except OSError as err:
        print(err)
    except Exception as err:
        print(err)

def create_gender_chart (gender_dict):
    # Setting the html and javascript template for the google chart.
    gender_piechart_template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = new google.visualization.DataTable(%(gender_json_text)s);

            var options = {
              title: 'Genders of the Characters in Rick and Morty',
              colors: ["#65C1E8", "#69ad53", "#314e1c", "#365829", "#c7fa6c", "#62a4ab"]
            };

            var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="chart_div" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """
    # Setting the description for the data.
    gender_description = [("Gender", "string"), ("Frequency", "number")]

    try:
        # Creating key, value tuples for each row in the data
        gender_data = []

        for key, value in gender_dict.items():
            gender_data.append((key, value))
    except KeyError as err:
        print(err)
    except Exception as err:
        print(err)


    # Creating the data table object from the description and tuples.
    gender_data_table = gviz_api.DataTable(gender_description)
    gender_data_table.LoadData(gender_data)

    # Converting to JSON - called in the html template.
    gender_json_text = gender_data_table.ToJSon()

    # Setting the output filename.
    filename = 'gender_piechart.html'

    # Creating the chart and html file.
    try:
        # Creating the HTML file
        html_file = open(filename, 'w', encoding='utf8')

        # Writing the pie chart template and substituting in the JSON text
        html_file.write(gender_piechart_template % vars())

        # Opening the HTML file in a browser
        webbrowser.open_new_tab(filename)

        # Closing the file
        html_file.close()

    # Exception handlers.
    except ValueError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except OSError as err:
        print(err)
    except Exception as err:
        print(err)

def create_origin_chart (origin_dict):
    # Setting the html and javascript template for the google chart.
    origin_piechart_template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = new google.visualization.DataTable(%(origin_json_text)s);

            var options = {
              title: 'Origins of the Characters in Rick and Morty',
              colors: ["#65C1E8", "#69ad53", "#314e1c", "#365829", "#c7fa6c", "#62a4ab"]
            };

            var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="chart_div" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """
    # Setting the description for the data.
    origin_description = [("Origin", "string"), ("Frequency", "number")]

    try:
        # Creating key, value tuples for each row in the data
        origin_data = []

        for key, value in origin_dict.items():
            origin_data.append((key, value))
    except KeyError as err:
        print(err)
    except Exception as err:
        print(err)

    # Creating the data table object from the description and tuples.
    origin_data_table = gviz_api.DataTable(origin_description)
    origin_data_table.LoadData(origin_data)

    # Converting to JSON - called in the html template.
    origin_json_text = origin_data_table.ToJSon()

    # Setting the output filename.
    filename = 'origin_piechart.html'

    # Creating the chart and html file.
    try:
        # Creating the HTML file
        html_file = open(filename, 'w', encoding='utf8')

        # Writing the pie chart template and substituting in the JSON text
        html_file.write(origin_piechart_template % vars())

        # Opening the HTML file in a browser
        webbrowser.open_new_tab(filename)

        # Closing the file
        html_file.close()

    # Exception handlers.
    except ValueError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except OSError as err:
        print(err)
    except Exception as err:
        print(err)


def create_location_chart (location_dict):
    # Setting the html and javascript template for the google chart.
    location_piechart_template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = new google.visualization.DataTable(%(location_json_text)s);

            var options = {
              title: 'Locations Rick and Morty Characters',
              colors: ["#65C1E8", "#69ad53", "#314e1c", "#365829", "#c7fa6c", "#62a4ab"]
            };

            var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="chart_div" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """
    # Setting the description for the data.
    location_description = [("Location", "string"), ("Frequency", "number")]

    try:
        # Creating key, value tuples for each row in the data
        location_data = []

        for key, value in location_dict.items():
            location_data.append((key, value))
    except KeyError as err:
        print(err)
    except Exception as err:
        print(err)


    # Creating the data table object from the description and tuples.
    location_data_table = gviz_api.DataTable(location_description)
    location_data_table.LoadData(location_data)

    # Converting to JSON - called in the html template.
    location_json_text = location_data_table.ToJSon()

    # Setting the output filename.
    filename = 'location_piechart.html'

    # Creating the chart and html file.
    try:
        # Creating the HTML file
        html_file = open(filename, 'w', encoding='utf8')

        # Writing the pie chart template and substituting in the JSON text
        html_file.write(location_piechart_template % vars())

        # Opening the HTML file in a browser
        webbrowser.open_new_tab(filename)

        # Closing the file
        html_file.close()

    # Exception handlers.
    except ValueError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except OSError as err:
        print(err)
    except Exception as err:
        print(err)


main()

