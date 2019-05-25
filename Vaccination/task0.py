from multiprocessing import Pool
from run_s0 import independent_run
from save import save
from plot import plot

run = 10
generation = 1000
omega = 0.1
N = 100
deg = 4
initial_vaccination_level = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
k11 = 0.5
k22 = 0.5
k33 = 0.5
k12 = 0.8
k13 = 0.8
k23 = 0.5
beta = 10
vcost = 3.5
icost = 5
r0 = 3
path = './../../Desktop/'
name = 'InitialVaccinationLevel-FinalVaccinationLevel'
p = Pool(7)

result_list = []
for i in range(len(initial_vaccination_level)):
    result_list.append([])
    for j in range(run):
        result_list[i].append(
            p.apply_async(independent_run, args=(run, generation, omega, N, deg, initial_vaccination_level[i],
                                                 k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0)))

p.close()
p.join()
print("DONE")

vaccination_level = []
for return_list in result_list:
    v = 0
    for x in return_list:
        v = v + x.get()
        print(x.get(), end='\t')
    print()
    vaccination_level.append(v / run)

data = 'run=' + str(run) + '   ' + 'generation=' + str(generation) + '   ' + 'omega=' + str(omega) + '   ' + 'N=' + str(
    N) + '   ' + 'deg=' + str(deg) + '   ' + 'k11=' + str(k11) + '   ' + 'k22=' + str(k22) + '   ' + 'k33=' + str(
    k33) + '   ' + 'k12=' + str(k12) + '   ' + 'k13=' + str(k13) + '   ' + 'k23=' + str(k23) + '   ' + 'beta=' + str(
    beta) + '   ' + 'vcost=' + str(vcost) + '   ' + 'icost=' + str(icost) + '   ' + 'r0=' + str(r0) + '\n'
data = data + '['
for v in vaccination_level:
    data = data + str(v) + ','
data = data + ']'

save(path=path, data=data)
plot(xaxis=initial_vaccination_level, yaxis=vaccination_level, xlabel='Initial Vaccination Level',
     ylabel='Final Vaccination Level', path=path, name=name)
