from mpmath import iv, ctx_iv    # type: ignore

iv.dps = 12
iv.pretty = True

def w(x: ctx_iv.ivmpf) -> ctx_iv.ivmpf:
    output = iv.fmul(iv.mpf('8'), x)                    # 8x
    output = iv.fadd(output, iv.mpf('1'))               # 8x + 1
    output = iv.sqrt(output)                            # sqrt(8x + 1)
    return output



def c(x: ctx_iv.ivmpf) -> ctx_iv.ivmpf:
    numerator = iv.fadd(w(x), iv.mpf('3'))              # w(x) + 3
    numerator = iv.fmul(numerator, numerator)           # (w(x) + 3)^2

    denominator = iv.mpf('16')                           # 16

    output = iv.fdiv(numerator, denominator)             # (w(x) + 3)^2 / 16
    return output



def d(x: ctx_iv.ivmpf) -> ctx_iv.ivmpf:
    numerator = iv.fadd(w(x), iv.mpf('3'))               # w(x) + 3
    numerator = iv.fmul(numerator, numerator)            # (w(x) + 3)^2

    denominator = iv.fadd(w(x), iv.mpf('1'))             # w(x) + 1
    denominator = iv.fmul(iv.mpf('8'), denominator)      # 8(w(x) + 1)

    output = iv.fdiv(numerator, denominator)             # (w(x) + 3)^2 / 8(w(x) + 1)
    return output



def s(x: ctx_iv.ivmpf) -> ctx_iv.ivmpf:
    numerator = iv.fsub(w(x), iv.mpf('1'))               # w(x) - 1
    numerator = iv.fmul(numerator, numerator)            # (w(x) - 1)^2

    denominator = iv.fadd(w(x), iv.mpf('7'))             # w(x) + 7
    denominator = iv.fmul(iv.mpf('4'), denominator)      # 4(w(x) + 7)
    
    output = iv.fdiv(numerator, denominator)             # (w(x) - 1)^2 / 4(w(x) + 7)
    return output



def s_inverse(x: ctx_iv.ivmpf) -> ctx_iv.ivmpf:
    numerator = iv.mpf('1')                              # 1
    denominator = s(iv.fdiv(iv.mpf('1'), x))             # s(1/x)
    output = iv.fdiv(numerator, denominator)             # 1 / s(1/x)
    return output



def s_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:
    output = x                                                                          # s_0 = x
    if i > 0:
        for _ in range(i):      # run i times
            output = s(output)                                                          # s_i = s(s_{i-1}(x)); i > 0
    elif i < 0:
        for _ in range(-i):     # run i times
            output = s_inverse(output)                                                  # s_i = s_{-1}(s_{i+1}(x)); i < 0
        
    if print_val:
        print(f's_{i} = {output}')

    return output



def c_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:
    output = c(s_i(x, i, print_val))                                                               # c_i = c(s_i(x))
    if print_val:
        print(f'c_{i} = {output}')

    return output



def d_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:
    output = d(s_i(x, i, print_val))                                                               # d_i = d(s_i(x))
    if print_val:
        print(f'd_{i} = {output}')
        
    return output



def P_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:              # i >= 0
    output = iv.mpf('1')                                                                # P_0 = 1
    if i == 0:
        return output
    
    for j in range(i):                                                                  # j = [0, 1, ..., i - 1]
        product = iv.mpf('1')
        for k in range(j + 1):                                                          # k = [0, 1, ..., j]
            new_product = iv.fsub(c_i(x, k, print_val), iv.mpf('1'))                    # c_k - 1
            product = iv.fmul(product, new_product)                                     # (c_0 - 1)(c_1 - 1)...(c_k - 1)

        output = iv.fadd(output, product)                                               # P_i = 1 + (c_0 - 1) + (c_0 - 1)(c_1 - 1) + ... + (c_0 - 1)(c_1 - 1)...(c_{i-1} - 1)

    if print_val:
        print(f'P_{i} = {output}\n')

    return output



