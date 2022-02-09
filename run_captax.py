import captax


print('------------------')
print(' CBO CapTax Model ')
print('------------------\n')

print('Begin reading parameter files')
env = captax.Environment()
wgt = captax.Weights(env.shares)
# Create list of Policy objects to simulate
policies = captax.policy.create_policies(env)
print('Finished reading parameter files\n')

for pol in policies:
    print('------------------------------------------------------------------')
    print(f' Running {pol.policy_name} with the {pol.perspective} perspective')
    print('------------------------------------------------------------------')

    calc = captax.Calculator(env, wgt, pol)
    calc.calc_all()

    agg = captax.Aggregator(env, wgt, pol, calc)
    agg.aggregate_all()

    output = captax.OutputBuilder(agg)
    output.build_all()

    if pol.perspective == 'uniformity':
        disp = captax.Dispersion(agg, output)
        disp.calc_all()

        writer = captax.Writer(env, pol, agg, output, disp=disp)
        writer.write_all()

    else:
        writer = captax.Writer(env, pol, agg, output)
        writer.write_all()

print('----------------')
print(' Model finished  ')
print('----------------\n')
