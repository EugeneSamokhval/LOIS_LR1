import copy
import Parser


def complicated_binary_formula_divider(to_divide: str):
    first_subformula = ''
    open_commas_count = 1
    binary_operator = ''
    for letter in range(1, len(to_divide)-1):
        if to_divide[letter] == '(':
            open_commas_count+=1
        elif to_divide[letter] == ')':
            open_commas_count-=1
        elif to_divide[letter] in ['@', '!', '*', '=', '+'] and open_commas_count == 1:
            binary_operator += to_divide[letter]
            break
        first_subformula+=to_divide[letter]
    second_subformula = copy.deepcopy(to_divide).removeprefix('('+first_subformula+binary_operator)
    second_subformula = second_subformula.removesuffix(')')
    return first_subformula, second_subformula, binary_operator


def complicated_unary_formula_divider(to_divide: str):
    striper = copy.deepcopy(to_divide).removeprefix('(!')
    striper = striper.removesuffix(')')
    return striper, '!'


class Checkout:
    def __init__(self, user_input: str):
        self.input = user_input
        self.possible_signs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.operations = ['@', '!', '*', '=', '+', '(', ')']
        self.logic_constant = ['1', '0']

    def is_formula(self, to_check):
        return to_check in self.logic_constant or self.is_atomic(to_check) or self.is_complicated(to_check)

    def is_complicated(self, to_check):
        return self.is_unary_complicated(to_check) or self.is_binary_complicated(to_check)

    def is_atomic(self, to_check: str):
        return to_check in self.possible_signs or to_check in self.logic_constant

    def is_unary_complicated(self, to_check: str):
        stripped = copy.deepcopy(to_check)
        stripped = stripped.removeprefix('(!')
        stripped = stripped.removesuffix(')')
        return to_check[0] == '(' and to_check[1] == '!'\
            and self.is_formula(stripped) and to_check[len(to_check)-1] == ')' and\
            not self.is_binary_complicated(to_check)

    def is_binary_complicated(self, to_check):
        check_box = [False for iteration in range(5)]
        first_subformula, second_subformula, action = complicated_binary_formula_divider(to_check)
        if to_check[0] == '(':
            check_box[0] = True
        if to_check[len(to_check)-1] == ')':
            check_box[4] = True
        if self.is_formula(first_subformula) and self.is_formula(second_subformula):
            check_box[1], check_box[3] = True, True
        if action in self.operations:
            check_box[2] = True
        return check_box.count(True) == len(check_box)

    def check_result(self):
        return self.is_formula(self.input)


class Solution:
    def __init__(self, description: Checkout):
        self.object_description = description
        self.all_subformulas = []

    def subformulas_search(self):
        recursive_search(self.object_description.input, self)
        print(self.all_subformulas)
        for subformula in self.all_subformulas:
            subformula_index = self.all_subformulas.index(subformula)
            temp_solver = Parser.Formula(subformula)
            solutions, table_of_truth = temp_solver.output_logic_list()
            print(subformula_index, ')', machine_into_optimized(subformula), ':', solutions.count(1) == len(solutions))


def recursive_search(to_find: str, where_to_add: Solution):
    descrption = Checkout(to_find)
    if descrption.is_atomic(to_find):
        where_to_add.all_subformulas.append(to_find)
    elif descrption.is_binary_complicated(to_find):
        where_to_add.all_subformulas.append(to_find)
        first_subformula, second_subformula, sign = complicated_binary_formula_divider(to_find)
        recursive_search(first_subformula, where_to_add)
        recursive_search(second_subformula, where_to_add)
    elif descrption.is_unary_complicated(to_find):
        where_to_add.all_subformulas.append(to_find)
        subformula, sign = complicated_unary_formula_divider(to_find)
        recursive_search(subformula, where_to_add)


def optimized_into_machine(optimized: str):
    iterator = 0
    machine = ''
    while iterator < len(optimized):
        if optimized[iterator] == "\\":
            machine += "+"
            iterator += 1
        elif optimized[iterator] == "/":
            machine += "*"
            iterator += 1
        elif optimized[iterator] == "-":
            machine += "@"
            iterator+=1
        elif optimized[iterator] == "~":
            machine += "="
        else:
            machine += optimized[iterator]
        iterator+=1
    return machine


def machine_into_optimized(machine: str):
    optimised = ''
    for letter in machine:
        if letter == "+":
            optimised += '\\/'
        elif letter == '*':
            optimised += '/\\'
        elif letter == '@':
            optimised += '->'
        elif letter == '=':
            optimised += '~'
        else:
            optimised += letter
    return optimised


def main():
    user_input = ''
    while user_input != 'exit':
        user_input = input()
        machine_logic_formula = optimized_into_machine(user_input)
        is_correct = Checkout(machine_logic_formula)
        if not is_correct.check_result():
            print('Введённая формула не фвляется формулой языка логики высказываний')
        else:
            solve = Solution(is_correct)
            solve.subformulas_search()


if __name__ == "__main__":
    main()