def S_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:              # i >= 0
    output = iv.mpf('1')                                                                # S_0 = 1
    if i == 0:
        return output
    
    for j in range(i):                                                                  # j = [0, 1, ..., i - 1]
        product = iv.mpf('1')
        for k in range(j + 1):                                                          # k = [0, 1, ..., j]
            new_product = iv.fsub(d_i(x, k, print_val), iv.mpf('1'))                    # d_k - 1
            product = iv.fmul(product, new_product)                                     # (d_0 - 1)(d_1 - 1)...(d_k - 1)

        output = iv.fadd(output, product)                                               # S_i = 1 + (d_0 - 1) + (d_0 - 1)(d_1 - 1) + ... + (d_0 - 1)(d_1 - 1)...(d_{i-1} - 1)

    if print_val:
        print(f'S_{i} = {output}\n')

    return output



def Q_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:              # i >= 1
    output = iv.mpf('0')                                                                # Q_1 = 0
    if i == 1:
        return output
    
    for j in range(1, i):                                                               # j = [1, 2, ..., i - 1]
        product = iv.mpf('1')
        for k in range(1, j + 1):                                                       # k = [1, 2, ..., j]
            new_product = iv.fsub(c_i(x, -k, print_val), iv.mpf('1'))                   # (c_{-k} - 1)
            new_product = iv.fdiv(iv.mpf('1'), new_product)                             # (c_{-k} - 1)^{-1}
            product = iv.fmul(product, new_product)                                     # (c_{-1} - 1)(c_{-2} - 1)...(c_{-k} - 1)

        output = iv.fadd(output, product)                                               # Q_i = 0 + (c_{-1} - 1) + (c_{-1} - 1)(c_{-2} - 1) + ... + (c_{-1} - 1)(c_{-2} - 1)...(c_{-i+1} - 1)

    if print_val:
        print(f'Q_{i} = {output}\n')

    return output



def T_i(x: ctx_iv.ivmpf, i: int, print_val: bool = False) -> ctx_iv.ivmpf:              # i >= 1
    output = iv.mpf('0')                                                                # T_1 = 0
    if i == 1:
        return output
    
    for j in range(1, i):                                                               # j = [1, 2, ..., i - 1]
        product = iv.mpf('1')
        for k in range(1, j + 1):                                                       # k = [1, 2, ..., j]
            new_product = iv.fsub(d_i(x, -k, print_val), iv.mpf('1'))                   # (d_{-k} - 1)
            new_product = iv.fdiv(iv.mpf('1'), new_product)                             # (d_{-k} - 1)^{-1}
            product = iv.fmul(product, new_product)                                     # (d_{-1} - 1)(d_{-2} - 1)...(d_{-k} - 1)

        output = iv.fadd(output, product)                                               # T_i = 0 + (d_{-1} - 1) + (d_{-1} - 1)(d_{-2} - 1) + ... + (d_{-1} - 1)(d_{-2} - 1)...(d_{-i+1} - 1)

    if print_val:
        print(f'T_{i} = {output}\n')

    return output



def M_lk(x: ctx_iv.ivmpf, l: int, k: int, print_val: bool = False) -> ctx_iv.ivmpf:
    numerator = iv.fadd(S_i(x, k, print_val), T_i(x, l, print_val))                     # S_k + T_l
    numerator = iv.fmul(x, numerator)                                                   # x(S_k + T_l)

    denominator = iv.fadd(P_i(x, k, print_val), Q_i(x, l, print_val))                   # P_k + Q_l

    output = iv.fdiv(numerator, denominator)                                            # x(S_k + T_l) / (P_k + Q_l)

    if print_val:
        print(f'M_{l},{k} = {output}\n')

    return output



def M_lk_down(a: ctx_iv.ivmpf, b: ctx_iv.ivmpf, l: int, k: int, print_val: bool = False) -> ctx_iv.ivmpf:
    numerator = iv.fadd(S_i(a, k, print_val), T_i(b, l, print_val))                     # S_k(a) + T_l(b)
    numerator = iv.fmul(a, numerator)                                                   # a(S_k(a) + T_l(b))

    denominator = iv.fadd(P_i(b, k, print_val), Q_i(a, l, print_val))                   # P_k(b) + Q_l(a)

    output = iv.fdiv(numerator, denominator)                                            # a(S_k(a) + T_l(b)) / (P_k(b) + Q_l(a))

    if print_val:
        print(f'M_{l},{k}^down = {output}\n')

    return output
