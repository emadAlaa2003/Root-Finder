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

    x0_val = st.number_input(
        "Initial guess x₀",
        value=0.75,
        step=0.1,
        format="%.4f",
        help="Starting point for convergence testing and iteration.",
    )
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
    ("x0_cache",      None),    # x0 used in the last calculation
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
    or st.session_state["x0_cache"]     != x0_val
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
    st.session_state["x0_cache"]     = x0_val
    st.session_state["use_fx_cache"] = use_fx


# ════════════════════════════════════════════════════════════════════════
# HELPER — run the iteration loop (shared by both paths)
# ════════════════════════════════════════════════════════════════════════
def run_iteration(phi_sym, x_sym, x0, max_it, tolerance):
    """
    Returns (found_root: bool, iterations: list of (step, value)).
    """
    phi_func  = sp.lambdify(x_sym, phi_sym, "math")
    x_current = x0
    iterations = []
    found_root = False
    
    for step in range(1, max_it + 1):
        try:
            x_next = phi_func(x_current)
        except OverflowError:
            # إذا انفجرت الأرقام، نوقف الـ Loop فوراً
            break
            
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
            st.metric("📉 |g′(x₀)|", f"{deriv_val:.6f}")
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
# TAB 1 — SOLVER
# ══════════════════════════════════════════════════════════════════════
with tab_solver:

    mode_label = "f(x) mode — auto-generate g(x)" if use_fx else "g(x) mode — direct iteration"
    st.markdown(f'<div class="mode-pill">{"📥 " + mode_label}</div>', unsafe_allow_html=True)

    # Live preview metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        label = "f(x)" if use_fx else "g(x)"
        st.metric(label, equation_input if equation_input else "—")
    with c2:
        st.metric("Initial guess x₀", f"{x0_val:.4f}")
    with c3:
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
                        # quick check: does it evaluate at x0?
                        g3.subs(x, x0_val).evalf()
                        candidates_raw.append(("g₃(x) = x − f(x)/f′(x)", g3))
                    except Exception:
                        pass  # f′ = 0 or undefined at x₀ — skip g₃

                    # ── Evaluate convergence for each candidate ───────────
                    candidates = []   # (label, expr, deriv_val, viable)
                    for label_c, expr_c in candidates_raw:
                        try:
                            gprime  = sp.diff(expr_c, x)
                            dval    = float(abs(gprime.subs(x, x0_val).evalf()))
                            viable  = dval < 1.0
                        except Exception:
                            dval, viable = float('inf'), False
                        candidates.append((label_c, expr_c, dval, viable))

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
                '<th>Candidate</th><th>|g′(x₀)|</th><th>Convergence</th><th>Formula</th>'
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
                    "❌ **None of the auto-generated candidates converge** at x₀ = "
                    f"{x0_val}. Try a different initial guess, or switch to g(x) mode "
                    "and provide a custom rearrangement."
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

            # ── Show convergence badge for chosen candidate ───────────────
            st.markdown('<div class="panel-label">📊 Convergence Analysis — chosen g(x)</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="deriv-chip">'
                f'<span class="label">|g′(x₀)|</span>'
                f'= &nbsp;<strong>{deriv_chosen:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )
            _, badge_html, _ = convergence_badge(deriv_chosen)
            st.markdown(badge_html, unsafe_allow_html=True)

            # ── Run iteration ─────────────────────────────────────────────
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.spinner(f"Iterating with {chosen_label} (ε = {tol:.0e})…"):
                found_root, iterations = run_iteration(phi_chosen, x, x0_val, max_iter, tol)

            display_results(found_root, iterations, deriv_chosen, tol)

        # ╔══════════════════════════════════════════════════════════╗
        # ║  PATH B — g(x) input (original flow, unchanged)         ║
        # ╚══════════════════════════════════════════════════════════╝
        else:
            # Only re-parse and check convergence when button was just pressed.
            # On every other rerun, restore the already-computed values from state.
            if st.session_state["phi_gx"] is None:
                with st.spinner("Analysing convergence…"):
                    try:
                        phi       = sp.sympify(equation_input)
                        phi_prime = sp.diff(phi, x)
                        deriv_val = float(abs(phi_prime.subs(x, x0_val).evalf()))
                    except Exception:
                        st.error(
                            "⚠️  **Invalid expression.** Could not parse g(x). "
                            "Check the Syntax Reference — use `x**2` not `x^2`."
                        )
                        st.stop()

                    run_loop, _, _ = convergence_badge(deriv_val)

                    # Persist to survive future reruns
                    st.session_state["phi_gx"]       = str(phi)
                    st.session_state["deriv_val_gx"] = deriv_val
                    st.session_state["run_loop_gx"]  = run_loop

            # Restore from state (valid on button-press AND all subsequent reruns)
            x         = sp.symbols('x')
            phi       = sp.sympify(st.session_state["phi_gx"])
            deriv_val = st.session_state["deriv_val_gx"]
            run_loop  = st.session_state["run_loop_gx"]

            # Convergence analysis display
            st.markdown('<div class="panel-label">📊 Convergence Analysis</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="deriv-chip">'
                f'<span class="label">|g′(x₀)|</span>'
                f'= &nbsp;<strong>{deriv_val:.6f}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

            _, badge_html, _ = convergence_badge(deriv_val)
            st.markdown(badge_html, unsafe_allow_html=True)

            if not run_loop:
                st.error(
                    "The Banach condition **|g′(x₀)| < 1** is not satisfied. "
                    "The iteration will **diverge**. Try a different g(x) or starting point."
                )
                st.stop()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.spinner(f"Iterating (ε = {tol:.0e}, max {max_iter} steps)…"):
                found_root, iterations = run_iteration(phi, x, x0_val, max_iter, tol)

            display_results(found_root, iterations, deriv_val, tol)

    else:
        st.info(
            "👈  **Choose your input mode and enter an equation in the sidebar**, "
            "set your initial guess, then click **▶ Find Root**."
        )


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — CORE ALGORITHM
# ══════════════════════════════════════════════════════════════════════
with tab_algo:

    st.markdown("## 💻 Core Algorithm — Fixed-Point Iteration")
    st.markdown(
        "Pure backend logic, stripped of all UI code. "
        "The solver now branches into **two paths** based on the user's input mode."
    )

    st.markdown("---")
    st.markdown("### Stage 0 — Select Input Mode")
    st.markdown("The user chooses whether to provide **f(x)** or **g(x)**.")
    st.code("""\
# 'fx' or 'gx' — determined by the sidebar radio button
mode = "fx"   # or "gx"
""", language="python")

    st.markdown("---")
    st.markdown("### Path A — f(x) Input: Auto-Generate g(x) Candidates")
    st.markdown(
        "Parse f(x), compute f′(x), then build candidate iteration functions. "
        "Each candidate is tested for the Banach condition at x₀."
    )
    st.code("""\
import sympy as sp

x = sp.symbols('x')
f_expr  = sp.sympify(equation_input)   # e.g. x**3 - x - 1
f_prime = sp.diff(f_expr, x)

# --- Auto-generate candidates ---
candidates_raw = [
    ("g1 = x - f(x)",         x - f_expr),
    ("g2 = x + f(x)",         x + f_expr),
    ("g3 = x - f(x)/f'(x)",  x - f_expr / f_prime),   # Newton-like
]

# --- Test convergence for each ---
for label, g_expr in candidates_raw:
    g_prime = sp.diff(g_expr, x)
    dval    = float(abs(g_prime.subs(x, x0_val).evalf()))
    viable  = dval < 1.0
    print(f"{label}  |g'(x0)| = {dval:.6f}  viable={viable}")
""", language="python")

    st.markdown("---")
    st.markdown("### Path B — g(x) Input: Direct Convergence Check")
    st.markdown(
        "Parse g(x) directly, evaluate |g′(x₀)|, and decide whether to proceed."
    )
    st.code("""\
phi       = sp.sympify(equation_input)   # e.g. (1 - x**2)**(1/3)
phi_prime = sp.diff(phi, x)
deriv_val = float(abs(phi_prime.subs(x, x0_val).evalf()))

if deriv_val < 0.5:
    print("Fast convergence  ✅  |g'| < 0.5")
elif deriv_val < 1.0:
    print("Slow convergence  ⚠️   0.5 ≤ |g'| < 1")
else:
    print("Divergence        ❌  |g'| ≥ 1 — will not converge")
""", language="python")

    st.markdown("---")
    st.markdown("### Stage C — Iteration Loop (shared by both paths)")
    st.markdown(
        "`sp.lambdify()` compiles the symbolic g(x) into a fast numeric callable. "
        "The recurrence **xₙ₊₁ = g(xₙ)** runs until |xₙ₊₁ − xₙ| < ε or the cap is hit."
    )
    st.code("""\
phi_func  = sp.lambdify(x, phi, "math")   # fast numeric function
x_current = x0_val
tolerance = 1e-6
max_iterations = 100

for step in range(1, max_iterations + 1):
    x_next = phi_func(x_current)

    if abs(x_next - x_current) < tolerance:
        print(f"Root found after {step} iterations: x* ≈ {x_next:.8f}")
        break

    x_current = x_next
else:
    print("Did not converge within the maximum number of iterations.")
""", language="python")

    st.markdown("---")
    st.markdown("### Key Libraries")
    st.markdown(
        "| Library | Role |\n"
        "|---|---|\n"
        "| `sympy.sympify()` | Parse string → symbolic expression |\n"
        "| `sympy.diff()` | Exact symbolic differentiation |\n"
        "| `sympy.lambdify()` | Compile symbolic expr → fast numeric function |\n"
        "| `math` (via lambdify) | Backend for numerical evaluation |"
    )
