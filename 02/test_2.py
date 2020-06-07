# import re
# my_str = '140\xa0000-220\xa0000 руб.'
# my_str = re.sub(r"[\xa0]", "", my_str)
# print(my_str)
# num1 = int(my_str[0:6])
# print(type(num1))
# print(num1)

text1 = '140\xa0000-220\xa0000 руб.'
text2 = 'от 110\xa0000 руб.'
text3 = 'до 150\xa0000 руб.'
text = text3.replace('\xa0', '')
print(text)
# num2 = int(text[0:6])
# print(type(num2))
# print(num2)

text = text.replace(' ', '-')
print(text)
text = text.split('-')
print(text)

if text[0] == 'от':
    salary_min = int(text[1])
    salary_max = None
    # a[2] = a[2]
elif text[0] == 'до':
    salary_min = None
    salary_max = int(text[1])
    # a[2] = a[2]
else:
    salary_min = int(text[0])
    salary_max = int(text[1])
salary_curr = text[2]
print(salary_max, salary_min, salary_curr)
