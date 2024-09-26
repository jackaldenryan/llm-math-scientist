from pylatex import Document, Package, NoEscape
from pylatex import Document, Package, Math, NoEscape
from pylatex.utils import NoEscape
import subprocess
import random
from visualization import *
from ops import *
import os


def generate_formula(num_prev_terms, num_values_tot, random_seed):
    random.seed(random_seed)
    possible_values = ["n"] + ["a_{n-" + str(i+1) + "}" for i in range(num_prev_terms)]

    possible_ops = {
        "unary": [
            # (square, square_latex),
            (add_1, add_1_latex),
            # (euler_totient, euler_totient_latex),
            (get_num_digits, get_num_digits_latex),
            (reverse_digits, reverse_digits_latex)
        ],
        "binary": [
            (add, add_latex),
            # (multiply, multiply_latex),
            (subtract, subtract_latex),
            # (mod, mod_latex)
        ],
        "ternary": [
            (max3, max3_latex),
            (min3, min3_latex)
        ],
    }

    # Choose num_values_tot values from possible_values at random with replacement
    values_abstract = random.choices(possible_values, k=num_values_tot)

    values = []
    for idx, val in enumerate(values_abstract):
        values.append({'name': val, 'value': val, 'latex': val})

    # The formula will be represented as a list of operations
    formula_ops = []

    tmp_counter = 0

    while len(values) > 1:
        # Randomly choose an operation type (unary, binary, ternary)
        op_types = []
        if len(values) >= 1:
            op_types.append("unary")
        if len(values) >= 2:
            op_types.append("binary")
        if len(values) >= 3:
            op_types.append("ternary")
        op_key = random.choice(op_types)
        op_category = possible_ops[op_key]

        # Among op category, choose random op
        op_func, op_latex = random.choice(op_category)

        if op_key == "unary":
            rand_idx1 = random.randint(0, len(values)-1)
            val1 = values.pop(rand_idx1)
            result_name = f"tmp{tmp_counter}"
            tmp_counter += 1
            result_value = f"{op_func.__name__}({val1['value']})"
            result_latex = op_latex(val1['latex'])
            values.append({'name': result_name, 'value': result_value, 'latex': result_latex})
            # Record operation in formula
            formula_ops.append(('unary', op_func, op_latex, val1['name'], result_name))
        elif op_key == "binary":
            rand_idx1, rand_idx2 = random.sample(range(len(values)), 2)
            val1 = values.pop(max(rand_idx1, rand_idx2))
            val2 = values.pop(min(rand_idx1, rand_idx2))
            result_name = f"tmp{tmp_counter}"
            tmp_counter += 1
            result_value = f"{op_func.__name__}({val1['value']}, {val2['value']})"
            result_latex = op_latex(val1['latex'], val2['latex'])
            values.append({'name': result_name, 'value': result_value, 'latex': result_latex})
            formula_ops.append(('binary', op_func, op_latex, val1['name'], val2['name'], result_name))
        elif op_key == "ternary":
            rand_idxs = random.sample(range(len(values)), 3)
            rand_idxs.sort(reverse=True)
            val_list = []
            for idx in rand_idxs:
                val_list.append(values.pop(idx))
            val1, val2, val3 = val_list
            result_name = f"tmp{tmp_counter}"
            tmp_counter += 1
            result_value = f"{op_func.__name__}({val1['value']}, {val2['value']}, {val3['value']})"
            result_latex = op_latex(val1['latex'], val2['latex'], val3['latex'])
            values.append({'name': result_name, 'value': result_value, 'latex': result_latex})
            formula_ops.append(('ternary', op_func, op_latex, val1['name'], val2['name'], val3['name'], result_name))

    final_result_name = values[0]['name']
    final_formula = values[0]['value']
    final_formula_latex = values[0]['latex']
    return formula_ops, final_result_name, final_formula, final_formula_latex


def apply_formula(n, seq, formula_ops, num_prev_terms):
    # Initial values mapping
    value_map = {}
    value_map["n"] = n
    for i in range(num_prev_terms):
        value_map[f"a_{{n-{i+1}}}"] = seq[-(i+1)]

    for op in formula_ops:
        if op[0] == 'unary':
            _, func, _, operand_name, result_name = op
            val = value_map[operand_name]
            result = func(val)
            value_map[result_name] = result
        elif op[0] == 'binary':
            _, func, _, operand1_name, operand2_name, result_name = op
            val1 = value_map[operand1_name]
            val2 = value_map[operand2_name]
            result = func(val1, val2)
            value_map[result_name] = result
        elif op[0] == 'ternary':
            _, func, _, operand1_name, operand2_name, operand3_name, result_name = op
            val1 = value_map[operand1_name]
            val2 = value_map[operand2_name]
            val3 = value_map[operand3_name]
            result = func(val1, val2, val3)
            value_map[result_name] = result
    # The final result is stored in the final_result_name
    final_result_name = list(value_map.keys())[-1]
    final_result = value_map[final_result_name]
    return final_result


def compute_seq(n_terms, random_seed, num_prev_terms, num_values_tot):

    # Create a basic init
    seq = [i for i in range(num_prev_terms)]

    # Generate the formula once
    formula_ops, final_result_name, final_formula_str, final_formula_latex = generate_formula(
        num_prev_terms, num_values_tot, random_seed)

    print("Generated formula: ", "$$ a_n = " + final_formula_latex + " $$")
    print("")

    while len(seq) < n_terms:
        current_n = len(seq)
        next_term = apply_formula(current_n, seq, formula_ops, num_prev_terms)
        seq.append(next_term)

    return seq, final_formula_latex, formula_ops


def gen_and_save_seq(n_terms, random_seed, num_prev_terms, num_values_tot, foldername, show_plot=False):

    subdirs = ["", "graphs", "formulas", "formulas/texs"]
    for subdir in subdirs:
        os.makedirs(os.path.join(foldername, subdir), exist_ok=True)

    seq, formula_latex, formula_ops = compute_seq(n_terms, random_seed, num_prev_terms, num_values_tot)

    filename = f"{n_terms}_{random_seed}_{num_prev_terms}_{num_values_tot}"

    # Create a LaTeX document
    doc = Document('article', page_numbers=False)
    doc.packages.append(Package('amsmath'))

    # Add the formula to the document
    doc.append(NoEscape(r'\['))
    doc.append(NoEscape(f"a_n = {formula_latex}"))
    doc.append(NoEscape(r'\]'))

    # Generate the PDF
    try:
        doc.generate_pdf(f"{foldername}/formulas/{filename}", clean_tex=True, clean=True, compiler='pdflatex')
        doc.generate_tex(f"{foldername}/formulas/texs/{filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")

    # Plotting the sequence
    plot_multiple_curves([seq], filename=f"{foldername}/graphs/{filename}.png", show_plot=show_plot)

    return seq, formula_latex, formula_ops


####################
# Generate several sequences
####################

# n_terms = 300
# num_prev_terms = 3
# num_values_tot = 10
# num_random_seeds = 100

# foldername = f"sequences/p{num_prev_terms}_v{num_values_tot}_t{n_terms}"

# for random_seed in range(num_random_seeds):

#     _, _, _, = gen_and_save_seq(n_terms, random_seed, num_prev_terms, num_values_tot, foldername, show_plot=False)


####################
# Plot an individual sequence
####################
# n_terms = 300
# num_prev_terms = 3
# num_values_tot = 10
# random_seed = 31
# foldername = "sequences/test"
# seq, formula_latex, formula_ops = gen_and_save_seq(
#     n_terms, random_seed, num_prev_terms, num_values_tot, foldername, show_plot=True)
