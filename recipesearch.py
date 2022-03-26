import requests

def get_base_url(ingredient):      # outputs URL with one ingredient as the search key
  app_id = 'f868acd1'
  app_key = '1c379b64acd134e8937938ba61367db9'
  base_url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}&field=label&field=ingredients&field=uri&field=calories&field=healthLabels'
  return base_url

def get_exclusion_parameters():     # prompts user to input food items to exclude from the search, splits inputted
                                    # string into a list, then converts list to properly formatted string to add
                                    # onto end of the search URL (formatted as "&excluded={food_item}" ). If no
                                    # input is given, prints "No ingredients excluded from search" and returns
                                    # original URL

  check = input("★ Ingredients to Exclude ★\n\nPlease input ingredients you wish to exclude from search results, separated by commas. Otherwise, press enter: \n")
  if len(check) >= 1:
    exclusion_lst = check.strip().split(',')
    exclusion_string = "&excluded=" + "&excluded=".join(str(food_item).strip() for food_item in exclusion_lst)
    return exclusion_string
  else:
    print("No ingredients excluded from search")
    return None


def get_dietary_requirements():               # asks user to enter any dietary requirements
  example_reqs = ["vegan", "vegetarian", "gluten-free", "alcohol-free"]
  diet_reqs = input(f"Do you have any dietary requirements? Please choose from the following options, or type 'N' if none...\n{example_reqs}: ")
  while (diet_reqs != "N" and diet_reqs != "n") and (diet_reqs not in example_reqs):
    diet_reqs = input(
        f"Invalid response. Choose your dietary requirement from the following options, or type 'N' if none...\n{example_reqs}: ")
    diet_reqs_count = 0
  if diet_reqs == 'N' or diet_reqs == 'n':
      diet_reqs_count = 0
  elif diet_reqs in example_reqs:
      include_reqs = '&health={}'.format(diet_reqs)
      diet_reqs_count = 1
  return include_reqs

def get_results(url):                              # creates JSON object from search results
  result = requests.get(url)
  data = result.json()
  return data

def get_calorie_count(hit: str) -> int:            # returns integer with total calorie count for each recipe in results          
  calories = hit.get('recipe').get('calories')
  if calories is None:
    return None
  return int(calories)

def print_results(res):
  print("Search Results: \n\n")

  for hit in res.get('hits'):
    print("\n\n★", hit['recipe']['label'].upper(), "★", "\n")  # retreives and prints recipe title

    if get_calorie_count(hit) != None:                          # calls get_calorie count() 
      print("\n➤", str(get_calorie_count(hit)), "calories")    # and prints calorie count
    else:                                                       # or message if not found
      print("No calorie count available")

    print("\n─── Ingredients ───")
    ingred_list = []                                            # Adds ingredients to list,
    for ingred in hit['recipe']['ingredients']:                 # excluding duplicates
      if ingred['text'] not in ingred_list:
        ingred_list.append(ingred['text'])
    
    for ingred_text in ingred_list:                             # Prints ingredients
      print(ingred_text)

    print("\n─── Health Labels ───")
    h_labels = enumerate(hit['recipe']['healthLabels'])         # Retreives health labels, enumerates,
    for i, hl in h_labels:                                      # prints without newline, and adds newline
      print(" ✓ ",hl, end='')                                   # after every sixth health label
      if i % 6 == 5:
        print("\n", end='')
  return

def run():                                          # executes program
  ingredient = input('Enter an ingredient: ')

  base_url = get_base_url(ingredient)            
  exclusions = get_exclusion_parameters()
  if exclusions != None:                            # if get_exclusion_parameters() has returned None,
    url = base_url + exclusions                     # assign the unaltered base url to the url variable.
  else:                                             # if get_exclusion_parameters() has returned a string with
    return url                                      # food items to be excluded), concatenate base url with exclusion string.

  d_reqs = get_dietary_requirements()               # if get_dietary_requirements() has returned None,
  if d_reqs != None:                                # assign the unaltered base url to the url variable.
    url = url + d_reqs                              # if get_dietary_requirements() has returned a string with
  else:                                             # dietary requirements, concatenate current url with dietary requirements parameter
    return url

  results = get_results(url)

  print_results(results)

  show_more = input("\nEnter 'y' to show more results or any other character to exit\n")  # Gets URL for next 20
  while show_more == 'y':                                                             # results, passes it through
    next_url = results.get('_links').get('next').get('href')                          # get_results(), then passes JSON
    next_results = get_results(next_url)                                              # through get_results(). Keeps asking
    results = next_results                                                            # until 'y' is not inputted
    print_results(results)
    show_more = input("\nEnter 'y' to show more results or any other character to exit\n")

run()
