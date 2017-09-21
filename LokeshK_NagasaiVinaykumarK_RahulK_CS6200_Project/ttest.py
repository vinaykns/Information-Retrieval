import math
from scipy import stats

def t_test(base_file, to_compare_file, result_file_name):
    f_result = open(result_file_name, 'w')

    data_a = {}
    f_base = open(base_file, 'r')  # A
    content = f_base.readlines()
    for each_line in content:
        data = each_line.split()
        data_a[int(data[0])] = float(data[1])
    f_base.close()

    data_b = {}
    f_compare = open(to_compare_file, 'r')  # B
    content = f_compare.readlines()
    for each_line in content:
        data = each_line.split()
        data_b[int(data[0])] = float(data[1])
    f_compare.close()

    b_minus_a = []
    for i in range(64):
        try:
            b_minus_a.append(data_b[i] - data_a[i])
        except KeyError:
            continue

    # sigma calculation
    x_mean = float(sum(b_minus_a)) / len(b_minus_a)

    sigma_ab = sum([(x-x_mean)**2 for x in b_minus_a])

    sigma_ab = sigma_ab ** (0.5)

    t_value = (x_mean / sigma_ab) * len(b_minus_a)
    p_value = stats.t.sf(t_value, len(b_minus_a))

    f_result.write("t-value = " + str(t_value) + '\n')
    f_result.write("p-value = " + str(p_value))
    f_result.close()