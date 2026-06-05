import streamlit as st
import sympy as sp
import numpy as np

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
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Lora:ital,wght@0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');
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
html, body, [class*="css"] { font-family: var(--sans); color: var(--text); }
.hero {
    background: linear-gradient(135deg, #0d1b38 0%, #0e1117 60%, #0b1a10 100%);
    border: 1px solid var(--border); border-radius: 16px;
    padding: 2.4rem 2.8rem 2rem; margin-bottom: 1.8rem;
    position: relative; overflow: hidden;
}
.hero::before {
    content: ""; position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow { font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
.hero-title   { font-family: var(--serif); font-size: 2.4rem; font-weight: 600; line-height: 1.15; margin: 0 0 0.5rem; color: #fff; }
.hero-sub     { font-size: 0.92rem; color: var(--muted); font-weight: 300; margin: 0; }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem 1.6rem; margin-bottom: 1.2rem; }
.panel-label { font-family: var(--mono); font-size: 0.68rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }
.panel-label::after { content: ""; flex: 1; height: 1px; background: var(--border); }
.badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.85rem; border-radius: 999px; font-family: var(--mono); font-size: 0.78rem; font-weight: 500; margin-bottom: 0.8rem; }
.badge-fast    { background:#0f2d1c; border:1px solid #1e5c38; color:#4ade80; }
.badge-slow    { background:#2d1f09; border:1px solid #5c3a11; color:#fbbf24; }
.badge-diverge { background:#2d0f0f; border:1px solid #5c2020; color:#f87171; }
.deriv-chip { background: #141e35; border: 1px solid var(--accent-dim); border-radius: 8px; padding: 0.9rem 1.2rem; font-family: var(--mono); font-size: 0.9rem; color: var(--accent); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.6rem; }
.deriv-chip .label { color: var(--muted); font-size: 0.75rem; margin-right: 0.3rem; }
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
.syntax-row { display: flex; align-items: baseline; gap: 0.7rem; padding: 0.45rem 0; border-bottom: 1px solid var(--border); font-size: 0.85rem; }
.syntax-row:last-child { border-bottom: none; }
.syntax-code { font-family: var(--mono); background: #0e1117; border: 1px solid var(--border); border-radius: 4px; padding: 0.15rem 0.5rem; color: var(--accent); white-space: nowrap; font-size: 0.8rem; }
.syntax-desc { color: var(--muted); flex: 1; font-size: 0.8rem; }
details summary { font-family: var(--mono) !important; font-size: 0.82rem !important; }
.iter-log { background: #090d14; border: 1px solid var(--border); border-radius: 8px; padding: 0.9rem 1.1rem; font-family: var(--mono); font-size: 0.8rem; line-height: 1.9; color: #94a3b8; max-height: 340px; overflow-y: auto; }
.iter-log span.n  { color: #475569; width: 2.5rem; display: inline-block; }
.iter-log span.v  { color: #7dd3fc; }
.iter-log span.hi { color: var(--gold); font-weight: 500; }
.result-banner { background: linear-gradient(135deg, #0a2010, #0d1f35); border: 1px solid #2a5f3a; border-radius: 12px; padding: 1.4rem 1.8rem; text-align: center; margin-top: 1rem; }
.result-banner .rb-label { font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--green); margin-bottom: 0.4rem; }
.result-banner .rb-value { font-family: var(--mono); font-size: 2.6rem; font-weight: 500; color: #fff; line-height: 1.1; }
.result-banner .rb-sub   { font-size: 0.8rem; color: var(--muted); margin-top: 0.4rem; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 1.5rem 0; }
/* ── Candidate table ── */
.cand-table { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 0.82rem; }
.cand-table th { color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.68rem; padding: 0.5rem 0.8rem; border-bottom: 1px solid var(--border); text-align: left; }
.cand-table td { padding: 0.55rem 0.8rem; border-bottom: 1px solid #1a2235; vertical-align: middle; }
.cand-table tr:last-child td { border-bottom: none; }
.cand-table tr:hover td { background: #1a2235; }
.tag-ok  { background:#0f2d1c; border:1px solid #1e5c38; color:#4ade80; border-radius:4px; padding:0.1rem 0.5rem; font-size:0.72rem; }
.tag-bad { background:#2d0f0f; border:1px solid #5c2020; color:#f87171; border-radius:4px; padding:0.1rem 0.5rem; font-size:0.72rem; }
.mode-pill { display:inline-block; background:#141e35; border:1px solid var(--accent-dim); color:var(--accent); font-family:var(--mono); font-size:0.72rem; border-radius:6px; padding:0.2rem 0.7rem; margin-bottom:0.6rem; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📐 Root Finder")
    st.caption("Fixed-Point Iteration · v3.0")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Input mode selection ────────────────────────────────────────────
    st.markdown("**🔀 Input Mode**")
    input_mode = st.radio(
        "What will you provide?",
        options=["f(x) — original equation", "g(x) — iteration function"],
        help="Choose f(x) to let the solver auto-generate g(x) candidates. "
             "Choose g(x) if you have already rearranged the equation.",
        label_visibility="collapsed",
    )
    use_fx = input_mode.startswith("f(x)")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**⚙️ Solver Settings**")

    if use_fx:
        equation_input = st.text_input(
            "f(x) — original equation",
            value="x**3 - x - 1",
            help="Enter f(x) where the root satisfies f(x) = 0. "
                 "Do NOT include '= 0'. Example: x**3 - x - 1",
        )
    else:
        equation_input = st.text_input(
            "g(x) — iteration function",
            value="(1 - x**2)**(1/3)",
            help="Enter g(x) such that the fixed-point x = g(x) is the root. "
                 "Use Python/SymPy syntax (e.g. x**2 not x^2).",
        )

    st.markdown("**📏 Convergence Interval [a, b]**")
    ia, ib = st.columns(2)
    with ia:
        a_val = st.number_input(
            "a  (left endpoint)",
            value=0.0,
            step=0.1,
            format="%.4f",
            help="Left endpoint of the interval [a, b]. "
                 "Theorem 2.2 requires g(x) ∈ [a, b] for all x ∈ [a, b].",
        )
    with ib:
        b_val = st.number_input(
            "b  (right endpoint)",
            value=1.5,
            step=0.1,
            format="%.4f",
            help="Right endpoint of the interval [a, b]. "
                 "The iteration will start from the midpoint x₀ = (a+b)/2.",
        )
    st.markdown("**🎯 Initial Guess x₀**")
    use_custom_x0 = st.checkbox(
        "Provide custom initial guess x₀",
        value=False,
        help="By default, iteration starts from the midpoint (a+b)/2. "
             "Enable this to supply your own starting point within [a, b].",
    )
    if use_custom_x0:
        x0_custom = st.number_input(
            "x₀ (custom initial guess)",
            value=round((0.0 + 1.5) / 2, 4),   # default shown as midpoint of default a,b
            step=0.1,
            format="%.4f",
            help="Must satisfy a ≤ x₀ ≤ b. "
                 "Theorem 2.3 guarantees convergence from any point in [a, b].",
        )
    else:
        x0_custom = None

    max_iter = st.slider(
        "Max iterations",
        min_value=10, max_value=500, value=100, step=10,
        help="The solver stops early once convergence is detected.",
    )
    tol = st.select_slider(
        "Tolerance (ε)",
        options=[1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
        value=1e-6,
        format_func=lambda v: f"{v:.0e}",
        help="Stops when |xₙ₊₁ − xₙ| < ε.",
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Syntax reference ────────────────────────────────────────────────
    st.markdown("**📖 Syntax Reference**")
    guide = [
        ("x**2",          "x squared  (xⁿ → x**n)"),
        ("sqrt(x)",       "Square root √x"),
        ("exp(x)",        "Euler's number eˣ"),
        ("log(x)",        "Natural log ln(x)"),
        ("log(x, 10)",    "Base-10 logarithm"),
        ("sin(x)",        "Sine (radians)"),
        ("cos(x)",        "Cosine (radians)"),
        ("pi",            "π ≈ 3.14159…"),
        ("Rational(1,3)", "Exact fraction ⅓"),
    ]
    rows_html = "".join(
        f'<div class="syntax-row">'
        f'<span class="syntax-code">{c}</span>'
        f'<span class="syntax-desc">{d}</span>'
        f'</div>'
        for c, d in guide
    )
    st.markdown(f'<div class="panel" style="padding:0.8rem 1rem">{rows_html}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.expander("📚 How does it work?"):
        st.markdown(
            "**Fixed-Point Iteration** rewrites f(x)=0 as **x = g(x)**.\n\n"
            "Starting from x₀, we iterate:\n```\nxₙ₊₁ = g(xₙ)\n```\n\n"
            "Convergence is **guaranteed** when the **Banach condition** holds:\n"
            "```\n|g′(x₀)| < 1\n```\nSmaller |g′| → faster convergence."
        )

    calculate = st.button("▶ Find Root", type="primary", use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# SESSION STATE — initialise keys that must survive reruns
# ════════════════════════════════════════════════════════════════════════
# These defaults are set only on the very first run of the script.
for _key, _default in [
    ("calculated",    False),   # has the button ever been pressed?
    ("candidates",    None),    # list of (label, expr, dval, viable) for Path A
    ("use_fx_cache",  None),    # which mode was active when we last calculated
    ("eq_cache",      None),    # equation string used in the last calculation
    ("a_cache",       None),    # interval [a] used in the last calculation
    ("b_cache",       None),    # interval [b] used in the last calculation
    ("deriv_val_gx",  None),    # |g'(x0)| for Path B
    ("phi_gx",        None),    # g(x) expression string for Path B
    ("run_loop_gx",   False),   # whether Path B passed the convergence check
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default

# Stale-result guard:
# If the user changes the equation, x0, or mode, the old results are
# no longer valid. Reset so the idle placeholder reappears.
_inputs_changed = (
    st.session_state["eq_cache"]        != equation_input
    or st.session_state["a_cache"]      != a_val
    or st.session_state["b_cache"]      != b_val
    or st.session_state["use_fx_cache"] != use_fx
)
if _inputs_changed and st.session_state["calculated"]:
    st.session_state["calculated"]   = False
    st.session_state["candidates"]   = None
    st.session_state["deriv_val_gx"] = None
    st.session_state["phi_gx"]       = None
    st.session_state["run_loop_gx"]  = False

# Latch the button press into session state.
# st.button() is True only for the single rerun caused by the click itself.
# Writing it here makes it persist across all future reruns
# (e.g. those triggered by the st.radio widget changing).
if calculate:
    st.session_state["calculated"]   = True
    st.session_state["eq_cache"]     = equation_input
    st.session_state["a_cache"]      = a_val
    st.session_state["b_cache"]      = b_val
    st.session_state["use_fx_cache"] = use_fx



def check_interval_conditions(phi_sym, x_sym, a, b, n_points=100):
    """
    Implements Theorems 2.2 & 2.3 over the interval [a, b].

    Returns a dict with keys:
        cond1_pass (bool)  : g(x) ∈ [a, b] for all test points
        cond2_pass (bool)  : max |g′(x)| < 1 over the interval
        k          (float) : the Lipschitz constant max |g′(x)|
        g_min      (float) : minimum g(x) value over test points
        g_max      (float) : maximum g(x) value over test points
        both_pass  (bool)  : True only if both conditions hold
    """
    test_pts  = np.linspace(a, b, n_points)
    phi_num   = sp.lambdify(x_sym, phi_sym, "numpy")
    phi_prime = sp.diff(phi_sym, x_sym)
    gprime_num = sp.lambdify(x_sym, phi_prime, "numpy")

    g_vals      = np.array([float(phi_num(xi))   for xi in test_pts], dtype=float)
    gprime_vals = np.array([float(gprime_num(xi)) for xi in test_pts], dtype=float)

    g_min = float(np.nanmin(g_vals))
    g_max = float(np.nanmax(g_vals))
    k     = float(np.nanmax(np.abs(gprime_vals)))

    cond1_pass = (g_min >= a) and (g_max <= b)
    cond2_pass = k < 1.0

    return {
        "cond1_pass": cond1_pass,
        "cond2_pass": cond2_pass,
        "k":          k,
        "g_min":      g_min,
        "g_max":      g_max,
        "both_pass":  cond1_pass and cond2_pass,
    }


def display_theorem_check(chk, a, b):
    """
    Renders the Theorem 2.2 / 2.3 condition check panel in the UI.
    Returns True if iteration should proceed, False otherwise.
    """
    st.markdown('<div class="panel-label">📐 Theorem 2.2 &amp; 2.3 — Global Convergence Check</div>',
                unsafe_allow_html=True)

    # ── Condition 1 ──────────────────────────────────────────────────────────
    c1_tag = (
        '<span class="tag-ok">✅ PASS</span>'  if chk["cond1_pass"]
        else '<span class="tag-bad">❌ FAIL</span>'
    )
    c1_detail = (
        f'g(x) ∈ [{chk["g_min"]:.5f}, {chk["g_max"]:.5f}] ⊆ [{a}, {b}]'
        if chk["cond1_pass"]
        else f'g(x) range [{chk["g_min"]:.5f}, {chk["g_max"]:.5f}] ⊄ [{a}, {b}]'
    )
    # ── Condition 2 ──────────────────────────────────────────────────────────
    c2_tag = (
        '<span class="tag-ok">✅ PASS</span>'  if chk["cond2_pass"]
        else '<span class="tag-bad">❌ FAIL</span>'
    )
    c2_detail = f'k = max |g′(x)| = <strong>{chk["k"]:.6f}</strong> {"&lt; 1" if chk["cond2_pass"] else "≥ 1"}'

    html = f"""
<table class="cand-table">
<thead><tr>
  <th>Theorem</th><th>Condition</th><th>Result</th><th>Detail</th>
</tr></thead>
<tbody>
<tr>
  <td>Thm 2.2 (i)</td>
  <td>g(x) ∈ [a, b] for all x ∈ [a, b]</td>
  <td>{c1_tag}</td>
  <td><code>{c1_detail}</code></td>
</tr>
<tr>
  <td>Thm 2.2 (ii) / 2.3</td>
  <td>∃ k &lt; 1 : |g′(x)| ≤ k on (a, b)</td>
  <td>{c2_tag}</td>
  <td>{c2_detail}</td>
</tr>
</tbody>
</table>
"""
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("")

    if chk["both_pass"]:
        x0_mid = (a + b) / 2.0
        st.success(
            f"✅ **Both conditions satisfied.** Unique fixed point guaranteed in [{a}, {b}] "
            f"(Theorem 2.3). Starting iteration from midpoint **x₀ = {x0_mid:.6f}**."
        )
    else:
        fails = []
        if not chk["cond1_pass"]:
            fails.append("Condition 1 (g(x) ∉ [a, b])")
        if not chk["cond2_pass"]:
            fails.append(f"Condition 2 (k = {chk['k']:.6f} ≥ 1)")
        st.error(
            "❌ **Global convergence not guaranteed.** "
            + " and ".join(fails)
            + " failed. Try adjusting the interval [a, b] or choosing a different g(x)."
        )

    return chk["both_pass"]


# ════════════════════════════════════════════════════════════════════════
# HELPER — run the iteration loop (shared by both paths)
# ════════════════════════════════════════════════════════════════════════
def run_iteration(phi_sym, x_sym, x0, max_it, tolerance):
    """
    Returns (found_root: bool, iterations: list of (step, value)).
    Core math loop — unchanged from original.
    """
    phi_func  = sp.lambdify(x_sym, phi_sym, "math")
    x_current = x0
    iterations = []
    found_root = False
    for step in range(1, max_it + 1):
        x_next = phi_func(x_current)
        iterations.append((step, x_next))
        if abs(x_next - x_current) < tolerance:
            found_root = True
            break
        x_current = x_next
    return found_root, iterations


def convergence_badge(deriv_val):
    """Return (run_loop, badge_html, label_str)."""
    if deriv_val < 0.5:
        return True, '<div class="badge badge-fast">🏎️ &nbsp;Fast Convergence &nbsp;·&nbsp; |g′| &lt; 0.5</div>', "fast"
    elif deriv_val < 1.0:
        return True, '<div class="badge badge-slow">🐢 &nbsp;Slow Convergence &nbsp;·&nbsp; 0.5 ≤ |g′| &lt; 1</div>', "slow"
    else:
        return False, '<div class="badge badge-diverge">❌ &nbsp;Divergence &nbsp;·&nbsp; |g′| ≥ 1</div>', "diverge"


def display_results(found_root, iterations, deriv_val, tol_val):
    """Render metrics, result banner, and iteration log expander."""
    if found_root:
        final_root  = iterations[-1][1]
        total_steps = iterations[-1][0]
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🎯 Fixed-Point Root", f"{final_root:.8f}")
        with m2:
            st.metric("🔄 Iterations Used", total_steps)
        with m3:
            st.metric("📉 k = max|g′| on [a,b]", f"{deriv_val:.6f}")
        st.markdown(
            f'<div class="result-banner">'
            f'  <div class="rb-label">✅ Converged — Fixed-Point Root</div>'
            f'  <div class="rb-value">x* ≈ {final_root:.8f}</div>'
            f'  <div class="rb-sub">Found in {total_steps} iteration{"s" if total_steps!=1 else ""}'
            f'  &nbsp;·&nbsp; ε = {tol_val:.0e}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error(
            f"🛑 **Did not converge** within {len(iterations)} iterations. "
            "Try increasing the limit, loosening ε, or choosing a different g(x)."
        )

    st.markdown("")
    with st.expander(f"🔬 View full iteration log ({len(iterations)} steps)"):
        rows = []
        for i, (step, val) in enumerate(iterations):
            is_last = (i == len(iterations) - 1) and found_root
            cls = "hi" if is_last else "v"
            rows.append(
                f'<div>'
                f'<span class="n">#{step:>3}</span>'
                f'  x&nbsp;=&nbsp;<span class="{cls}">{val:.10f}</span>'
                f'{"  ← ✓ converged" if is_last else ""}'
                f'</div>'
            )
        st.markdown(f'<div class="iter-log">{"".join(rows)}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Numerical Analysis · Fixed-Point Iteration</div>
  <div class="hero-title">Root Finder</div>
  <p class="hero-sub">
    Solve x&nbsp;=&nbsp;g(x) iteratively. Provide f(x) for automatic g(x)
    generation, or supply g(x) directly. Configure the solver in the sidebar.
  </p>
</div>
""", unsafe_allow_html=True)

tab_solver, tab_algo = st.tabs(["🧮 Solver", "💻 Core Algorithm"])


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — CORE ALGORITHM  (rendered BEFORE tab_solver so st.stop()
#          inside tab_solver never skips this static content)
# ══════════════════════════════════════════════════════════════════════
with tab_algo:

    st.markdown("## 💻 Core Algorithm — Fixed-Point Iteration")
    st.markdown(
        "Pure backend logic, stripped of all UI code. "
        "The solver verifies **global convergence** over an interval **[a, b]** "
        "before iterating, in accordance with Theorems 2.2 and 2.3."
    )

    # ── Stage 0 ─────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Stage 0 — Parse the Iteration Function g(x)")
    st.markdown(
        "Whether the user provides **f(x)** (Path A) or **g(x)** directly (Path B), "
        "the solver produces a SymPy expression `phi` representing g(x) and a user-chosen "
        "interval `[a, b]`.  For **Path A**, up to three g(x) candidates are "
        "auto-generated from f(x):"
    )
    st.code("""import sympy as sp
import numpy as np

x = sp.symbols('x')

# ── Path A: auto-generate g(x) candidates from f(x) ─────────────────
f_expr  = sp.sympify("x**3 - x - 1")
f_prime = sp.diff(f_expr, x)

candidates = [
    ("g1: x - f(x)",          x - f_expr),               # standard rearrangement
    ("g2: x + f(x)",          x + f_expr),               # sign-flipped variant
    ("g3: x - f(x)/f'(x)",   x - f_expr / f_prime),     # Newton-like damping
]

# ── Path B: user supplies g(x) directly ──────────────────────────────
phi = sp.sympify("(x**2 - 1) / 3")

# Interval and midpoint
a, b = -1.0, 1.0
p0   = (a + b) / 2.0   # starting guess — chosen in Stage 2
""", language="python")

    # ── Stage 1 ─────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Stage 1 — Global Condition Checks (Theorems 2.2 & 2.3)")
    st.markdown(
        "100 evenly-spaced test points are generated across **[a, b]** using `np.linspace`. "
        "Two conditions are checked numerically across all points:"
    )
    st.markdown(
        "- **Condition 1 (Thm 2.2 i):** g(x) maps [a, b] into itself — "
        "`g(x) ∈ [a, b]` for all x ∈ [a, b]\n"
        "- **Condition 2 (Thm 2.2 ii / 2.3):** A Lipschitz constant k < 1 exists — "
        "`max |g′(x)| < 1` on (a, b)"
    )
    st.code("""# Convert symbolic g(x) and g'(x) to fast numeric callables
phi_num    = sp.lambdify(x, phi,              "numpy")
gprime_num = sp.lambdify(x, sp.diff(phi, x), "numpy")

# Generate 100 test points uniformly across [a, b]
x_vals = np.linspace(a, b, 100)

# Evaluate g(x) and |g'(x)| at every test point
g_vals      = np.array([float(phi_num(xi))    for xi in x_vals])
gprime_vals = np.array([float(gprime_num(xi)) for xi in x_vals])

# ── Condition 1: closed mapping — g(x) ∈ [a, b] (Theorem 2.2 i) ─────────
g_min      = float(np.nanmin(g_vals))
g_max      = float(np.nanmax(g_vals))
is_closed  = (g_min >= a) and (g_max <= b)

# ── Condition 2: contraction — k < 1 (Theorem 2.2 ii / 2.3) ─────────
k              = float(np.nanmax(np.abs(gprime_vals)))   # Lipschitz constant
is_contraction = k < 1.0

print(f"Condition 1 — g(x) ∈ [{a}, {b}]:     {'PASS' if is_closed else 'FAIL'}")
print(f"  g(x) range on [a,b]: [{g_min:.6f}, {g_max:.6f}]")
print()
print(f"Condition 2 — k = max|g′(x)| < 1:  {'PASS' if is_contraction else 'FAIL'}")
print(f"  k = {k:.6f}")

both_pass = is_closed and is_contraction
if both_pass:
    print("\n✅ Both conditions satisfied — unique fixed point guaranteed in [a, b].")
else:
    print("\n❌ Conditions not met — adjust [a, b] or choose a different g(x).")
""", language="python")

    # ── Stage 2 ─────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Stage 2 — Initialisation & Iteration Loop")
    st.markdown(
        "If both conditions pass, Theorem 2.3 guarantees convergence from **any** "
        "starting point in [a, b]. The user may optionally supply a custom x₀; "
        "otherwise the midpoint `(a + b) / 2` is used as the canonical fallback. "
        "The recurrence **pₙ = g(pₙ₋₁)** then runs until `|pₙ − pₙ₋₁| < ε` "
        "or the iteration cap is reached."
    )
    st.code("""import math

# Guard: only iterate if both theorem conditions are satisfied
if not both_pass:
    raise RuntimeError("Convergence conditions not met — cannot guarantee a root.")

# Compile g(x) into a fast numeric function for the loop
phi_func = sp.lambdify(x, phi, "math")

# ── Determine starting point ─────────────────────────────────────────
# Check if user provided a custom x0
if use_custom_x0:
    if a <= user_x0 <= b:
        p0 = user_x0                    # user-supplied starting point
    else:
        raise ValueError("x0 must be within [a, b]")   # shown as st.error + st.stop()
else:
    p0 = (a + b) / 2.0                 # fallback: midpoint of the interval

# Solver parameters
tolerance      = 1e-6
max_iterations = 100

p_current = p0

for step in range(1, max_iterations + 1):
    p_next = phi_func(p_current)        # apply g: pₙ = g(pₙ₋₁)

    if abs(p_next - p_current) < tolerance:
        print(f"✅ Root found: p* ≈ {p_next:.8f}  (converged in {step} iterations)")
        break

    p_current = p_next

else:
    print(f"🛑 Did not converge within {max_iterations} iterations.")
""", language="python")

    # ── Corollary ──────────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Corollary — Error Bound")
    st.markdown(
        "Once `k` is known, Theorem 2.3's corollary gives a rigorous upper bound "
        "on the error after `n` iterations:"
    )
    st.code("""# Error bound after n iterations (Corollary to Theorem 2.3):
#
#   |pₙ − p| ≤ (kⁿ / (1 − k)) · |p₁ − p₀|
#
# This bound holds for any p₀ ∈ [a, b].

p1          = phi_func(p0)
first_step  = abs(p1 - p0)
n           = step                           # actual iterations taken

error_bound = (k**n / (1 - k)) * first_step
print(f"Error bound after {n} iterations: |pₙ − p| ≤ {error_bound:.2e}")
""", language="python")

    # ── Key Libraries ──────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Key Libraries")
    st.markdown(
        "| Library | Role |\n"
        "|---|---|\n"
        "| `numpy.linspace()` | Generate 100 uniform test points over [a, b] |\n"
        "| `numpy.nanmax / nanmin` | Find g(x) range and k = max\\|g′\\| safely |\n"
        "| `sympy.sympify()` | Parse user string → symbolic expression |\n"
        "| `sympy.diff()` | Exact symbolic differentiation for g′(x) |\n"
        "| `sympy.lambdify()` | Compile symbolic expr → fast numeric function |\n"
        "| `math` (via lambdify) | Backend for the iteration loop |\n"
    )

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — SOLVER
# ══════════════════════════════════════════════════════════════════════
with tab_solver:

    mode_label = "f(x) mode — auto-generate g(x)" if use_fx else "g(x) mode — direct iteration"
    st.markdown(f'<div class="mode-pill">{"📥 " + mode_label}</div>', unsafe_allow_html=True)

    # Live preview metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        label = "f(x)" if use_fx else "g(x)"
        st.metric(label, equation_input if equation_input else "—")
    with c2:
        st.metric("Interval a", f"{a_val:.4f}")
    with c3:
        st.metric("Interval b", f"{b_val:.4f}")
    with c4:
        st.metric("Tolerance ε", f"{tol:.0e}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Calculation block ────────────────────────────────────────────────────
    if calculate:
        if not equation_input.strip():
            st.error("⚠️  Please enter an equation in the sidebar before calculating.")
            st.stop()

        x = sp.symbols('x')

        # ╔══════════════════════════════════════════════════════════╗
        # ║  PATH A — f(x) input                                    ║
        # ╚══════════════════════════════════════════════════════════╝
        if use_fx:
            # Only re-run expensive SymPy work when button was just pressed
            # (candidates not in state yet). Radio-widget reruns restore from state.
            if st.session_state["candidates"] is None:
                with st.spinner("Parsing f(x) and generating g(x) candidates…"):
                    try:
                        f_expr  = sp.sympify(equation_input)
                        f_prime = sp.diff(f_expr, x)
                    except Exception:
                        st.error(
                            "⚠️  **Could not parse f(x).** "
                            "Check the Syntax Reference — use `x**2` not `x^2`."
                        )
                        st.stop()

                    # ── Auto-generate candidates ────────────────────────────
                    candidates_raw = [
                        ("g₁(x) = x − f(x)",         x - f_expr),
                        ("g₂(x) = x + f(x)",         x + f_expr),
                    ]
                    # Newton-like candidate: only add if f′ is not trivially zero
                    try:
                        g3 = x - f_expr / f_prime
                        # quick check: evaluates at midpoint without error?
                        g3.subs(x, (a_val + b_val) / 2).evalf()
                        candidates_raw.append(("g₃(x) = x − f(x)/f′(x)", g3))
                    except Exception:
                        pass  # f′ = 0 or undefined at midpoint — skip g₃

                    # ── Evaluate interval conditions for each candidate ───────
                    candidates = []   # (label, expr, k_val, viable)
                    for label_c, expr_c in candidates_raw:
                        try:
                            chk_c  = check_interval_conditions(expr_c, x, a_val, b_val)
                            k_val  = chk_c["k"]
                            viable = chk_c["both_pass"]
                        except Exception:
                            k_val, viable = float('inf'), False
                        candidates.append((label_c, expr_c, k_val, viable))

                    # Persist so radio-widget reruns can restore without recomputing
                    st.session_state["candidates"] = candidates

            # Restore from state (covers button-press AND all radio-widget reruns)
            candidates = st.session_state["candidates"]

            # ── Display candidate table ───────────────────────────────
            st.markdown('<div class="panel-label">🔬 Auto-Generated g(x) Candidates</div>',
                        unsafe_allow_html=True)

            header = (
                '<table class="cand-table">'
                '<thead><tr>'
                '<th>Candidate</th><th>k = max|g′| on [a,b]</th><th>Global Convergence</th><th>Formula</th>'
                '</tr></thead><tbody>'
            )
            rows_t = ""
            for lbl, expr_c, dval, viable in candidates:
                tag   = '<span class="tag-ok">✅ viable</span>' if viable else '<span class="tag-bad">❌ diverges</span>'
                speed = ""
                if viable:
                    speed = " · fast" if dval < 0.5 else " · slow"
                rows_t += (
                    f'<tr>'
                    f'<td><strong>{lbl}</strong></td>'
                    f'<td>{dval:.6f}</td>'
                    f'<td>{tag}{speed}</td>'
                    f'<td><code>{sp.pretty(expr_c, use_unicode=False)}</code></td>'
                    f'</tr>'
                )
            st.markdown(header + rows_t + "</tbody></table>", unsafe_allow_html=True)
            st.markdown("")

            # ── Let the user pick a viable candidate ─────────────────────
            viable_candidates = [(lbl, expr_c, dval) for lbl, expr_c, dval, v in candidates if v]

            if not viable_candidates:
                st.error(
                    f"❌ **None of the auto-generated candidates satisfy Theorems 2.2/2.3 "
                    f"on [{a_val}, {b_val}].** Try a wider or different interval, "
                    "or switch to g(x) mode and provide a custom rearrangement."
                )
                st.stop()

            choice_labels = [lbl for lbl, _, _ in viable_candidates]
            chosen_label  = st.radio(
                "Select a viable g(x) to iterate with:",
                options=choice_labels,
                help="Only candidates with |g′(x₀)| < 1 are shown.",
            )

            chosen_idx   = choice_labels.index(chosen_label)
            phi_chosen   = viable_candidates[chosen_idx][1]
            deriv_chosen = viable_candidates[chosen_idx][2]

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # ── Theorem 2.2 / 2.3 check for chosen candidate ─────────────
            chk_chosen = check_interval_conditions(phi_chosen, x, a_val, b_val)
            can_iterate = display_theorem_check(chk_chosen, a_val, b_val)

            if not can_iterate:
                st.stop()

            # ── Resolve starting point: custom x₀ or midpoint ────────────
            if use_custom_x0:
                if not (a_val <= x0_custom <= b_val):
                    st.error(
                        f"⚠️  **x₀ = {x0_custom} is outside [{a_val}, {b_val}].** "
                        "Your custom initial guess must satisfy a ≤ x₀ ≤ b. "
                        "Adjust x₀ or widen the interval."
                    )
                    st.stop()
                x0_start = x0_custom
                x0_label = f"custom x₀ = {x0_start:.6f}"
            else:
                x0_start = (a_val + b_val) / 2.0
                x0_label = f"midpoint x₀ = {x0_start:.6f}"

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.spinner(f"Iterating with {chosen_label} from {x0_label} (ε = {tol:.0e})…"):
                found_root, iterations = run_iteration(phi_chosen, x, x0_start, max_iter, tol)

            display_results(found_root, iterations, chk_chosen["k"], tol)

        # ╔══════════════════════════════════════════════════════════╗
        # ║  PATH B — g(x) input (original flow, unchanged)         ║
        # ╚══════════════════════════════════════════════════════════╝
        else:
            # Only re-parse when button was just pressed; restore from state otherwise.
            if st.session_state["phi_gx"] is None:
                with st.spinner("Parsing g(x)…"):
                    try:
                        phi = sp.sympify(equation_input)
                        # quick validity check
                        phi.subs(sp.Symbol('x'), (a_val + b_val) / 2).evalf()
                    except Exception:
                        st.error(
                            "⚠️  **Invalid expression.** Could not parse g(x). "
                            "Check the Syntax Reference — use `x**2` not `x^2`."
                        )
                        st.stop()

                    # Persist the expression string
                    st.session_state["phi_gx"] = str(phi)

            # Restore from state
            x   = sp.symbols('x')
            phi = sp.sympify(st.session_state["phi_gx"])

            # ── Theorem 2.2 / 2.3 check over [a, b] ──────────────────────
            try:
                chk = check_interval_conditions(phi, x, a_val, b_val)
            except Exception as e:
                st.error(f"⚠️  Could not evaluate g(x) on [{a_val}, {b_val}]: {e}")
                st.stop()

            can_iterate = display_theorem_check(chk, a_val, b_val)

            if not can_iterate:
                st.stop()

            # ── Resolve starting point: custom x₀ or midpoint ────────────
            if use_custom_x0:
                if not (a_val <= x0_custom <= b_val):
                    st.error(
                        f"⚠️  **x₀ = {x0_custom} is outside [{a_val}, {b_val}].** "
                        "Your custom initial guess must satisfy a ≤ x₀ ≤ b. "
                        "Adjust x₀ or widen the interval."
                    )
                    st.stop()
                x0_start = x0_custom
                x0_label = f"custom x₀ = {x0_start:.6f}"
            else:
                x0_start = (a_val + b_val) / 2.0
                x0_label = f"midpoint x₀ = {x0_start:.6f}"

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.spinner(f"Iterating from {x0_label} (ε = {tol:.0e}, max {max_iter} steps)…"):
                found_root, iterations = run_iteration(phi, x, x0_start, max_iter, tol)

            display_results(found_root, iterations, chk["k"], tol)

    else:
        st.info(
            "👈  **Choose your input mode and enter an equation in the sidebar**, "
            "set the interval [a, b], then click **▶ Find Root**. "
            "The solver will verify Theorems 2.2 & 2.3 before iterating."
        )