some_list = [7, 14, 28, 32, 32, 56]
some_list = [7, 14, 28, 32, 32, '56']

def custom_filter(numbers):
    return sum(filter(lambda x: isinstance(x, int) and not x % 7, some_list)) < 84

print(custom_filter(some_list))
