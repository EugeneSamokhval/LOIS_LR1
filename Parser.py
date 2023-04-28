import copy
import LogicOperatins

operators = ['*', '+', '!', '=', '@']

operation_priority = {"!": 5, '*': 4, '+': 3, '@': 2, '=': 1, '(': 0, ')': 0}


def starting_table_constructor(prebuilt_formula: str):
    list_of_variables = []
    for sign in prebuilt_formula:
        if sign.islower() or sign.isupper():
            list_of_variables.append(sign)
    list_of_variables = list(dict.fromkeys(list_of_variables))
    table_of_truth = [bin(counter) for counter in range(2 ** len(list_of_variables))]
    table_of_truth = [number.removeprefix('0b') for number in table_of_truth]
    table_of_truth = [[sign for sign in number] for number in table_of_truth]
    for sub_list in table_of_truth:
        while len(sub_list) != len(list_of_variables):
            sub_list.insert(0, '0')
    table_of_truth = [[int(sign) for sign in number] for number in table_of_truth]
    return table_of_truth, list_of_variables


class Formula:
    def __init__(self, formula_prototype: str):
        self.formula_pre_built = formula_prototype.strip(" ")
        self.starting_table, self.list_of_variables = starting_table_constructor(self.formula_pre_built)
        self.final_form = []

    def sub_formulas_creation(self):
        self.final_form = []
        stack = []
        for letter in self.formula_pre_built:
            if letter.islower() or letter.isupper():
                self.final_form.append(letter)
            elif letter in operators:
                if len(stack) != 0:
                    while operation_priority.get(letter) < operation_priority.get(stack[0]):
                        self.final_form.append(stack.pop(0))
                        if len(stack) == 0:
                            break
                stack.insert(0, letter)
            elif letter == "(":
                stack.insert(0, letter)
            elif letter == ")":
                while stack[0] != "(":
                    self.final_form.append(stack.pop(0))
                stack.pop(0)
        for rest in stack:
            self.final_form.append(rest)

    def function_fill_variables(self, variables: dict):
        counter = 0
        filled_with_variables = copy.deepcopy(self.final_form)
        while counter != len(filled_with_variables):
            if filled_with_variables[counter].islower() or filled_with_variables[counter].isupper():
                filled_with_variables[counter] = variables.get(filled_with_variables[counter])
            counter+=1
        return filled_with_variables

    def function_solution(self, filled_with_variables: list):
        stack = []
        for sign in filled_with_variables:
            if type(sign) == int:
                stack.insert(0, sign)
            elif sign in operators:
                if sign == "!":
                    stack[0] = LogicOperatins.logic_not(stack[0])
                elif sign == "@":
                    stack[0] = LogicOperatins.logic_then(stack[1], stack[0])
                    stack.remove(stack[1])
                elif sign == "=":
                    stack[0] = stack[1] == stack[0]
                elif sign == "*":
                    stack[0] = stack[1] and stack[0]
                elif sign == "+":
                    stack[0] = stack[1] or stack[0]
        return stack[0]

    def output_logic_list(self):
        ready_to_solve_form = []
        self.sub_formulas_creation()
        for situation in self.starting_table:
            variable_value_dictionary = {self.list_of_variables[iteration]: situation[iteration]
                                         for iteration in range(len(self.list_of_variables))}
            ready_to_solve_form.append(self.function_fill_variables(variable_value_dictionary))
        output_list = []
        for formula in ready_to_solve_form:
            output_list.append(self.function_solution(formula))
        return output_list, self.starting_table
