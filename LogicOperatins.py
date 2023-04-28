
def logic_not(variable):
    if variable == 1:
        return 0
    else:
        return 1


def logic_then(first_variable: int, second_variable: int):
    if first_variable and not second_variable:
        return 0
    else:
        return 1
