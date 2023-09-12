def butlast(mylist):
    """Like butlast in Lisp; returns the list without the last element."""
    return mylist[:-1]  # This returns a copy of mylist


def remove_last_item(mylist):
    """Removes the last item from a list"""
    mylist.pop(-1)  # This modifies mylist


list = ["A", "B", "C"]

# This function returns the modified copy of the list
new_list = butlast(list)

# Printing the modified copy returned by the function
print(new_list)
print(list)  # The original list is not modified

# This function modifies the list passed to it
remove_last_item(list)

# Printing the list after it is modified
print(list)
