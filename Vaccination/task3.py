from multiprocessing import Pool
from run_s0 import independent_run
from plot import plot
from save import save

run = 50
generation = [10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000,
              10000000, 10000000, 10000000, 10000000, 10000000]
omega = [0.001, 0.003, 0.005, 0.007, 0.009, 0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.3, 0.5, 0.7, 0.9]
N = 100
deg = 4
initial_vaccination_level = 50
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.8
beta = 10
vcost = 1
icost = 5
r0 = 6
path = './../../Desktop/'
name = 'omega-FinalVaccinationLevel'
p = Pool(7)

result_list = []
for i in range(len(omega)):
    result_list.append([])
    for j in range(run):
        result_list[i].append(
            p.apply_async(independent_run, args=(run, generation[i], omega[i], N, deg, initial_vaccination_level,
                                                 k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0)))

p.close()
p.join()
print('DONE')

data = 'run=' + str(run) + '   ' + 'generation=' + str(generation) + '   ' + 'N=' + str(
    N) + '   ' + 'deg=' + str(deg) + '   ' + 'initial_vaccination_level=' + str(
    initial_vaccination_level) + '   ' + 'k11=' + str(k11) + '   ' + 'k22=' + str(k22) + '   ' + 'k33=' + str(
    k33) + '   ' + 'k12=' + str(k12) + '   ' + 'k13=' + str(k13) + '   ' + 'k23=' + str(k23) + '   ' + 'beta=' + str(
    beta) + '   ' + 'vcost=' + str(vcost) + '   ' + 'icost=' + str(icost) + '   ' + 'r0=' + str(r0) + '\n'
data = data + 'omega=['
for o in omega:
    data = data + str(o) + ','
data = data + ']\n'

data = data + '['
vaccination_level = []
for return_list in result_list:
    v = 0
    data = data + '['
    for x in return_list:
        v = v + x.get()
        data = data + str(x.get()) + ','
        print(x.get(), end='\t')
    data = data + '],'
    print()
    vaccination_level.append(v / run)
data = data + ']'

data = data + '['
for v in vaccination_level:
    data = data + str(v) + ','
data = data + ']'
save(path=path, data=data)
plot(xaxis=omega, yaxis=vaccination_level, xlabel='omega', ylabel='Final Vaccination Level',
     path=path, name=name)
