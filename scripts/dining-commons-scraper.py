from bs4 import BeautifulSoup
import pandas as pd
import requests


dc_url_prefix = 'https://housing.ucdavis.edu/dining/menus/dining-commons/'
dining_commons = ['cuarto', 'tercero', 'segundo']


def get_menu(tb):
  """
  Returns a list of dictionaries which are food menu items with attributes
  """
  menu = []
  newItem = {
    "Name": ""
  }

  curLocation = ""  # some dont have any location
  curFilters = []  # some dont have any filters

  for line in tb.find_all():
    if line.name == 'h3':
      curDate = line.text
    elif line.name == 'h4':
      curMealTime = line.text
    elif line.name == 'h5':
      curLocation = line.text
    elif line.name == 'img':
      curFilters.append(line.get('alt'))
    elif line.name == "span":
      if newItem["Name"] != '':
        # adds a new item everytime you hit a span and the name is not empty
        menu.append(newItem)

      curFilters = []  # some dont have any filters

      newItem = {
        "Name": ""
      }

      newItem["Name"] = line.text
      newItem["Filters"] = curFilters
      newItem["Date"] = curDate
      newItem["Mealtime"] = curMealTime
      newItem["Location"] = curLocation
      state = "Description"
    elif line.name == 'p':
      newItem[state] = line.text.strip(':[]')
      state = "N/A"
    elif line.name == 'h6':
      state = line.text

  menu.append(newItem)
  return(menu)


if __name__ == "__main__":
  for dc in dining_commons:
    response = requests.get(dc_url_prefix + dc)

    soup = BeautifulSoup(response.content, 'html.parser')
    tabs = soup.find("div", {"id": "tabs"})

    days = []
    for tab in tabs.find_all("div", recursive=False):  # breakfast, lunch, dinner
      days.append(tab)

    # TODO: function to obtain induvidual day manus
    items = []  # index corresponds to days of the week
    for day in days:
      items.append(get_menu(day))

    dfs = []
    for i in items:
      dfs.append(pd.DataFrame.from_dict(i))

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(f'./data/{dc}-menu.csv')
