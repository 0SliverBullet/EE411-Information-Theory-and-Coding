import numpy as np
from scipy.optimize import minimize_scalar

# 定义目标函数
def target_function(x):
    return (1 - 0.5 * x) * np.log2(1 - 0.5 * x) +0.5 * x * np.log2(0.5 * x) + x

# 在[0, 1]范围内寻找最大值
result = minimize_scalar(target_function, bounds=(0, 1), method='bounded')

# 输出结果
if result.success:
    max_value = -result.fun  # 取负号是因为我们要找最大值，而minimize_scalar寻找最小值
    arg_max = result.x
    print(f"在区间[0, 1]中, C最大值为 {max_value:.4f}, 取得最大值的x值为 {arg_max:.4f}")
else:
    print("优化过程失败")

