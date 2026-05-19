import streamlit as st
import sympy as sp

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Root Finder · Fixed-Point Iteration",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Lora:ital,wght@0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0e1117;
    --surface:   #161b27;
    --border:    #252d3d;
    --accent:    #4f8ef7;
    --accent-dim:#2a4a8a;
    --gold:      #f5c542;
    --green:     #2ecc71;
    --amber:     #f39c12;
    --red:       #e74c3c;
    --text:      #e2e8f0;
    --muted:     #8892a4;
    --mono:      'DM Mono', monospace;
    --serif:     'Lora', Georgia, serif;
    --sans:      'DM Sans', sans-serif;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: var(--sans);
    color: var(--text);
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0d1b38 0%, #0e1117 60%, #0b1a10 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.4rem 2.8rem 2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: var(--serif);
    font-size: 2.4rem;
    font-weight: 600;
    line-height: 1.15;
    margin: 0 0 0.5rem;
    color: #fff;
}
.hero-sub {
    font-size: 0.92rem;
    color: var(--muted);
    font-weight: 300;
    margin: 0;
}

/* ── Panel card ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.2rem;
}
.panel-label {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Convergence badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-family: var(--mono);
    font-size: 0.78rem;
    font-weight: 500;
    margin-bottom: 0.8rem;
}
.badge-fast   { background:#0f2d1c; border:1px solid #1e5c38; color:#4ade80; }
.badge-slow   { background:#2d1f09; border:1px solid #5c3a11; color:#fbbf24; }
.badge-diverge{ background:#2d0f0f; border:1px solid #5c2020; color:#f87171; }

/* ── Derivative chip ── */
.deriv-chip {
    background: #141e35;
    border: 1px solid var(--accent-dim);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    font-family: var(--mono);
    font-size: 0.9rem;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.deriv-chip .label { color: var(--muted); font-size: 0.75rem; margin-right: 0.3rem; }

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.metric-card {
    flex: 1;
    min-width: 140px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.metric-card .m-label { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.metric-card .m-value { font-family: var(--mono); font-size: 1.6rem; font-weight: 500; color: #fff; line-height: 1; }
.metric-card .m-value.accent { color: var(--accent); }
.metric-card .m-value.gold   { color: var(--gold); }
.metric-card .m-sub { font-size: 0.72rem; color: var(--muted); margin-top: 0.3rem; }

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Syntax guide code blocks ── */
.syntax-row {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
.syntax-row:last-child { border-bottom: none; }
.syntax-code {
    font-family: var(--mono);
    background: #0e1117;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    color: var(--accent);
    white-space: nowrap;
    font-size: 0.8rem;
}
.syntax-desc { color: var(--muted); flex: 1; font-size: 0.8rem; }

/* ── Expander tweak ── */
details summary { font-family: var(--mono) !important; font-size: 0.82rem !important; }

/* ── Iteration log ── */
.iter-log {
    background: #090d14;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    font-family: var(--mono);
    font-size: 0.8rem;
    line-height: 1.9;
    color: #94a3b8;
    max-height: 340px;
    overflow-y: auto;
}
.iter-log span.n  { color: #475569; width: 2.5rem; display: inline-block; }
.iter-log span.v  { color: #7dd3fc; }
.iter-log span.hi { color: var(--gold); font-weight: 500; }

/* ── Final result banner ── */
.result-banner {
    background: linear-gradient(135deg, #0a2010, #0d1f35);
    border: 1px solid #2a5f3a;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    text-align: center;
    margin-top: 1rem;
}
.result-banner .rb-label { font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--green); margin-bottom: 0.4rem; }
.result-banner .rb-value { font-family: var(--mono); font-size: 2.6rem; font-weight: 500; color: #fff; line-height: 1.1; }
.result-banner .rb-sub   { font-size: 0.8rem; color: var(--muted); margin-top: 0.4rem; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📐 Root Finder")
    st.caption("Fixed-Point Iteration · v2.0")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("**⚙️ Solver Settings**")

    equation_input = st.text_input(
        "g(x) — iteration function",
        value="(1 - x**2)**(1/3)",
        help="Enter g(x) such that the fixed-point x = g(x) is the root you seek. "
             "Use Python/SymPy syntax (e.g. x**2 not x^2).",
    )
    x0_val = st.number_input(
        "Initial guess x₀",
        value=0.75,
        step=0.1,
        format="%.4f",
        help="Starting point for the iteration. Choose a value close to the expected root "
             "and within the convergence region where |g′(x)| < 1.",
    )
    max_iter = st.slider(
        "Max iterations",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
        help="Upper bound on iteration count. The solver stops early once convergence is detected.",
    )
    tol = st.select_slider(
        "Tolerance (ε)",
        options=[1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
        value=1e-6,
        format_func=lambda v: f"{v:.0e}",
        help="Convergence threshold. The iteration stops when |xₙ₊₁ − xₙ| < ε.",
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Syntax Guide ────────────────────────────────────────────────────────
    st.markdown("**📖 Syntax Reference**")
    guide = [
        ("x**2",         "x squared (xⁿ → x**n)"),
        ("sqrt(x)",      "Square root √x"),
        ("exp(x)",       "Euler's number eˣ"),
        ("log(x)",       "Natural log ln(x)"),
        ("log(x, 10)",   "Base-10 logarithm"),
        ("sin(x)",       "Sine (radians)"),
        ("cos(x)",       "Cosine (radians)"),
        ("pi",           "π ≈ 3.14159…"),
        ("Rational(1,3)","Exact fraction ⅓"),
    ]
    rows_html = "".join(
        f'<div class="syntax-row">'
        f'<span class="syntax-code">{code}</span>'
        f'<span class="syntax-desc">{desc}</span>'
        f'</div>'
        for code, desc in guide
    )
    st.markdown(f'<div class="panel" style="padding:0.8rem 1rem">{rows_html}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Theory note ─────────────────────────────────────────────────────────
    with st.expander("📚 How does it work?"):
        st.markdown(
            "The **Fixed-Point Iteration** rewrites f(x)=0 as **x = g(x)**. "
            "Starting from x₀, we iterate:\n\n"
            "```\nxₙ₊₁ = g(xₙ)\n```\n\n"
            "Convergence is **guaranteed** near the fixed point when the "
            "**Banach condition** holds:\n\n"
            "```\n|g′(x₀)| < 1\n```\n\n"
            "Smaller |g′| → faster convergence."
        )

    calculate = st.button("▶ Find Root", type="primary", use_container_width=True)


# ─── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Numerical Analysis · Fixed-Point Iteration</div>
  <div class="hero-title">Root Finder</div>
  <p class="hero-sub">
    Solve x&nbsp;=&nbsp;g(x) iteratively. Enter your iteration function in the
    sidebar, set an initial guess, and hit <strong>Find Root</strong>.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Preview of current input ────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("g(x)", equation_input if equation_input else "—")
with c2:
    st.metric("Initial guess x₀", f"{x0_val:.4f}")
with c3:
    st.metric("Tolerance ε", f"{tol:.0e}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─── Computation ───────────────────────────────────────────────────────────────
if calculate:
    if not equation_input.strip():
        st.error("⚠️  Please enter a function g(x) in the sidebar before calculating.")
        st.stop()

    x = sp.symbols('x')

    with st.spinner("Analysing convergence and running iterations…"):
        try:
            # ── 1. Parse ──────────────────────────────────────────────────
            phi = sp.sympify(equation_input)

            # ── 2. Differentiate ──────────────────────────────────────────
            phi_prime = sp.diff(phi, x)

            # ── 3. Convergence check ──────────────────────────────────────
            derivative_value = float(abs(phi_prime.subs(x, x0_val).evalf()))

        except Exception:
            st.error(
                "⚠️  **Invalid expression.** Could not parse the function. "
                "Check the Syntax Reference in the sidebar — use `x**2` not `x^2`, "
                "and `exp(x)` not `e^x`."
            )
            st.stop()

    # ── Analysis panel ───────────────────────────────────────────────────────
    st.markdown('<div class="panel-label">📊 Convergence Analysis</div>', unsafe_allow_html=True)

    # Derivative chip
    st.markdown(
        f'<div class="deriv-chip">'
        f'<span class="label">|g′(x₀)|</span>'
        f'= &nbsp;<strong>{derivative_value:.6f}</strong>'
        f'</div>',
        unsafe_allow_html=True,
    )

    run_loop = False
    if derivative_value < 0.5:
        st.markdown(
            '<div class="badge badge-fast">🏎️ &nbsp;Fast Convergence &nbsp;·&nbsp; |g′| &lt; 0.5</div>',
            unsafe_allow_html=True,
        )
        run_loop = True
    elif derivative_value < 1.0:
        st.markdown(
            '<div class="badge badge-slow">🐢 &nbsp;Slow Convergence &nbsp;·&nbsp; 0.5 ≤ |g′| &lt; 1</div>',
            unsafe_allow_html=True,
        )
        run_loop = True
    else:
        st.markdown(
            '<div class="badge badge-diverge">❌ &nbsp;Divergence &nbsp;·&nbsp; |g′| ≥ 1</div>',
            unsafe_allow_html=True,
        )
        st.error(
            "The Banach condition **|g′(x₀)| < 1** is not satisfied at x₀. "
            "The iteration will **diverge**. Try a different g(x) or a different starting point."
        )

    # ── Iteration loop ───────────────────────────────────────────────────────
    if run_loop:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        phi_func    = sp.lambdify(x, phi, "math")
        x_current   = x0_val
        found_root  = False
        iterations  = []     # collect (step, x_next) — backend unchanged

        with st.spinner(f"Iterating (tolerance ε = {tol:.0e}, max {max_iter} steps)…"):
            for step in range(1, max_iter + 1):
                x_next = phi_func(x_current)
                iterations.append((step, x_next))

                if abs(x_next - x_current) < tol:
                    found_root = True
                    break

                x_current = x_next

        # ── Result banner ────────────────────────────────────────────────
        if found_root:
            final_root  = iterations[-1][1]
            total_steps = iterations[-1][0]

            # st.metric row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("🎯 Fixed-Point Root", f"{final_root:.8f}")
            with m2:
                st.metric("🔄 Iterations Used", total_steps)
            with m3:
                st.metric("📉 |g′(x₀)|", f"{derivative_value:.6f}")

            st.markdown(
                f'<div class="result-banner">'
                f'  <div class="rb-label">✅ Converged — Fixed-Point Root</div>'
                f'  <div class="rb-value">x* ≈ {final_root:.8f}</div>'
                f'  <div class="rb-sub">Found in {total_steps} iteration{"s" if total_steps != 1 else ""} '
                f'&nbsp;·&nbsp; ε = {tol:.0e}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.error(
                f"🛑 **Did not converge** within {max_iter} iterations. "
                "Try increasing the max iteration count, loosening the tolerance, "
                "or choosing a different g(x)."
            )

        # ── Iteration log (hidden in expander) ──────────────────────────
        st.markdown("")
        with st.expander(f"🔬 View full iteration log ({len(iterations)} steps)"):
            # Build the HTML table in one shot for performance
            rows = []
            for i, (step, val) in enumerate(iterations):
                is_last = (i == len(iterations) - 1) and found_root
                cls     = "hi" if is_last else "v"
                rows.append(
                    f'<div>'
                    f'<span class="n">#{step:>3}</span>'
                    f'  x&nbsp;=&nbsp;<span class="{cls}">{val:.10f}</span>'
                    f'{"  ← ✓ converged" if is_last else ""}'
                    f'</div>'
                )
            st.markdown(
                f'<div class="iter-log">{"".join(rows)}</div>',
                unsafe_allow_html=True,
            )

else:
    # ── Idle placeholder ─────────────────────────────────────────────────────
    st.info(
        "👈  **Enter your iteration function g(x) in the sidebar**, set your initial guess, "
        "then click **▶ Find Root** to begin. "
        "Check the Syntax Reference in the sidebar if you're unsure about formatting."
    )