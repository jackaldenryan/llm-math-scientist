
def square(x):
    return x * x


def square_latex(x):
    return f"({x})^2"


def add_1(x):
    return x + 1


def add_1_latex(x):
    return f"({x} + 1)"


def get_num_digits(x):
    return len(str(abs(int(x))))


def get_num_digits_latex(x):
    return f"\\text{{num\_digits}}({x})"


def reverse_digits(x):
    s = str(abs(int(x)))
    s_rev = s[::-1]
    return int(s_rev) if x >= 0 else -int(s_rev)


def reverse_digits_latex(x):
    return f"\\text{{reverse}}({x})"


def euler_totient(x):
    result = x
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            while x % i == 0:
                x //= i
            result *= (1 - (1 / i))
    if x > 1:
        result *= (1 - (1 / x))
    return int(result)


def euler_totient_latex(x):
    return f"\\phi({x})"


def add(x, y):
    return x + y


def add_latex(x, y):
    return f"({x} + {y})"


def multiply(x, y):
    return x * y


def multiply(x, y):
    return f"({x} \\times {y})"


def subtract(x, y):
    return x - y


def subtract_latex(x, y):
    return f"({x} - {y})"


def mod(x, y):
    return x % y if y != 0 else 0


def mod_latex(x, y):
    return f"({x} \\bmod {y})"


def max3(x, y, z):
    return max(x, y, z)


def max3_latex(x, y, z):
    return f"\\max({x}, {y}, {z})"


def min3(x, y, z):
    return min(x, y, z)


def min3_latex(x, y, z):
    return f"\\min({x}, {y}, {z})"
