
import numpy as np

def objective(x):
    # if x[0] + x[1] == 0:
    #     return np.inf
    # else:
    return ((x[0]*np.log2(1/x[0])+(1-x[0])*np.log2(1/(1-x[0]))))/(x[0]+1)
    #return (x[0]*(x[1]*np.log2(1/x[1])+(1-x[1])*np.log2(1/(1-x[1]))) + x[1]*(x[0]*np.log2(1/x[0])+(1-x[0])*np.log2(1/(1-x[0]))))/(x[0]+x[1])

def differential_evolution(objective, bounds, population_size, max_generations, F, CR):
    # 初始化种群
    population = np.random.uniform(bounds[0][0], bounds[0][1], (population_size, len(bounds)))
    print(population)
    
    # 迭代进化
    for i in range(max_generations):
        # 遍历种群中的每个个体
        for j in range(population_size):
            # 随机选择三个个体作为变异向量
            candidates = [index for index in range(population_size) if index != j]
            a, b, c = population[np.random.choice(candidates, 3, replace=False)]
            
            # 生成变异向量
            mutant = np.clip(a + F * (b - c), bounds[0][0], bounds[0][1])
            
            # 生成交叉向量
            cross_points = np.random.rand(len(bounds)) < CR
            
            trial = np.where(cross_points, mutant, population[j])
        
            # 评估目标函数值
            obj_value = objective(population[j])
            trial_value = objective(trial)
            


            # 更新个体
            if trial_value > obj_value:
                population[j] = trial
    
    # 返回最优解
    best_index = np.argmax([objective(individual) for individual in population])
    best_solution = population[best_index]
    best_fitness = objective(best_solution)
    
    return best_solution, best_fitness

# 设置参数和变量范围
bounds = [(0.1, 0.9), (0.1, 0.9)]
population_size = 40
max_generations = 2000
F = 0.5
CR = 0.7

# 求解最优解
best_solution, best_fitness = differential_evolution(objective, bounds, population_size, max_generations, F, CR)

# 输出结果
# print((0.5*(0.5*np.log2(1/0.5)+(1-0.5)*np.log2(1/(1-0.5))) + 0.5*(0.5*np.log2(1/0.5)+(1-0.5)*np.log2(1/(1-0.5))))/(0.5+0.5))
# print((0.4*(0.4*np.log2(1/0.4)+(1-0.4)*np.log2(1/(1-0.4))) + 0.4*(0.4*np.log2(1/0.4)+(1-0.4)*np.log2(1/(1-0.4))))/(0.4+0.4))
print("最优解：", best_solution)
print("最优解的目标函数值：", best_fitness)
