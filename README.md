# VegaDelta Options Modelling

Welcome to **VegaDelta Options Modelling**, the turbocharged toolkit that transforms the black‑box world of options Greeks and volatility surfaces into your very own playground. Whether you’re a seasoned quant, a risk manager, or a volatility novice, **VegaDelta** delivers speed, precision, and panache in one electrifying package.

---

## ⚙️ Key Features

- 🧪 **Deep SVI Calibration**: Experience industry‑standard SVI (Stochastic Volatility Inspired) calibration with multi‑start L‑BFGS‑B optimization and regularization. Tweak your lambda weight or random seeds on the fly for arbitrage‑free, ultra‑smooth surfaces—even in thinly traded strikes.
- 🏎️ **Lightning‑Fast Implied Volatility**: Invert Black–Scholes in milliseconds using vectorized routines and Brent’s solver. Crunch hundreds of strikes in the blink of an eye.
- 🏞️ **SVI Surface Explorer**: Rotate, zoom, and inspect your calibrated volatility landscape in stunning 3D.
- 😊 **Volatility Smile**: Snap up single‑maturity smiles—choose strikes or moneyness for your X‑axis and see skew in action.
- 🔍 **Comparison Mode**: Layer multiple maturities to reveal how the smile evolves over time and market cycles.
- 📈 **Greek Visualizations**: Plot Delta, Gamma, Theta, Vega, Rho, Vanna, Volga (Vomma), Charm, and Speed in both 2D and 3D. Hover‑tooltips and download buttons make analysis a breeze.
- 🔢 **Greeks Table Lookup**: Type in a strike & expiry, and instantly fetch Greek values from the SVI surface or raw market data.

---

## 🧠 Deep Dive: The SVI Model

SVI (Stochastic Volatility Inspired) is the gold standard for parametric volatility surfaces. VegaDelta’s SVI engine:

1. **Parametrizes** the total variance as
   \[ w(k) = a + b\bigl[\rho\,(k - m) + \sqrt{(k - m)^2 + \sigma^2}\bigr] \]
   where \(k = \log(K/S)\).
2. **Calibrates** using multi‑start optimization: avoid local minima by seeding the solver in multiple random zones.
3. **Regularizes** with a tunable penalty on \(b^2 + \sigma^2\) to prevent overfitting and ensure stability in low‑liquidity regimes.
4. **Smooths** the surface by sampling a fine grid of log‑moneyness, then back‑transforming to strikes.

The result? An arbitrage‑free, ultra‑smooth volatility surface you can trust for pricing, hedging, and risk analysis.

---

## 🚀 Quickstart

1. **Clone** the repo:
   ```bash
   git clone https://github.com/your-username/volatility-surface.git
   cd volatility-surface
   ```

2. **Install** dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Mac/Linux
   .\\.venv\\Scripts\\activate # Windows
   pip install -r requirements.txt
   ```

3. **Launch** the app:
   ```bash
   streamlit run app.py
   ```

4. **Enter** any ticker (e.g. `AAPL`, `TSLA`, `SPY`) and watch volatility come alive!

---

## 💡 Pro Tips

- **Strike Filtering**: Narrow to deep ITM or OTM zones to isolate edge cases.
- **Moneyness Mode**: Normalize strikes and compare different underlyings on equal footing.
- **Advanced SVI Settings**: Ramp up `Multi-Start Count` or tweak `Regularization Weight (λ)` for bespoke fits.
- **Greek Modes**: Toggle between raw market Greeks or SVI‑smoothed Greeks for outlier‑resistant views.

---

## 🏆 Why VegaDelta?

- **Blazing Speed**: Optimized numpy & SciPy routines make heavy computations feel frictionless.
- **Full Transparency**: Open‑source code, clear math, and interactive visualizations mean you can audit every step.
- **Modular Design**: Swap in your own volatility model or add custom Greeks with minimal code changes.
- **Interactive UI**: Streamlit powers a responsive, mobile‑friendly frontend—no installs, just browse and explore.
- **Quant‑Approved**: Trusted by researchers and traders for rapid prototyping, analysis, and production insights.

---

## 🤝 Contributing

We ❤️ community contributions:

1. Fork the repo  
2. Create a branch (`git checkout -b feature/my-awesome-addition`)  
3. Commit & push  
4. Open a pull request and let’s collaborate! 🚀

---

## 📜 License

This project is released under the MIT License. Use it, tweak it, and let the community know what you build!

---

*Happy hedging—you’re now riding the VegaDelta wave!* 🌊

