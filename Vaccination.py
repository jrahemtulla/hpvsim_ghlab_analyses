import numpy as np
import pandas as pd
import sciris as sc
import hpvsim as hpv

pars = dict(
    n_agents      = 20e3,       # Population size
    n_years       = 60,         # Number of years to simulate
    verbose       = 0,          # Don't print details of the run
    rand_seed     = 2,          # Set a non-default seed
    genotypes     = [16, 18],   # Include the two genotypes of greatest general interest
)

probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
results_list = []

for prob in probs:
    vx = hpv.routine_vx(prob=prob, start_year=2015, age_range=[9,14], product='bivalent')
    sim = hpv.Sim(pars, interventions=vx, label='With vaccination (prob={})'.format(prob))
    sim.run()
    results = sim.results

    hpv_incidence_50 = results['hpv_incidence'][50]
    cancer_incidence_50 = results['cancer_incidence'][50]
    cancer_cases_50 = results['cancers'][50]

    results_list.append({'Vaccination probability': prob,
     'HPV incidence after 50 years': hpv_incidence_50,
     'Cervical cancer incidence after 50 years': cancer_incidence_50,
     'Cancers_in_year 50': cancer_cases_50})

    results_vx_df = pd.DataFrame(results_list)

    # Save the results to an Excel file
    results_vx_df.to_excel('results.xlsx', index=False)

    #print('Results for simulation with vaccination probability =', prob)
    #print('-------------------------------------------')
    #print('HPV incidence:', results['hpv_incidence'][50])
    #print('Cervical cancer incidence:', results['cancer_incidence'][50])
    #print('-------------------------------------------')