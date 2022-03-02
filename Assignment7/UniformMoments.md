### Moments of the Uniform Distribution

If X $\sim U(\alpha, \beta)$ then:
$$
\begin{align*}
\mu_X &= \frac{\beta-\alpha}{2} \\
\sigma_X^2 &= \frac{1}{12}(\beta-\alpha)^2
\end{align*}
$$

Let $x_1, x_2, \dots x_n$ be IID, and let $y = \sum_{i=1}^N a_i x_i$ then:
$$
\begin{align*}
E(y) &= \sum_{i=1}^N a_i E(x_i) \\
var(y) &= \sum_{i=1}^N a_i^2 var(x_i) + 2\sum\sum_{i<j} a_i a_j cov(x_i,x_j)
\end{align*}
$$
Since by assumption, the $x_i$'s are independent, $cov(x_i, x_j) = 0$ so the covariance term vanishes, leaving $var(y) = \sum_{i=1}^N a_i^2 var(x_i)$.

Run the experiment $NTrials=7$ times, each $y_i =\sum_{x=1}^{NTrials} x_{i,j}$ where $i={0,1,\dots, (N-1); N=100000}$.
$$
\mu_{y_i} = E(y_i) = E\left(\sum_{j=1}^{NTrials}x_{i,j}\right) = \sum_{j=1}^{NTrials}E(x_{i,j}) 
        = NTrials\left(\frac{\beta-\alpha}{2}\right) = \frac{7}{2}
$$
Similarly:
$$
var(y_i) = \sigma_{y_i}^2 = \sum_{j=1}^N var(x_i) = Ntrials\ var(x_i)
        = \frac{NTrials}{12}\left(\beta-\alpha\right)^2 = \frac{7}{12}
$$
