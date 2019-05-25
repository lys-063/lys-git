from multiprocessing import Pool
from run_s0 import independent_run
from save import save
from plot import plot

'''
shorthand of notation
vaccinated 1
unvaccinated but healthy 2
unvaccinated and infected 3
'''

run = 50
generation = 10000000
omega = 0.001
N = 100
deg = 4
initial_vaccination_level = 50
k11 = 0.5
k22 = 0.5
k33 = 0.5
k12 = [0.3, 0.32, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
k13 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
k23 = 0.5
beta = 10
v_cost = 1
i_cost = 5
r0 = 5
path = '/home/lys-063/Desktop/!research/Bin.Wu.1.0/Vaccination.Project/'
path = './../../Desktop/'
name = 'k-CooperationLevel'

p = Pool(7)

# k12 = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.52, 0.5]
# k13 = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
# index, generation, omega, N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0

result_list = []
for i in range(15):
    result_list.append([])
    for j in range(run):
        result_list[i].append(p.apply_async(independent_run, args=(
            j, generation, omega, N, deg, initial_vaccination_level, k11, k22, k33, k12[i], k13[i], k23, beta, v_cost,
            i_cost, r0)))

p.close()
p.join()
print("DONE")

vaccination_level = []
for return_list in result_list:
    vaccination = 0
    for x in return_list:
        vaccination = vaccination + x.get()
        print(x.get(), end="   ")
    print()
    vaccination_level.append(vaccination / run)

k = []
for i in range(15):
    k.append(k13[i] / k12[i])

data = 'run=' + str(run) + '   ' + 'generation=' + str(generation) + '   ' + 'omega=' + str(omega) + '   ' + 'N=' + str(
    N) + '   ' + 'deg=' + str(deg) + '   ' + 'initial_vaccination_level=' + str(
    initial_vaccination_level) + '   ' + 'k11=' + str(k11) + '   ' + 'k22=' + str(k22) + '   ' + 'k33=' + str(
    k33) + '   ' + 'k23=' + str(k23) + '\n' + 'k12=' + str(k12) + '\n' + 'k13=' + str(k13) + '   ' + 'vcost=' + str(
    v_cost) + '   ' + 'icost=' + str(i_cost) + '   ' + 'r0=' + str(r0) + '\n'
data = data + '['
for v in vaccination_level:
    data = data + str(v) + ','
data = data + ']'
save(path=path, data=data)
plot(xaxis=k, yaxis=vaccination_level, xlabel='kVUI/kVUH', ylabel='Final Vaccination Level',
     path=path, name=name)
