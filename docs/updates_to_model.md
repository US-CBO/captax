# Updates to CapTax model's formulas

We have applied changes to the formulas defined in CBO's Working Paper: [“CBO’s Model for Estimating the Effect of Federal Taxes on Capital Income from New Investment"](https://cbo.gov/publication/57429). Those changes relate to both the required before-tax rate of return to investors and the after-tax rate of return to savers, and have been introduced to:
* allow modeling of excise taxes on shares repurchases,
* update our modeling of production tax credits, 
* distinguish between sources of equity financing and uses of profits for equity-financed investment, and
* refine our modeling for calculating depreciation deductions when using the income forecast method 

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

## Refine modeling for calculating depreciation deductions when using the income forecast method (effective with Version 0.7.0)

The 10-year income forecast method used for determining the present value of depreciation deductions ($z$) for entertainment, literary, and artistic (ELA) originals accounts for the income profile of an investment in the ten years following that investment. It accounts for the fact that the income generated with that investment is at the same time declining over time at rate $\delta$ (as the value of the asset depreciates) and rising over time at the inflation rate $\pi$.



The expression for $z$ is derived by first calculating the undiscounted sum of tax depreciation deductions claimed in the ten years after the investment is made and $(\delta-\pi)$ is recovered in each period:

$$
\begin{aligned}
sum &= (\delta-\pi)\int_{0}^{10}e^{-(\delta-\pi)t}dt \\
&= \frac{(\delta-\pi)}{(\delta-\pi)}(1-e^{-10(\delta-\pi)}) \\
&= (1-e^{-10(\delta-\pi)})
\end{aligned}
$$

Because the undiscounted sum of depreciation deductions must cover the entire initial investment, each period's depreciation deduction $(\delta-\pi)$ needs to be multiplied by $\frac{1}{(1-e^{-10(\delta-\pi)})}$. In addition, future depreciation deductions are discounted at the nominal discount rate $i$. As a result:

$$
\begin{aligned}
z &= \frac{(\delta-\pi)}{(1-e^{-10(\delta-\pi)})}\int_{0}^{10}e^{-(\delta-\pi)t}e^{-it}dt \\
&= \frac{(\delta-\pi)}{(i-\pi+\delta)}\frac{(1-e^{-10(i-\pi+\delta)})}{(1-e^{-10(\delta-\pi)})}
\end{aligned}
$$
