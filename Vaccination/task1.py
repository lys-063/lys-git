from multiprocessing import Pool
from run_s0 import independent_run
from plot import plot
from save import save

run = 30
generation = 1000000
omega = 0.01
N = 100
deg = 4
initial_vaccination_level = 50
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.8
beta = [0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10]
vcost = 1
icost = 5
r0 = 6
path = './../../Desktop/'
name = 'SelectionIntensity-FinalVaccinationLevel'
p = Pool(7)

result_list = []
for i in range(len(beta)):
    result_list.append([])
    for j in range(run):
        result_list[i].append(
            p.apply_async(independent_run, args=(i, generation, omega, N, deg, initial_vaccination_level,
                                                 k11, k22, k33, k12, k13, k23, beta[i], vcost, icost, r0)))
p.close()
p.join()
print('DONE')

vaccination_level = []
for return_list in result_list:
    v = 0
    for x in return_list:
        v = v + x.get()
        print(x.get(), end='\t')
    print()
    vaccination_level.append(v / run)

data = 'run=' + str(run) + '   ' + 'generation=' + str(generation) + '   ' + 'omega=' + str(omega) + '   ' + 'N=' + str(
    N) + '   ' + 'deg=' + str(deg) + '   ' + 'initial_vaccination_level=' + str(
    initial_vaccination_level) + '   ' + 'k11=' + str(k11) + '   ' + 'k22=' + str(k22) + '   ' + 'k33=' + str(
    k33) + '   ' + 'k12=' + str(k12) + '   ' + 'k13=' + str(k13) + '   ' + 'k23=' + str(k23) + '   ' + 'vcost=' + str(
    vcost) + '   ' + 'icost=' + str(icost) + '   ' + 'r0=' + str(r0) + '\n'
data = data + '['
for v in vaccination_level:
    data = data + str(v) + ','
data = data + ']'
save(path=path, data=data)
plot(xaxis=beta, yaxis=vaccination_level, xlabel='Selection Intensity', ylabel='Final Vaccination Level',
     path=path, name=name)
