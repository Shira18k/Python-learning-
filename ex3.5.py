
#1.
#def that return a dict of inf for a string s:
#{length , amount of english vowels , letter list, list of length's words}
def processes_text(s):
    if len(s) == 0:
        raise ValueError("Empty string")

    length = len(s)
    VOWELS = {'a', 'e', 'i', 'o', 'u'} #English vowels (a, e, i, o, u).
    # explain this method -  rather for char in s bla bla :
    #                               char - the exp that we need
    #                               for each char in s (the string)
    #                               and condition for adding = just if from the array VOWELS
    #                               (the uses of .lower - not ignore from letter vowels
    found_vowels_list = [char for char in s.lower() if char in VOWELS]
    amount_of_vowels = len(found_vowels_list)
    # a list of letters so we search a 'letter' in s and add to list if 'letter' is letter
    letter_list = [letter for letter in s if letter.isupper()]
    # a list of the word's length
    len_of_words_lengths = [len(word) for word in s.split()]

    dict = {}
    dict['length'] = length
    dict['amount_of_vowels'] = amount_of_vowels
    dict['letter_list'] = letter_list
    dict['len_of_words_lengths'] = len_of_words_lengths
    return dict
# check 1
print(processes_text(input("what is your string? ")))

#2.
#The function returns a list of strings where text appears "time" times
#Each appearance is wrapped with left and right, and the wrapped parts are separated by commas.
def repeat_frame(text, times=3, left='[', right=']'):
    word = left + text + right
    list_of_text = [word for _ in range(times)]
    return list_of_text
# check 2
print(repeat_frame("text", 3, "[","]")) #origin
print(repeat_frame("text", 5, "[","]")) #change time
print(repeat_frame("text", 3, "<",">")) #change framing characters

#3.
#fun that computes the sum of digits of a positive integer n
def digit_sum(n):
    if n < 0:
        raise ValueError("num is negative")

    digit_list = [int(char) for char in str(n)]
    print(digit_list)
    return sum(digit_list)

# a recursive function that returns how many times the digit d appears in n
def count_digit(n, d):
    if n < 0:
        raise ValueError("num is negative")

    if(n==0):
        return 0

    if(d == (n % 10)):
        return 1+count_digit(n //10 ,d)

    else:
        return count_digit(n // 10,d)

# checks 3
print(digit_sum(123))
print(count_digit(1000,0))


#4.
#helping function for recognized integer
def isDigit(s):
     try:
         int(s)
         return True

     except ValueError:
         return False

#get from the user list of integers
#check that the list contains only numbers
#return list with only the negative values
#return the max value from the list

integers_user= input("list of integers: ")
#creat a list from the input
integer_list = integers_user.split(" ")

good_integer_list = [s for s in integer_list if  isDigit(s)]
print(good_integer_list)
if len(good_integer_list) != len(integer_list):
    raise ValueError("There is a incorrect value, write a list again:( ")

negative_integers = [num for num in good_integer_list if int(num)<0]
print(negative_integers)

max_value = 0
for char in good_integer_list:
    if int(char) > max_value:
        max_value = int(char)

print(max_value)


