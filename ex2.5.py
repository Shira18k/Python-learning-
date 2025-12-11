"""1-
this part get a logline and return the information by a list """

user_logLine = input("the information is: ")
user_list = user_logLine.split()

location = user_list[-1]
IP = user_list[-2]

#the middle of the list(the velues from index 2 include undex 6)
middle_list = user_list[2:7]
#from middle just values in format :"-:-"
values_list = middle_list[1:]

#after
couple_list = []

for item in values_list:

  # for cases like "User:moshe-m-ofer" we will get "[User, moshe-m-ofer]"
  key, value = item.split(':', 1)
  # for cases like "moshe-m-ofer" we will get "moshe m ofer"
  cleaned_value = value.replace('-', ' ')
  couple_list.append((key, cleaned_value))

#just add IP and Location to the couple_list
key, value = IP.split(':', 1)
couple_list.append((key, value))
key, value = location.split(':', 1)
cleaned_value = value.replace('-', ' ')
couple_list.append((key, cleaned_value))

print("output: ")
#loop on the (key, value)
for key, value in couple_list:
    print(f"{key} = {value}")


"""2-
this part get list of hits and return tuple that including: 
how much hits in total, average and the max hit of the list"""

def analyze_damage(hits: list[int]) -> tuple[int, float, int]:
    # TODO: compute total, average, and max; return them as a tuple
    total = sum(hits)

    if len(hits) == 0:
        average = 0.0  # float
    else:
        average = total / len(hits)

    max_hit = max(hits)

    # example return: return total, average, maximum
    return total, average, max_hit


def demo_damage():
    # more useful - #user_damageList = input("the damages are: ")

    hits = [10, 45, 90, 12, 70, 83]
    # TODO: call analyze_damage and unpack result
    total, avg, max_val = analyze_damage(hits)
    # TODO: print the report line
    print(f"Total: {total}, Avg: {avg}, Max: {max_val}")
    # Comment: in Java I would probably ...


print(demo_damage())

# the last part is if coding on pyton system

##cool gadget , if we want a short float we can add in the print level ".1f" it will do it

"""3-
this part get a set of visitors and set of premium_users and check some information between them"""

from enum import unique
# Creat a new empty set named "visitors"
# Add list of the visitors ID's (I want to do it general so i will ask from the ueser)
# Print how many unique visitors the site had (diffrences)

visitors = set()
visitors_ID = input("the visetors ID's: ")

visitors_ID_check = visitors_ID.split(',')
#for checking
print(visitors_ID_check)

for item in visitors_ID_check:
    ID_as_int = int(item.strip())
    visitors.add(ID_as_int)
#for checking
print(visitors)

#add ignore from duplication so the length of the set is the answer for the unick visitors
print(f"{len(visitors)} is the num of the unique visitors")

# Creat a new empty set named "premium_users"
# Print:
#       1.how much in common between the setחs
#       2.how much in "visitors" and not in "premium_users"

premium_users = set()
premium_users_list = input("the premium_users: ")
premium_users_check = premium_users_list.split(',')
#for checking
print(premium_users_check)

for item in premium_users_check:
    premium_users_int = int(item.strip())
    premium_users.add(premium_users_int)
#for checking
print(premium_users)

#1.
print(visitors & premium_users)
#2.
print(visitors - premium_users)

"""4-
this part get a list of dicts and get value and return which dicts contains the tag
the steps are:
1. create filter fun that check which part in the dict contains "tag"
2. use the fun with the dict from the Ex2.5 """


def list_contains_tag(products: list[dict], tag: str) -> list[dict]:
    # new list that will return with the dicts that contains the "tag"
    filtered_products = []
    for product in products:
        # checking if dict contains "tag" -if y - add to the list
        if tag in product["tags"]:
            filtered_products.append(product)
    # return
    return filtered_products

#products_list = input("the products list: ")
products = [
    {"name": "Tea", "price": 12.5, "tags": {"drink", "hot"}},
    {"name": "Apple", "price": 3.0, "tags": {"fruit", "food"}},
]

results = list_contains_tag(products, "drink")
print(results)






