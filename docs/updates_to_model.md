# Updates to CapTax model's formulas

We have applied changes to the formulas defined in CBO's Working Paper: [“CBO’s Model for Estimating the Effect of Federal Taxes on Capital Income from New Investment"](https://cbo.gov/publication/57429). Those changes relate to both the required before-tax rate of return to investors and the after-tax rate of return to savers, and have been introduced to:
* allow modelling of excise taxes on shares repurchases,
* update our modelling of production tax credits, and 
* distinguish between sources of equity financing and uses of profits for equity-financed investment

## Changes to the required before-tax rate of return

### Excise tax on shares repurchases for equity-financed investment in C corporations (effective with Version 0.3.0)

When modeling the required before-tax rate of return for equity-financed investment in C corporations we now account for differences in both the source of equity financing (retained earnings or new shares issuance) and the use of profits (shares repurchases or dividends). We include an excise tax $t_{rep}$ on the shares repurchases of C corporations using retained earnings as source for financing and paying out profits using shares repurchases. For those corporations the required before-tax rate of return equals:

$$T_{cc,equity}=\frac{[1-t{'}z(1-\psi k)-k^{\dagger}]}{(1-t^{\star})}[(1-\phi)+\phi(1-m)+\frac{m\phi}{(1-t_{rep})}]$$

where $m$ is the share of equity-financed investment from retained earnings and $\phi$ is the share of profits paid out as share repurchases.

### Production tax credits for marginal investment in businesses (effective with Version 0.4.0)

We previously modeled production tax credits as tax rate adjustments that varied by industry or by asset type. We now model production tax credits by including an additional additive term $\eta$ in $T$. That additional term captures the present discounted value of future production tax credits associated with a marginal investment:

$$T=\frac{[1-t{'}z(1-\psi k)-k^{\dagger}-\eta]}{(1-t^{\star})}$$

## Changes to the after-tax rate of return to savers for equity-financed investment in C corporations when savings are taxable (effective with Version 0.3.0)

The new expression for the after-tax rate of return to savers for equity-financed investment in C corporations accounts for differences in the source of equity financing and the use of profits. The after-tax rate of return to savers is a weighted average of four components, three of which are consistent with the "new view" of dividend taxation. (Under the "new view" the source of equity financing is the same as the use of profits and dividend taxes do not matter for marginal investment.) 
The new expression is:

$$s_{cc,equity,ft}=(1-m)(1-\phi)[i_{equity}(1-t_{div})-\pi]+[m+(1-m)\phi]\sum_{n}^{3}(\omega_{n}g_{n})$$

where $m$ is the share of equity-financed investment from retained earnings and $\phi$ is the share of profits paid out as share repurchases.

