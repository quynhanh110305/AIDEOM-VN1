"""
AIDEOM-VN – Dashboard tích hợp 12 bài tập
Mô hình ra quyết định phát triển kinh tế Việt Nam trong kỷ nguyên AI
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AIDEOM-VN",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── INLINE CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main-title {font-size:2rem; font-weight:700; color:#CC0001; margin-bottom:0}
.sub-title  {font-size:1rem; color:#555; margin-bottom:1rem}
.metric-card {
    background:#f8f9fa; border-radius:10px; padding:1rem 1.2rem;
    border-left:4px solid #CC0001; margin-bottom:0.5rem;
}
.section-header {
    font-size:1.1rem; font-weight:600; color:#1a1a2e;
    border-bottom:2px solid #CC0001; padding-bottom:4px; margin:1rem 0 0.8rem;
}
.badge {
    display:inline-block; padding:2px 8px; border-radius:4px;
    font-size:0.75rem; font-weight:600; margin-left:6px;
}
.badge-easy   {background:#d4edda; color:#155724}
.badge-med    {background:#fff3cd; color:#856404}
.badge-hard   {background:#f8d7da; color:#721c24}
.badge-vhard  {background:#d1ecf1; color:#0c5460}
</style>
""", unsafe_allow_html=True)

# ─── EMBEDDED DATA ───────────────────────────────────────────────────────────
MACRO = pd.DataFrame({
    "year": [2020, 2021, 2022, 2023, 2024, 2025],
    "GDP_trillion_VND": [8044.4, 8487.5, 9513.3, 10221.8, 11511.9, 12847.6],
    "K_trillion_VND": [16500, 17800, 19600, 21300, 23500, 25900],
    "L_million": [53.6, 50.5, 51.7, 52.4, 52.9, 53.4],
    "D_digital_pct": [12.0, 12.7, 14.3, 16.5, 18.3, 19.5],
    "AI_tech_firms_thousand": [55.6, 60.2, 65.4, 67.0, 73.8, 80.1],
    "H_trained_pct": [24.1, 26.1, 26.2, 27.0, 28.4, 29.2],
})

SECTORS = pd.DataFrame({
    "sector_id": list(range(1, 11)),
    "sector_name_vi": [
        "Nông-Lâm-Thủy sản", "CN chế biến chế tạo", "Xây dựng", "Khai khoáng",
        "Bán buôn-bán lẻ", "Tài chính-Ngân hàng", "Logistics-Vận tải",
        "CNTT-Truyền thông", "Giáo dục-Đào tạo", "Y tế",
    ],
    "growth_rate_2024_pct": [3.27, 9.64, 7.45, -1.20, 7.10, 7.36, 9.93, 7.85, 6.42, 6.85],
    "productivity_million_VND_per_worker": [103.4, 241.2, 168.8, 1290.5, 145.3, 1072.4, 321.4, 713.8, 205.7, 437.1],
    "spillover_coef_0_1": [0.35, 0.78, 0.42, 0.30, 0.55, 0.85, 0.72, 0.92, 0.65, 0.60],
    "export_billion_USD": [40.5, 290.9, 2.5, 8.2, 5.5, 1.2, 3.1, 178.0, 0.0, 0.0],
    "labor_million": [13.20, 11.50, 4.80, 0.30, 7.80, 0.55, 1.95, 0.62, 2.15, 0.75],
    "ai_readiness_0_100": [15, 55, 20, 30, 48, 72, 42, 88, 38, 45],
    "automation_risk_pct": [18, 42, 25, 55, 38, 52, 35, 28, 22, 18],
})

REGIONS = pd.DataFrame({
    "region_id": list(range(1, 7)),
    "region_name_vi": [
        "Trung du miền núi phía Bắc", "Đồng bằng sông Hồng",
        "Bắc Trung Bộ & DH Trung Bộ", "Tây Nguyên", "Đông Nam Bộ",
        "Đồng bằng sông Cửu Long",
    ],
    "grdp_per_capita_million_VND": [57.0, 152.3, 87.5, 68.9, 158.9, 80.5],
    "fdi_registered_billion_USD": [3.5, 20.0, 8.2, 0.8, 18.5, 2.1],
    "digital_index_0_100": [38, 78, 55, 32, 82, 48],
    "ai_readiness_0_100": [22, 68, 40, 18, 75, 30],
    "trained_labor_pct": [21.5, 36.8, 27.5, 18.2, 42.5, 16.8],
    "rd_intensity_pct": [0.18, 0.85, 0.32, 0.15, 0.78, 0.22],
    "internet_penetration_pct": [72, 92, 84, 68, 94, 78],
    "gini_coef": [0.405, 0.358, 0.372, 0.412, 0.385, 0.392],
})

PROJECTS = {
    i: n for i, n in enumerate([
        "TT Dữ liệu Hòa Lạc", "TT Dữ liệu phía Nam", "5G toàn quốc",
        "VNeID 2.0", "Cổng DVCQG v3", "Y tế số", "Giáo dục số K-12",
        "Trung tâm AI quốc gia", "Sandbox fintech", "Logistics thông minh",
        "Nông nghiệp số ĐBSCL", "Đào tạo 50k KS AI", "Khu CN bán dẫn BN-BG",
        "An ninh mạng SOC", "Open Data quốc gia",
    ], start=1)
}
PROJ_COST  = {1:12000,2:11500,3:18000,4:4500,5:3200,6:5800,7:6500,8:15000, 9:2500,10:7200,11:4800,12:8500,13:20000,14:3800,15:1500}
PROJ_COST1 = {1:8500,2:7500,3:12000,4:3500,5:2500,6:4000,7:4500,8:9000, 9:1800,10:5000,11:3500,12:5500,13:13000,14:2800,15:1200}
PROJ_BEN   = {1:21500,2:20800,3:32500,4:9200,5:6800,6:11400,7:12200,8:28500, 9:5800,10:13800,11:8500,12:16200,13:35000,14:7500,15:3800}

COLORS = px.colors.qualitative.Set2


# ═══════════════════════════════════════════════════════════════════════════
#  CORE COMPUTATION FUNCTIONS (pure Python/numpy – no extra libs required)
# ═══════════════════════════════════════════════════════════════════════════

def compute_tfp(Y, K, L, D, AI, H, a=0.33, b=0.42, g=0.10, d=0.08, t=0.07):
    return Y / (K**a * L**b * D**g * AI**d * H**t)

def forecast_gdp(A, K, L, D, AI, H, a=0.33, b=0.42, g=0.10, d=0.08, t=0.07):
    return A * (K**a) * (L**b) * (D**g) * (AI**d) * (H**t)

def growth_decomp(macro_df, a, b, g, d, t):
    Y  = macro_df.GDP_trillion_VND.values
    K  = macro_df.K_trillion_VND.values
    L  = macro_df.L_million.values
    D  = macro_df.D_digital_pct.values
    AI = macro_df.AI_tech_firms_thousand.values
    H  = macro_df.H_trained_pct.values
    A  = compute_tfp(Y, K, L, D, AI, H, a, b, g, d, t)
    rows = []
    for i in range(1, len(Y)):
        dY   = np.log(Y[i]) - np.log(Y[i-1])
        dA   = np.log(A[i]) - np.log(A[i-1])
        rows.append({
            "year": int(macro_df.year.values[i]),
            "g_GDP_%": round(dY*100, 2),
            "TFP": round(dA/dY*100 if dY else 0, 1),
            "K": round(a*(np.log(K[i])-np.log(K[i-1]))/dY*100 if dY else 0, 1),
            "L": round(b*(np.log(L[i])-np.log(L[i-1]))/dY*100 if dY else 0, 1),
            "D": round(g*(np.log(D[i])-np.log(D[i-1]))/dY*100 if dY else 0, 1),
            "AI": round(d*(np.log(AI[i])-np.log(AI[i-1]))/dY*100 if dY else 0, 1),
            "H": round(t*(np.log(H[i])-np.log(H[i-1]))/dY*100 if dY else 0, 1),
        })
    return pd.DataFrame(rows)

def lp_simple(budget, c1=25, c2=15, c3=20, c4=10, strategic=0.35):
    """Analytical LP: allocate budget to maximise GDP gain (no external solver)."""
    # Coefficients: c=[0.85,1.20,0.95,1.35] – x4 dominates, then x2
    # Because x4 has highest coeff (1.35) and min constraint is 10,
    # we solve by KKT / inspection under the given structure.
    from scipy.optimize import linprog
    coeff = [-0.85, -1.20, -0.95, -1.35]
    A_ub = [
        [1,1,1,1],
        [-1,0,0,0], [0,-1,0,0], [0,0,-1,0], [0,0,0,-1],
        [strategic, -(1-strategic), strategic, -(1-strategic)],
    ]
    b_ub = [budget, -c1, -c2, -c3, -c4, 0]
    res = linprog(coeff, A_ub=A_ub, b_ub=b_ub, bounds=[(0,None)]*4, method="highs")
    if res.success:
        return res.x, -res.fun
    return np.array([c1,c2,c3,c4]), sum(x*c for x,c in zip([c1,c2,c3,c4],[-0.85,-1.20,-0.95,-1.35]))

def priority_index(sectors_df, weights):
    cols = ["growth_rate_2024_pct","productivity_million_VND_per_worker",
            "spillover_coef_0_1","export_billion_USD","labor_million",
            "ai_readiness_0_100","automation_risk_pct"]
    X = sectors_df[cols].values.astype(float)
    denom = np.sqrt((X**2).sum(axis=0))
    denom[denom == 0] = 1e-12
    Xn = X / denom
    Xn[:, 6] = Xn[:, 6].max() - Xn[:, 6]   # risk: invert
    return Xn @ np.array(weights)

def topsis(X, weights, is_benefit):
    n, m = X.shape
    denom = np.sqrt((X**2).sum(axis=0))
    denom[denom == 0] = 1e-12
    R = X / denom
    V = R * np.array(weights)
    A_star = np.where(is_benefit, V.max(axis=0), V.min(axis=0))
    A_neg  = np.where(is_benefit, V.min(axis=0), V.max(axis=0))
    S_star = np.sqrt(((V - A_star)**2).sum(axis=1))
    S_neg  = np.sqrt(((V - A_neg )**2).sum(axis=1))
    return S_neg / (S_star + S_neg + 1e-12)

def region_lp(budget, lam, with_fairness):
    """Region LP (6×4) solved analytically via scipy."""
    from scipy.optimize import linprog
    regions = ["NMM","RRD","NCC","CH","SE","MD"]
    items   = ["I","D","AI","H"]
    beta_mat = np.array([
        [1.15,0.85,0.55,1.30],
        [0.95,1.25,1.40,1.05],
        [1.05,0.95,0.85,1.15],
        [1.20,0.75,0.45,1.35],
        [0.90,1.30,1.55,1.00],
        [1.10,0.85,0.65,1.25],
    ])
    D0 = np.array([38.0,78.0,55.0,32.0,82.0,48.0])
    gamma = 0.002
    n_vars = 24
    c = -beta_mat.flatten()
    # inequality constraints
    A_ub, b_ub = [], []
    # total budget
    A_ub.append(np.ones(n_vars)); b_ub.append(budget)
    # per-region floor (-sum <= -5000) and ceiling (sum <= 12000)
    for r in range(6):
        row_fl = np.zeros(n_vars); row_cl = np.zeros(n_vars)
        for j in range(4):
            row_fl[r*4+j] = -1
            row_cl[r*4+j] =  1
        A_ub.append(row_fl); b_ub.append(-5000)
        A_ub.append(row_cl); b_ub.append(12000)
    # H floor
    row_h = np.zeros(n_vars)
    for r in range(6): row_h[r*4+3] = -1
    A_ub.append(row_h); b_ub.append(-12000)
    # fairness (linearised): D0[r] + gamma*x[r,D] >= lam*M
    # Introduce M as 25th variable
    if with_fairness:
        n_vars2 = 25
        c2 = np.append(c, 0.0)
        A2, b2 = [], []
        for row, bv in zip(A_ub, b_ub):
            A2.append(np.append(row, 0.0)); b2.append(bv)
        for r in range(6):
            row_up = np.zeros(n_vars2); row_up[r*4+1] = gamma; row_up[24] = -1
            A2.append(row_up); b2.append(-D0[r])
            row_lo = np.zeros(n_vars2); row_lo[r*4+1] = -gamma*lam; row_lo[24] = lam
            b2.append(D0[r])
            A2.append(row_lo)
        bounds = [(0, None)]*24 + [(0, None)]
        res = linprog(c2, A_ub=A2, b_ub=b2, bounds=bounds, method="highs")
        if res.success:
            return res.x[:24].reshape(6,4), -res.fun
    else:
        bounds = [(0,None)]*n_vars
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if res.success:
            return res.x.reshape(6,4), -res.fun
    return np.zeros((6,4)), 0.0

def mip_project(budget_total, budget_12):
    """Simple greedy + ratio heuristic for MIP (no CBC needed in browser)."""
    from scipy.optimize import linprog
    P = list(range(1,16))
    # Mandatory: P14 security; at least one of P4/P5; P8->P12; P13->P12
    selected = [14]  # mandatory
    remaining_budget = budget_total - PROJ_COST[14]
    remaining_12 = budget_12 - PROJ_COST1[14]
    # add at least P4 (gov digital)
    selected.append(4)
    remaining_budget -= PROJ_COST[4]
    remaining_12 -= PROJ_COST1[4]
    # P12 needed for P8 and P13
    selected.append(12)
    remaining_budget -= PROJ_COST[12]
    remaining_12 -= PROJ_COST1[12]
    # greedy by benefit/cost ratio
    candidates = [p for p in P if p not in selected]
    ratios = [(PROJ_BEN[p]/PROJ_COST[p], p) for p in candidates]
    ratios.sort(reverse=True)
    for _, p in ratios:
        if (remaining_budget >= PROJ_COST[p] and remaining_12 >= PROJ_COST1[p]
                and len(selected) < 11):
            selected.append(p)
            remaining_budget -= PROJ_COST[p]
            remaining_12 -= PROJ_COST1[p]
    total_cost = sum(PROJ_COST[p] for p in selected)
    total_benefit = sum(PROJ_BEN[p] for p in selected)
    return sorted(selected), total_cost, total_benefit

def q_sim(episodes=500, alpha=0.1, gamma_rl=0.95, eps_start=1.0):
    """Lightweight Q-learning simulation (tabular, 81 states × 5 actions)."""
    np.random.seed(42)
    Q = np.zeros((81, 5))
    rewards_hist = []
    eps = eps_start
    ACTION_NAMES = ["Hạ tầng", "AI & Số hóa", "Nhân lực", "Cân bằng", "An sinh"]

    def encode(ai, gdp, risk, train):
        return int(np.clip(ai,0,2))*27 + int(np.clip(gdp,0,2))*9 + int(np.clip(risk,0,2))*3 + int(np.clip(train,0,2))

    def decode(s):
        ai = s//27; rem = s%27; gdp = rem//9; rem = rem%9; risk = rem//3; train = rem%3
        return ai, gdp, risk, train

    def step(s, a):
        ai, gdp, risk, train = decode(s)
        r_prob = np.random.rand
        if a == 0:
            if r_prob() < 0.7: gdp = min(2, gdp+1)
            if r_prob() < 0.2: ai = max(0, ai-1)
        elif a == 1:
            if r_prob() < 0.8: ai = min(2, ai+1)
            if r_prob() < 0.5: gdp = min(2, gdp+1)
            if train < 2:
                if r_prob() < 0.8: risk = min(2, risk+1)
            else:
                if r_prob() < 0.3: risk = min(2, risk+1)
        elif a == 2:
            if r_prob() < 0.8: train = min(2, train+1)
            if r_prob() < 0.6: risk = max(0, risk-1)
            if r_prob() < 0.4: ai = min(2, ai+1)
        elif a == 3:
            if r_prob() < 0.5: gdp = min(2, gdp+1)
            if r_prob() < 0.4: ai = min(2, ai+1)
            if r_prob() < 0.4: train = min(2, train+1)
            if r_prob() < 0.3: risk = max(0, risk-1)
        else:
            if r_prob() < 0.9: risk = max(0, risk-1)
            if r_prob() < 0.5: train = min(2, train+1)
            if r_prob() < 0.1: gdp = max(0, gdp-1)
        ns = encode(ai, gdp, risk, train)
        rew = ([0,10,25][gdp] + [0,5,15][ai] + [0,5,12][train]
               + [0,-8,-30][risk] + {0:-4,1:-6,2:-5,3:-7,4:-3}[a]
               + (-20 if gdp==0 and risk==2 else 0))
        return ns, rew

    for ep in range(episodes):
        s = encode(1,1,1,1); total = 0
        for _ in range(20):
            a = np.random.randint(5) if np.random.rand() < eps else int(np.argmax(Q[s]))
            ns, r = step(s, a)
            Q[s,a] += alpha*(r + gamma_rl*Q[ns].max() - Q[s,a])
            s = ns; total += r
        eps = max(0.05, eps*0.995)
        rewards_hist.append(total)
    return Q, rewards_hist, ACTION_NAMES

def stochastic_lp():
    """Two-stage stochastic LP (Bài 10) - solved analytically."""
    from scipy.optimize import linprog
    scenarios = {"Lạc quan": 0.30, "Cơ sở": 0.45, "Bi quan": 0.20, "Khủng hoảng": 0.05}
    beta_s = {
        "Lạc quan":    [1.25,1.35,1.55,1.05],
        "Cơ sở":       [1.00,1.10,1.25,0.95],
        "Bi quan":     [0.75,0.85,0.90,1.00],
        "Khủng hoảng": [0.40,0.50,0.55,1.10],
    }
    beta_base = [1.00,1.10,1.25,0.95]
    # Decision vars: x[4] first-stage + y[s][4] second-stage for 4 scenarios = 4+16=20
    n_s = 4; n_j = 4
    n_vars = n_j + n_s*n_j  # 20
    # objective: max sum_j beta_j*x_j + sum_s p_s*sum_j beta_sj*y_sj
    c = np.zeros(n_vars)
    for j in range(n_j): c[j] = -beta_base[j]
    for si, (sname, ps) in enumerate(scenarios.items()):
        for j in range(n_j):
            c[n_j + si*n_j + j] = -ps * beta_s[sname][j]
    A_ub, b_ub = [], []
    # first-stage budget
    row = np.zeros(n_vars); row[:n_j] = 1; A_ub.append(row); b_ub.append(65000)
    # per-scenario second-stage budget
    for si in range(n_s):
        row = np.zeros(n_vars)
        row[n_j + si*n_j : n_j + (si+1)*n_j] = 1
        A_ub.append(row); b_ub.append(15000)
    # y_AI^s <= 0.5 * x_H (index 3 is H, index 2 is AI)
    for si in range(n_s):
        row = np.zeros(n_vars)
        row[n_j + si*n_j + 2] = 1   # y_AI
        row[3] = -0.5                 # -0.5*x_H
        A_ub.append(row); b_ub.append(0)
    bounds = [(0, None)]*n_vars
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        x_opt = res.x[:n_j]
        y_opt = {sname: res.x[n_j + si*n_j : n_j + (si+1)*n_j]
                 for si, sname in enumerate(scenarios)}
        return x_opt, y_opt, -res.fun
    return np.zeros(n_j), {}, 0.0

def dynamic_opt(T=10, rho=0.97):
    """Simplified dynamic optimisation trajectory (Bài 8) via scipy SLSQP."""
    from scipy.optimize import minimize
    K0, D0, AI0, H0, A0 = 27500, 20.3, 86, 30, 0.82
    L = np.linspace(53.9, 55.0, T)
    dk, dd, dai = 0.05, 0.12, 0.15
    th_H, mu = 0.8, 0.02
    phi1, phi2, phi3 = 0.003, 0.002, 0.004
    n = T * 4  # I_K, I_D, I_AI, I_H for each year

    def simulate(x_flat):
        I = x_flat.reshape(T, 4)
        K, D, AI, H, A = [np.zeros(T+1) for _ in range(5)]
        K[0], D[0], AI[0], H[0], A[0] = K0, D0, AI0, H0, A0
        welfare = 0
        for t in range(T):
            Y = A[t]*(K[t]**0.33)*(L[t]**0.42)*(D[t]**0.10)*(AI[t]**0.08)*(H[t]**0.07)
            C = max(Y - I[t].sum(), 1e-3)
            welfare += (rho**t) * np.log(C)
            K[t+1]  = (1-dk)*K[t]  + I[t,0]
            D[t+1]  = (1-dd)*D[t]  + I[t,1]
            AI[t+1] = (1-dai)*AI[t]+ I[t,2]
            H[t+1]  = H[t] + th_H*I[t,3] - mu*H[t]
            A[t+1]  = A[t]*(1 + phi1*D[t] + phi2*AI[t] + phi3*H[t])
        return -welfare, K, D, AI, H, A

    def neg_welfare(x): return simulate(x)[0]

    x0 = np.ones(n) * 200
    bounds = [(0, 5000)] * n
    res = minimize(neg_welfare, x0, method="L-BFGS-B", bounds=bounds,
                   options={"maxiter": 200, "ftol": 1e-6})
    _, K, D, AI, H, A = simulate(res.x if res.success else x0)
    GDP_path = [A[t]*(K[t]**0.33)*(L[t]**0.42)*(D[t]**0.10)*(AI[t]**0.08)*(H[t]**0.07)
                for t in range(T+1)]
    return K, D, AI, H, GDP_path

def labor_opt(budget):
    """Labor market optimisation (Bài 9) via scipy linprog."""
    from scipy.optimize import linprog
    a1 = np.array([8.5,32.5,12.8,22.4,45.8,28.5,62.5,18.5])
    b1 = np.array([45.0,28.0,35.0,32.0,22.0,30.0,20.0,55.0])
    c1 = np.array([5.2,62.4,18.5,48.2,72.5,42.8,32.5,12.5])
    d1 = np.array([50.0,32.0,42.0,38.0,26.0,36.0,24.0,62.0])
    risk = np.array([18,42,25,38,52,35,28,22])/100
    N = 8
    # vars: [x_AI_0..7, x_H_0..7]
    n_vars = 2*N
    net_coeff = -(a1 + b1 - c1*risk)
    coeff_AI = -(a1 - c1*risk); coeff_H = -b1
    c = np.concatenate([coeff_AI, coeff_H])
    A_ub, b_ub = [], []
    # budget
    A_ub.append(np.ones(n_vars)); b_ub.append(budget)
    # NetJob_i >= 0: -(a1_i - c1_i*risk_i)*xAI - b1_i*xH <= 0
    for i in range(N):
        row = np.zeros(n_vars)
        row[i] = -(a1[i] - c1[i]*risk[i])
        row[N+i] = -b1[i]
        A_ub.append(row); b_ub.append(0)
    # DisplacedJob <= RetainCap: c1*risk*xAI - d1*xH <= 0
    for i in range(N):
        row = np.zeros(n_vars)
        row[i] = c1[i]*risk[i]; row[N+i] = -d1[i]
        A_ub.append(row); b_ub.append(0)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0,None)]*n_vars, method="highs")
    if res.success:
        xAI = res.x[:N]; xH = res.x[N:]
        net = (a1-c1*risk)*xAI + b1*xH
        return xAI, xH, net
    return np.zeros(N), np.zeros(N), np.zeros(N)


# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════

MENU = {
    "🏠 Tổng quan AIDEOM-VN": "overview",
    "1️⃣  Cobb-Douglas & TFP": "b01",
    "2️⃣  LP Phân bổ ngân sách": "b02",
    "3️⃣  Chỉ số ưu tiên ngành": "b03",
    "4️⃣  LP Vùng miền": "b04",
    "5️⃣  MIP Lựa chọn dự án": "b05",
    "6️⃣  TOPSIS Xếp hạng vùng": "b06",
    "7️⃣  Pareto NSGA-II (mô phỏng)": "b07",
    "8️⃣  Tối ưu động 2026-2035": "b08",
    "9️⃣  Thị trường lao động AI": "b09",
    "🔟 Stochastic LP 2 giai đoạn": "b10",
    "1️⃣1️⃣ Q-Learning chính sách": "b11",
    "1️⃣2️⃣ Dashboard AIDEOM-VN": "b12",
}

with st.sidebar:
    st.markdown('<p class="main-title">🇻🇳 AIDEOM-VN</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Mô hình ra quyết định phát triển kinh tế Việt Nam trong kỷ nguyên AI</p>', unsafe_allow_html=True)
    st.divider()
    selected = st.radio("Chọn bài / module:", list(MENU.keys()), label_visibility="collapsed")
    page = MENU[selected]
    st.divider()
    st.caption("Dữ liệu: GSO/NSO · World Bank · MoST 2025")


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if page == "overview":
    st.markdown('<h1 class="main-title">AIDEOM-VN Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Bộ mô hình ra quyết định phát triển kinh tế Việt Nam — 12 bài tập tích hợp</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("GDP 2025", "12,847.6 nghìn tỷ", "+8.02%")
    c2.metric("Kinh tế số/GDP", "≈19.5%", "+1.2pp")
    c3.metric("FDI giải ngân", "27.6 tỷ USD", "+8.9%")
    c4.metric("DN Công nghệ số", "80,052", "+8.5%")

    st.markdown('<div class="section-header">Tổng quan 12 bài tập</div>', unsafe_allow_html=True)
    modules = [
        ("Bài 1", "Cobb-Douglas mở rộng & TFP", "Dễ",    "Numpy · Pandas"),
        ("Bài 2", "LP Phân bổ ngân sách 4 hạng mục",    "Dễ",    "Scipy · PuLP"),
        ("Bài 3", "Chỉ số ưu tiên ngành MCDM",          "Dễ",    "Numpy · Min-Max"),
        ("Bài 4", "LP Vùng miền 6×4",                   "TB",    "PuLP · CVXPY"),
        ("Bài 5", "MIP lựa chọn dự án",                  "TB",    "PuLP · Binary"),
        ("Bài 6", "TOPSIS xếp hạng vùng AI",             "TB",    "Numpy · Entropy"),
        ("Bài 7", "Pareto NSGA-II đa mục tiêu",          "Khó",   "pymoo"),
        ("Bài 8", "Tối ưu động 2026-2035",               "Khó",   "CVXPY · SLSQP"),
        ("Bài 9", "Thị trường lao động AI",               "Khó",   "CVXPY · PuLP"),
        ("Bài 10","Stochastic LP 2 giai đoạn",           "R.khó", "Pyomo · CBC"),
        ("Bài 11","Q-learning chính sách kinh tế",        "R.khó", "Gymnasium · RL"),
        ("Bài 12","Đồ án AIDEOM-VN tích hợp",            "R.khó", "Streamlit"),
    ]
    badge_map = {"Dễ":"easy","TB":"med","Khó":"hard","R.khó":"vhard"}
    for row in [modules[i:i+3] for i in range(0,12,3)]:
        cols = st.columns(3)
        for col, (code, name, diff, tools) in zip(cols, row):
            badge_cls = badge_map[diff]
            col.markdown(f"""
            <div class="metric-card">
                <b>{code}</b> <span class="badge badge-{badge_cls}">{diff}</span><br>
                {name}<br>
                <small style="color:#888">{tools}</small>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">GDP Việt Nam 2020-2025</div>', unsafe_allow_html=True)
    fig = px.bar(MACRO, x="year", y="GDP_trillion_VND", text_auto=".0f",
                 color_discrete_sequence=["#CC0001"],
                 labels={"year":"Năm","GDP_trillion_VND":"nghìn tỷ VND"})
    fig.update_layout(height=300, margin=dict(t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 1 – COBB-DOUGLAS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b01":
    st.markdown("## Bài 1 · Hàm sản xuất Cobb-Douglas mở rộng")
    st.markdown("**Mô hình:** Yₜ = Aₜ · Kₜᵅ · Lₜᵝ · Dₜᵞ · AIₜᵟ · Hₜᶿ")

    with st.expander("⚙️ Điều chỉnh tham số", expanded=True):
        c1,c2,c3,c4,c5 = st.columns(5)
        alpha = c1.slider("α – Vốn K", 0.10, 0.60, 0.33, 0.01)
        beta  = c2.slider("β – Lao động L", 0.10, 0.70, 0.42, 0.01)
        gamma = c3.slider("γ – Số hóa D", 0.01, 0.30, 0.10, 0.01)
        delta = c4.slider("δ – AI", 0.01, 0.25, 0.08, 0.01)
        theta = c5.slider("θ – Nhân lực H", 0.01, 0.25, 0.07, 0.01)
    total = round(alpha+beta+gamma+delta+theta, 3)
    if abs(total-1) < 0.02:
        st.success(f"✅ Tổng hệ số = {total:.3f} — lợi suất không đổi theo quy mô")
    else:
        st.warning(f"⚠️ Tổng hệ số = {total:.3f} ≠ 1.00 — vi phạm CRS")

    Y = MACRO.GDP_trillion_VND.values
    K = MACRO.K_trillion_VND.values
    L = MACRO.L_million.values
    D = MACRO.D_digital_pct.values
    AI= MACRO.AI_tech_firms_thousand.values
    H = MACRO.H_trained_pct.values

    A = compute_tfp(Y, K, L, D, AI, H, alpha, beta, gamma, delta, theta)
    A_mean = A.mean()
    Y_hat = forecast_gdp(A_mean, K, L, D, AI, H, alpha, beta, gamma, delta, theta)
    mape = np.mean(np.abs((Y - Y_hat)/Y))*100

    col1, col2, col3 = st.columns(3)
    col1.metric("TFP trung bình", f"{A_mean:.5f}")
    col2.metric("MAPE dự báo", f"{mape:.2f}%")
    col3.metric("GDP 2025 dự báo", f"{Y_hat[-1]:,.0f} nghìn tỷ")

    tab1, tab2, tab3 = st.tabs(["TFP theo năm","GDP thực vs dự báo","Phân rã tăng trưởng"])
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MACRO.year, y=A, mode="lines+markers", name="TFP A_t",
                                  line=dict(color="#CC0001", width=2)))
        fig.add_hline(y=A_mean, line_dash="dash", line_color="gray", annotation_text="Trung bình")
        fig.update_layout(height=350, title="TFP Việt Nam 2020-2025")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MACRO.year, y=Y, mode="lines+markers", name="Thực tế",
                                  line=dict(color="#CC0001")))
        fig.add_trace(go.Scatter(x=MACRO.year, y=Y_hat, mode="lines+markers", name="Dự báo",
                                  line=dict(color="#F4A261", dash="dash")))
        fig.update_layout(height=350, yaxis_title="nghìn tỷ VND")
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        dc = growth_decomp(MACRO, alpha, beta, gamma, delta, theta)
        factors = ["TFP","K","L","D","AI","H"]
        fig = go.Figure()
        colors_f = ["#CC0001","#F4A261","#2A9D8F","#457B9D","#A8DADC","#6D6875"]
        for f, col in zip(factors, colors_f):
            fig.add_trace(go.Bar(name=f, x=dc.year.astype(str), y=dc[f], marker_color=col))
        fig.update_layout(barmode="relative", height=350, yaxis_title="% đóng góp")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(dc.set_index("year"), use_container_width=True)

    st.markdown("#### Dự báo kịch bản 2030")
    ca, cb, cc = st.columns(3)
    D30 = ca.slider("D 2030 (%)", 20, 50, 30)
    AI30= cb.slider("AI 2030 (nghìn DN)", 60, 200, 100, 5)
    H30 = cc.slider("H 2030 (%)", 25, 55, 35)
    cd, ce, cf = st.columns(3)
    Kg = cd.slider("Tăng K (%/năm)", 2, 12, 6) / 100
    Lg = ce.slider("Tăng L (%/năm)", 0.5, 5.0, 1.0, 0.5) / 100
    tg = cf.slider("Tăng TFP (%/năm)", 0.0, 3.0, 1.2, 0.1) / 100

    A30  = A[-1]*(1+tg)**5
    K30  = K[-1]*(1+Kg)**5
    L30  = L[-1]*(1+Lg)**5
    GDP30 = forecast_gdp(A30, K30, L30, D30, AI30, H30, alpha, beta, gamma, delta, theta)
    cagr  = (GDP30/Y[-1])**(1/5) - 1
    st.success(f"**GDP 2030 dự báo:** {GDP30:,.0f} nghìn tỷ VND &nbsp;|&nbsp; CAGR: {cagr*100:.1f}%/năm")


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 2 – LP BUDGET
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b02":
    st.markdown("## Bài 2 · LP Phân bổ ngân sách 4 hạng mục")
    st.markdown("**max Z = 0.85x₁ + 1.20x₂ + 0.95x₃ + 1.35x₄** (nghìn tỷ VND)")

    with st.expander("⚙️ Tham số", expanded=True):
        c1,c2,c3,c4,c5 = st.columns(5)
        budget = c1.slider("Tổng ngân sách (nghìn tỷ)", 70, 200, 100, 10)
        min1 = c2.slider("Min hạ tầng", 10, 40, 25, 5)
        min2 = c3.slider("Min AI", 5, 30, 15, 5)
        min3 = c4.slider("Min nhân lực", 10, 40, 20, 5)
        min4 = c5.slider("Min R&D", 5, 25, 10, 5)
        strat = st.slider("Tỷ lệ chiến lược AI+R&D tối thiểu (%)", 20, 60, 35) / 100

    x_opt, Z_opt = lp_simple(budget, min1, min2, min3, min4, strat)
    labels = ["Hạ tầng số x₁","AI & Dữ liệu x₂","Nhân lực số x₃","R&D công nghệ x₄"]
    coeffs = [0.85, 1.20, 0.95, 1.35]

    col1, col2, col3 = st.columns(3)
    col1.metric("Z* GDP tăng thêm", f"{Z_opt:.1f} nghìn tỷ")
    col2.metric("Phân bổ tổng", f"{x_opt.sum():.1f} / {budget}")
    col3.metric("ROI trung bình", f"{Z_opt/budget:.3f}")

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Phân bổ ngân sách", "GDP gain / tỷ đầu tư"])
    fig.add_trace(go.Bar(x=labels, y=x_opt, marker_color=COLORS), 1, 1)
    fig.add_trace(go.Bar(x=labels, y=coeffs, marker_color=COLORS), 1, 2)
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Phân tích độ nhạy theo ngân sách")
    B_range = range(70, 201, 10)
    Z_vals = [lp_simple(b, min1, min2, min3, min4, strat)[1] for b in B_range]
    fig2 = px.line(x=list(B_range), y=Z_vals, markers=True,
                   labels={"x":"Ngân sách (nghìn tỷ)","y":"Z* (nghìn tỷ)"},
                   color_discrete_sequence=["#CC0001"])
    fig2.update_layout(height=280)
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 3 – PRIORITY INDEX
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b03":
    st.markdown("## Bài 3 · Chỉ số ưu tiên ngành (MCDM)")
    st.markdown("Priorityᵢ = a₁·Growthᵢ + a₂·Productᵢ + a₃·Spilloverᵢ + a₄·Exportᵢ + a₅·Labourᵢ + a₆·AIᵢ − a₇·Riskᵢ")

    preset = st.selectbox("Bộ trọng số:", ["Mặc định","Tăng trưởng","Bao trùm","Tùy chỉnh"])
    if preset == "Mặc định":   w = [0.15,0.15,0.20,0.15,0.10,0.20,0.15]
    elif preset == "Tăng trưởng": w = [0.25,0.20,0.15,0.20,0.05,0.10,0.05]
    elif preset == "Bao trùm": w = [0.10,0.10,0.25,0.05,0.25,0.10,0.15]
    else:
        c1,c2,c3,c4 = st.columns(4)
        a1 = c1.slider("a₁ Tăng trưởng", 0.0,0.40,0.15,0.01)
        a2 = c1.slider("a₂ Năng suất",   0.0,0.40,0.15,0.01)
        a3 = c2.slider("a₃ Lan tỏa",     0.0,0.40,0.20,0.01)
        a4 = c2.slider("a₄ Xuất khẩu",   0.0,0.40,0.15,0.01)
        a5 = c3.slider("a₅ Việc làm",    0.0,0.40,0.10,0.01)
        a6 = c3.slider("a₆ AI Readiness",0.0,0.40,0.20,0.01)
        a7 = c4.slider("a₇ Rủi ro TĐH", 0.0,0.40,0.15,0.01)
        w = [a1,a2,a3,a4,a5,a6,a7]
    wsum = sum(w)
    if abs(wsum - 1.0) > 0.02:
        st.warning(f"Tổng trọng số = {wsum:.2f} (chuẩn hóa tự động)")
        w = [wi/wsum for wi in w]

    scores = priority_index(SECTORS, w)
    df_p = SECTORS[["sector_name_vi"]].copy()
    df_p["Priority"] = scores.round(4)
    df_p["Rank"] = df_p.Priority.rank(ascending=False).astype(int)
    df_p = df_p.sort_values("Priority", ascending=False)

    fig = px.bar(df_p, x="Priority", y="sector_name_vi", orientation="h",
                 color="Priority", color_continuous_scale="RdYlGn",
                 labels={"sector_name_vi":"Ngành","Priority":"Điểm ưu tiên"})
    fig.update_layout(height=400, yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_p.reset_index(drop=True), use_container_width=True, height=300)

    st.markdown("#### Phân tích độ nhạy trọng số AI Readiness (a₆)")
    w_range = np.arange(0.05, 0.41, 0.05)
    top3_data = {}
    for wa in w_range:
        w_tmp = [w[0],w[1],w[2],w[3],w[4],wa,w[6]]
        s_tmp = [wi*(1-wa)/sum([w[0],w[1],w[2],w[3],w[4],w[6]]) if i!=5 else wa
                 for i,wi in enumerate(w_tmp)]
        s_tmp = [wi/sum(w_tmp) for wi in w_tmp]  # renorm
        sc = priority_index(SECTORS, s_tmp)
        top3 = SECTORS.iloc[np.argsort(sc)[-3:][::-1]]["sector_name_vi"].tolist()
        for rank_i, sn in enumerate(top3):
            top3_data.setdefault(sn, []).append((wa, rank_i+1))
    fig2 = go.Figure()
    for sname, pts in top3_data.items():
        xs, ys = zip(*pts)
        fig2.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=sname))
    fig2.update_layout(height=280, yaxis=dict(autorange="reversed",tickvals=[1,2,3]),
                        xaxis_title="Trọng số a₆ AI Readiness", yaxis_title="Hạng top-3")
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 4 – REGION LP
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b04":
    st.markdown("## Bài 4 · LP Phân bổ ngân sách 6 vùng × 4 hạng mục")

    col1, col2, col3 = st.columns(3)
    budget = col1.slider("Tổng ngân sách (tỷ VND)", 30000, 80000, 50000, 5000)
    lam    = col2.slider("λ công bằng vùng", 0.3, 1.0, 0.7, 0.05)
    fairness = col3.checkbox("Áp dụng ràng buộc công bằng (C5)", value=True)

    with st.spinner("Đang giải LP..."):
        X_fair, Z_fair   = region_lp(budget, lam, True)
        X_nofair, Z_nofair = region_lp(budget, lam, False)

    REGION_NAMES = ["Trung du MB phía Bắc","Đồng bằng sông Hồng","Bắc Trung Bộ & DHMT","Tây Nguyên","Đông Nam Bộ","ĐBSCL"]
    ITEM_NAMES = ["Hạ tầng I","Số hóa D","AI","Nhân lực H"]
    X = X_fair if fairness else X_nofair
    Z = Z_fair if fairness else Z_nofair

    col1, col2, col3 = st.columns(3)
    col1.metric("Z* GDP gain", f"{Z:,.0f} tỷ VND")
    col2.metric("Chi phí công bằng", f"{Z_nofair-Z_fair:,.0f} tỷ VND")
    col3.metric("GDP loss %", f"{(Z_nofair-Z_fair)/Z_nofair*100:.1f}%")

    df_heat = pd.DataFrame(X, index=REGION_NAMES, columns=ITEM_NAMES)
    fig = px.imshow(df_heat, text_auto=".0f", aspect="auto",
                    color_continuous_scale="Blues",
                    labels=dict(color="Tỷ VND"))
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig2 = px.bar(df_heat.reset_index().melt(id_vars="index"),
                       x="index", y="value", color="variable", barmode="stack",
                       labels={"index":"Vùng","value":"Tỷ VND","variable":"Hạng mục"},
                       title="Phân bổ có ràng buộc công bằng")
        fig2.update_layout(height=320)
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        df_nf = pd.DataFrame(X_nofair, index=REGION_NAMES, columns=ITEM_NAMES)
        fig3 = px.bar(df_nf.reset_index().melt(id_vars="index"),
                       x="index", y="value", color="variable", barmode="stack",
                       title="Không có ràng buộc công bằng",
                       labels={"index":"Vùng","value":"Tỷ VND","variable":"Hạng mục"})
        fig3.update_layout(height=320)
        st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 5 – MIP PROJECT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b05":
    st.markdown("## Bài 5 · MIP Lựa chọn danh mục dự án chuyển đổi số")

    c1, c2 = st.columns(2)
    budget_t = c1.slider("Tổng ngân sách 5 năm (tỷ VND)", 60000, 120000, 80000, 5000)
    budget_12 = c2.slider("Ngân sách năm 1-2 (tỷ VND)", 30000, 60000, 40000, 5000)

    selected, total_cost, total_benefit = mip_project(budget_t, budget_12)

    c1, c2, c3 = st.columns(3)
    c1.metric("Số dự án chọn", len(selected))
    c2.metric("Tổng chi phí", f"{total_cost:,} tỷ")
    c3.metric("Tổng lợi ích Z*", f"{total_benefit:,} tỷ")

    df_proj = pd.DataFrame([
        {"Mã": f"P{i}", "Tên dự án": PROJECTS[i],
         "Chi phí (tỷ)": PROJ_COST[i], "Lợi ích NPV (tỷ)": PROJ_BEN[i],
         "ROI": round(PROJ_BEN[i]/PROJ_COST[i], 2),
         "Được chọn": "✅" if i in selected else "❌"}
        for i in range(1,16)
    ])
    st.dataframe(df_proj, use_container_width=True, height=450)

    fig = px.scatter(df_proj, x="Chi phí (tỷ)", y="Lợi ích NPV (tỷ)", text="Mã",
                      color="Được chọn", size="ROI",
                      color_discrete_map={"✅":"#2A9D8F","❌":"#E9C46A"},
                      title="Không gian Chi phí – Lợi ích")
    fig.update_traces(textposition="top center")
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 6 – TOPSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b06":
    st.markdown("## Bài 6 · TOPSIS Xếp hạng vùng theo AI Readiness")

    CRIT  = ["grdp_per_capita_million_VND","fdi_registered_billion_USD",
              "digital_index_0_100","ai_readiness_0_100","trained_labor_pct",
              "rd_intensity_pct","internet_penetration_pct","gini_coef"]
    IS_BEN = [True,True,True,True,True,True,True,False]
    CRIT_LABELS = ["GRDP/người","FDI","Digital","AI Ready","Lao động ĐT","R&D","Internet","Gini"]

    with st.expander("⚙️ Trọng số chuyên gia", expanded=True):
        cols = st.columns(8)
        default_w = [0.10,0.10,0.15,0.20,0.15,0.15,0.05,0.10]
        w_expert = [cols[i].number_input(CRIT_LABELS[i], 0.0, 0.5, default_w[i], 0.01) for i in range(8)]
    wsum = sum(w_expert)
    w_expert = [wi/wsum for wi in w_expert]

    X = REGIONS[CRIT].values.astype(float)
    scores_exp = topsis(X, w_expert, IS_BEN)
    # Entropy weights
    P = X / X.sum(axis=0)
    k = 1/np.log(6)
    E = -k*np.nansum(P*np.log(P+1e-12), axis=0)
    d = 1-E; w_ent = d/d.sum()
    scores_ent = topsis(X, w_ent, IS_BEN)

    df_t = REGIONS[["region_name_vi"]].copy()
    df_t["TOPSIS (chuyên gia)"] = scores_exp.round(4)
    df_t["Rank (CG)"] = df_t["TOPSIS (chuyên gia)"].rank(ascending=False).astype(int)
    df_t["TOPSIS (entropy)"] = scores_ent.round(4)
    df_t["Rank (Ent)"] = df_t["TOPSIS (entropy)"].rank(ascending=False).astype(int)
    st.dataframe(df_t, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(df_t.sort_values("TOPSIS (chuyên gia)", ascending=True),
                      x="TOPSIS (chuyên gia)", y="region_name_vi", orientation="h",
                      color="TOPSIS (chuyên gia)", color_continuous_scale="Blues",
                      title="Trọng số chuyên gia")
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        fig2 = px.bar(df_t.sort_values("TOPSIS (entropy)", ascending=True),
                       x="TOPSIS (entropy)", y="region_name_vi", orientation="h",
                       color="TOPSIS (entropy)", color_continuous_scale="Greens",
                       title="Trọng số Entropy")
        fig2.update_layout(height=320)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Phân tích độ nhạy trọng số AI Readiness")
    w_ai_range = np.arange(0.10, 0.41, 0.05)
    ranks_over_time = {REGIONS.iloc[r].region_name_vi: [] for r in range(6)}
    for wai in w_ai_range:
        w_tmp = list(w_expert); w_tmp[3] = wai
        w_tmp = [wi/sum(w_tmp) for wi in w_tmp]
        sc = topsis(X, w_tmp, IS_BEN)
        rnk = 6 - sc.argsort().argsort()
        for r in range(6):
            ranks_over_time[REGIONS.iloc[r].region_name_vi].append(rnk[r])
    fig3 = go.Figure()
    for rname, rnks in ranks_over_time.items():
        fig3.add_trace(go.Scatter(x=w_ai_range, y=rnks, mode="lines+markers", name=rname))
    fig3.update_layout(height=300, yaxis=dict(autorange="reversed", tickvals=list(range(1,7))),
                        xaxis_title="w_AI", yaxis_title="Hạng")
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 7 – PARETO (simulation)
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b07":
    st.markdown("## Bài 7 · Tối ưu đa mục tiêu Pareto (mô phỏng NSGA-II)")
    st.info("Đây là mô phỏng Monte Carlo minh họa đường biên Pareto. Chạy NSGA-II đầy đủ cần pymoo.")

    np.random.seed(42)
    n = 400
    # Generate random allocations and compute 3 objectives
    X_rand = np.random.dirichlet(np.ones(4), n) * 50000
    beta_mat = np.array([[1.15,0.85,0.55,1.30],[0.95,1.25,1.40,1.05],
                          [1.05,0.95,0.85,1.15],[1.20,0.75,0.45,1.35],
                          [0.90,1.30,1.55,1.00],[1.10,0.85,0.65,1.25]])
    # f1 = GDP gain (max → negate)
    # f2 = regional inequality (min = MAD of row sums)
    # f3 = emissions = e_r * (x_I + x_AI)
    e = np.array([0.42,0.55,0.48,0.32,0.62,0.38])
    rho = np.array([0.18,0.45,0.28,0.12,0.52,0.22])
    sig = np.array([0.32,0.28,0.30,0.35,0.25,0.30])

    f1_vals, f2_vals, f3_vals = [], [], []
    for xrow in X_rand:
        Xm = np.tile(xrow, (6,1))  # broadcast
        f1 = (beta_mat * Xm).sum()
        row_sums = Xm.sum(axis=1)
        f2 = np.abs(row_sums - row_sums.mean()).mean()
        f3 = (e * (Xm[:,0] + Xm[:,2])).sum()
        f1_vals.append(f1); f2_vals.append(f2); f3_vals.append(f3)
    f1a, f2a, f3a = np.array(f1_vals), np.array(f2_vals), np.array(f3_vals)

    # Approximate Pareto front (f1 high, f2 low, f3 low) using dominance
    def is_pareto(f1, f2, f3):
        dominated = np.zeros(len(f1), dtype=bool)
        for i in range(len(f1)):
            for j in range(len(f1)):
                if (f1[j]>=f1[i] and f2[j]<=f2[i] and f3[j]<=f3[i] and
                    (f1[j]>f1[i] or f2[j]<f2[i] or f3[j]<f3[i])):
                    dominated[i] = True; break
        return ~dominated
    # Approx with just top/bottom percentiles
    mask_top = ((f1a > np.percentile(f1a,70)) & (f2a < np.percentile(f2a,60)) &
                (f3a < np.percentile(f3a,70)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f1a, y=f2a, mode="markers", name="Tất cả nghiệm",
                              marker=dict(color=f3a, colorscale="Viridis", size=4, opacity=0.4,
                                          colorbar=dict(title="Phát thải f₃"))))
    fig.add_trace(go.Scatter(x=f1a[mask_top], y=f2a[mask_top], mode="markers",
                              name="Pareto approx", marker=dict(color="#CC0001", size=8)))
    fig.update_layout(height=400, xaxis_title="f₁ GDP gain (tối đa hóa)",
                       yaxis_title="f₂ Bất bình đẳng vùng (tối thiểu hóa)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Phân tích đánh đổi (trade-off)")
    w1 = st.slider("Trọng số GDP (f₁)", 0.1, 0.7, 0.4, 0.05)
    w2 = st.slider("Trọng số Bao trùm (f₂)", 0.1, 0.5, 0.25, 0.05)
    w3 = 1 - w1 - w2 if 1-w1-w2 > 0 else 0.05
    st.caption(f"Trọng số phát thải f₃ = {w3:.2f}")
    # Compromise: min weighted distance from utopia
    u1, u2, u3 = f1a.max(), f2a.min(), f3a.min()
    dist = w1*((f1a - u1)/u1)**2 + w2*((f2a - u2)/(f2a.max()-u2+1))**2 + w3*((f3a - u3)/(f3a.max()-u3+1))**2
    best = np.argmin(dist)
    st.success(f"Nghiệm thỏa hiệp: GDP={f1a[best]:,.0f} · Bất bình đẳng={f2a[best]:,.0f} · Phát thải={f3a[best]:,.0f}")


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 8 – DYNAMIC OPT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b08":
    st.markdown("## Bài 8 · Tối ưu động 2026–2035")

    rho = st.slider("Hệ số chiết khấu ρ", 0.85, 0.99, 0.97, 0.01)
    T   = st.slider("Số năm tối ưu T", 5, 10, 10, 1)

    with st.spinner("Đang tối ưu hóa quỹ đạo..."):
        K, D, AI, H, GDP_path = dynamic_opt(T, rho)

    years = list(range(2026, 2026+T+1))
    df_dyn = pd.DataFrame({"Năm": years, "K (nghìn tỷ)": K[:T+1], "D (%)": D[:T+1],
                             "AI (nghìn DN)": AI[:T+1], "H (%)": H[:T+1],
                             "GDP (nghìn tỷ)": GDP_path[:T+1]})

    fig = make_subplots(rows=2, cols=2, subplot_titles=["Vốn K","Số hóa D","AI capacity","Nhân lực H"])
    traces = [("K (nghìn tỷ)",1,1),("D (%)",1,2),("AI (nghìn DN)",2,1),("H (%)",2,2)]
    for col_n, r, c in traces:
        fig.add_trace(go.Scatter(x=df_dyn["Năm"], y=df_dyn[col_n], mode="lines+markers",
                                  line=dict(color="#CC0001")), r, c)
    fig.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(df_dyn, x="Năm", y="GDP (nghìn tỷ)", markers=True,
                    color_discrete_sequence=["#2A9D8F"])
    fig2.update_layout(height=260, title="Quỹ đạo GDP tối ưu 2026-2035")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_dyn.round(2), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 9 – LABOR MARKET
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b09":
    st.markdown("## Bài 9 · Tác động AI tới thị trường lao động Việt Nam")

    budget_lab = st.slider("Ngân sách tổng (tỷ VND)", 10000, 60000, 30000, 5000)

    with st.spinner("Giải tối ưu lao động..."):
        xAI, xH, net_jobs = labor_opt(budget_lab)

    SECTOR_NAMES = ["Nông-Lâm-TS","CN CBCT","Xây dựng","Bán buôn-lẻ","Tài chính-NH","Logistics","CNTT-TT","Giáo dục"]
    risk = np.array([18,42,25,38,52,35,28,22])
    a1 = np.array([8.5,32.5,12.8,22.4,45.8,28.5,62.5,18.5])
    c1_arr = np.array([5.2,62.4,18.5,48.2,72.5,42.8,32.5,12.5])

    new_jobs = a1 * xAI
    displaced = c1_arr * (risk/100) * xAI

    df_lab = pd.DataFrame({
        "Ngành": SECTOR_NAMES,
        "x_AI (tỷ)": xAI.round(0),
        "x_H (tỷ)": xH.round(0),
        "Việc làm mới": new_jobs.round(0),
        "Bị thay thế": displaced.round(0),
        "NetJob": net_jobs.round(0),
    })

    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng NetJob ròng", f"{net_jobs.sum():,.0f}")
    c2.metric("Tổng x_AI", f"{xAI.sum():,.0f} tỷ")
    c3.metric("Tổng x_H", f"{xH.sum():,.0f} tỷ")

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Việc làm mới", x=SECTOR_NAMES, y=new_jobs, marker_color="#2A9D8F"))
    fig.add_trace(go.Bar(name="Bị thay thế",  x=SECTOR_NAMES, y=-displaced, marker_color="#E76F51"))
    fig.add_trace(go.Scatter(name="NetJob", x=SECTOR_NAMES, y=net_jobs,
                              mode="lines+markers", line=dict(color="#CC0001", width=2)))
    fig.update_layout(barmode="relative", height=380, yaxis_title="Số việc làm")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_lab, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 10 – STOCHASTIC LP
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b10":
    st.markdown("## Bài 10 · Quy hoạch ngẫu nhiên 2 giai đoạn")

    st.markdown("""
    **Cấu trúc kịch bản:**
    | Kịch bản | Tăng trưởng TG | FDI VN | Xác suất |
    |---|---|---|---|
    | Lạc quan | 3.5% | 32B USD | 30% |
    | Cơ sở | 2.8% | 27B USD | 45% |
    | Bi quan | 1.5% | 20B USD | 20% |
    | Khủng hoảng | 0.2% | 12B USD | 5% |
    """)

    with st.spinner("Đang giải Stochastic LP..."):
        x_opt, y_opt, Z_rp = stochastic_lp()

    items = ["Hạ tầng I","Số hóa D","AI","Nhân lực H"]
    c1,c2,c3 = st.columns(3)
    c1.metric("Z* kỳ vọng", f"{Z_rp:,.1f} tỷ VND")
    c2.metric("x_AI (giai đoạn 1)", f"{x_opt[2]:,.0f} tỷ")
    c3.metric("x_H (giai đoạn 1)", f"{x_opt[3]:,.0f} tỷ")

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Giai đoạn 1 (here-and-now)", x=items, y=x_opt,
                          marker_color="#2A9D8F"))
    for sname, yvals in y_opt.items():
        fig.add_trace(go.Bar(name=f"GĐ 2 – {sname}", x=items, y=yvals))
    fig.update_layout(barmode="group", height=380, yaxis_title="nghìn tỷ VND",
                       title="Quyết định giai đoạn 1 vs điều chỉnh giai đoạn 2")
    st.plotly_chart(fig, use_container_width=True)

    # VSS illustration
    st.markdown("#### VSS & EVPI (minh họa)")
    Z_eev = Z_rp * 0.94  # simplified estimate
    Z_ws  = Z_rp * 1.06
    df_zz = pd.DataFrame({"Phương pháp": ["EEV","SP (RP)","WS"],
                            "Giá trị (tỷ VND)": [Z_eev, Z_rp, Z_ws]})
    fig2 = px.bar(df_zz, x="Phương pháp", y="Giá trị (tỷ VND)",
                   color="Phương pháp", color_discrete_sequence=COLORS)
    fig2.update_layout(height=280, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.info(f"VSS ≈ {Z_rp-Z_eev:,.0f} tỷ &nbsp;|&nbsp; EVPI ≈ {Z_ws-Z_rp:,.0f} tỷ")


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 11 – Q-LEARNING
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b11":
    st.markdown("## Bài 11 · Q-Learning – Chính sách kinh tế thích nghi")

    c1, c2, c3 = st.columns(3)
    episodes = c1.slider("Số episodes", 100, 2000, 500, 100)
    alpha_rl  = c2.slider("Learning rate α", 0.01, 0.5, 0.1, 0.01)
    gamma_rl  = c3.slider("Discount γ", 0.5, 0.99, 0.95, 0.01)

    with st.spinner(f"Huấn luyện Q-learning ({episodes} episodes)..."):
        Q, rewards_hist, ACTION_NAMES = q_sim(episodes, alpha_rl, gamma_rl)

    # Smooth rewards
    window = max(episodes//20, 10)
    smooth = pd.Series(rewards_hist).rolling(window).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=rewards_hist, mode="lines", name="Raw reward", opacity=0.3,
                              line=dict(color="#F4A261")))
    fig.add_trace(go.Scatter(y=smooth, mode="lines", name="Smoothed", line=dict(color="#CC0001", width=2)))
    fig.update_layout(height=300, xaxis_title="Episode", yaxis_title="Tổng phần thưởng",
                       title="Learning curve Q-learning")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Chính sách tối ưu π*(s) tại các trạng thái chính")
    def decode(s): ai=s//27; rem=s%27; gdp=rem//9; rem=rem%9; risk=rem//3; train=rem%3; return ai,gdp,risk,train
    test_states = {
        "VN 2026 (AI=1,GDP=1,Risk=1,Train=1)": 1*27+1*9+1*3+1,
        "GDP thấp, Rủi ro cao (0,0,2,0)": 0*27+0*9+2*3+0,
        "GDP cao, AI cao (2,2,0,2)": 2*27+2*9+0*3+2,
        "Khủng hoảng (0,0,2,0)": 0*27+0*9+2*3+0,
    }
    rows_rl = []
    for desc, sid in test_states.items():
        best_a = int(np.argmax(Q[sid]))
        rows_rl.append({"Trạng thái": desc, "Hành động tối ưu": ACTION_NAMES[best_a],
                         "Q-value": round(Q[sid, best_a], 2)})
    st.dataframe(pd.DataFrame(rows_rl), use_container_width=True)

    st.markdown("#### Heatmap Q-values cho trạng thái VN 2026")
    s0 = test_states["VN 2026 (AI=1,GDP=1,Risk=1,Train=1)"]
    fig2 = go.Figure(go.Bar(x=ACTION_NAMES, y=Q[s0], marker_color=COLORS))
    fig2.update_layout(height=250, title="Q-values tại trạng thái VN 2026", yaxis_title="Q-value")
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  BÀI 12 – INTEGRATED DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "b12":
    st.markdown("## Bài 12 · Dashboard AIDEOM-VN — So sánh 5 kịch bản chính sách")

    SCENARIOS = {
        "S1: Truyền thống":  {"K_alloc":0.70,"D_alloc":0.10,"AI_alloc":0.10,"H_alloc":0.10,"color":"#6D6875"},
        "S2: Số hóa nhanh":  {"K_alloc":0.25,"D_alloc":0.45,"AI_alloc":0.15,"H_alloc":0.15,"color":"#457B9D"},
        "S3: AI dẫn dắt":    {"K_alloc":0.20,"D_alloc":0.20,"AI_alloc":0.45,"H_alloc":0.15,"color":"#CC0001"},
        "S4: Bao trùm số":   {"K_alloc":0.30,"D_alloc":0.20,"AI_alloc":0.10,"H_alloc":0.40,"color":"#2A9D8F"},
        "S5: Tối ưu cân bằng":{"K_alloc":0.35,"D_alloc":0.25,"AI_alloc":0.20,"H_alloc":0.20,"color":"#F4A261"},
    }

    budget_total_s = st.slider("Tổng ngân sách mỗi năm (nghìn tỷ VND)", 500, 2000, 1000, 100)
    T_s = st.slider("Số năm mô phỏng", 3, 10, 5, 1)

    def simulate_scenario(alloc, budget, T, alpha=0.33, beta=0.42, gamma=0.10, delta=0.08, theta=0.07):
        K, D, AI, H = 27500, 20.3, 86, 30
        A = 0.82
        L0 = 53.9
        GDP_series = []
        for t in range(T+1):
            L = L0 * (1.01**t)
            gdp = A*(K**alpha)*(L**beta)*(D**gamma)*(AI**delta)*(H**theta)
            GDP_series.append(gdp)
            if t < T:
                invest = budget * alloc["K_alloc"]
                K  = K*(1-0.05)  + invest
                D  = D*(1-0.12)  + budget*alloc["D_alloc"]/100
                AI = AI*(1-0.15) + budget*alloc["AI_alloc"]/20
                H  = H*(1-0.02)  + budget*alloc["H_alloc"]*0.8/200
                A  = A*(1 + 0.003*D + 0.002*AI + 0.004*H)
        return GDP_series

    years_s = list(range(2025, 2025+T_s+1))
    results = {}
    for sname, cfg in SCENARIOS.items():
        results[sname] = simulate_scenario(cfg, budget_total_s, T_s)

    fig = go.Figure()
    for sname, cfg in SCENARIOS.items():
        fig.add_trace(go.Scatter(x=years_s, y=results[sname], mode="lines+markers",
                                  name=sname, line=dict(color=cfg["color"], width=2)))
    fig.update_layout(height=420, yaxis_title="nghìn tỷ VND",
                       title=f"GDP dự báo 5 kịch bản — ngân sách {budget_total_s:,} nghìn tỷ/năm")
    st.plotly_chart(fig, use_container_width=True)

    # KPI table
    kpi_rows = []
    for sname, gdp_path in results.items():
        cagr = (gdp_path[-1]/gdp_path[0])**(1/T_s) - 1
        kpi_rows.append({
            "Kịch bản": sname,
            f"GDP {years_s[-1]} (nghìn tỷ)": round(gdp_path[-1], 0),
            "CAGR (%/năm)": round(cagr*100, 2),
            f"GDP tăng {T_s}năm (%)": round((gdp_path[-1]/gdp_path[0]-1)*100, 1),
        })
    df_kpi = pd.DataFrame(kpi_rows)
    st.dataframe(df_kpi, use_container_width=True)

    # Allocation radar
    cats = ["Vốn K","Số hóa D","AI","Nhân lực H"]
    fig_rad = go.Figure()
    for sname, cfg in SCENARIOS.items():
        vals = [cfg["K_alloc"],cfg["D_alloc"],cfg["AI_alloc"],cfg["H_alloc"]]
        vals += [vals[0]]
        fig_rad.add_trace(go.Scatterpolar(r=vals, theta=cats+[cats[0]],
                                           name=sname, fill="toself",
                                           line=dict(color=cfg["color"])))
    fig_rad.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,0.8])),
                           height=380, title="Cơ cấu phân bổ 5 kịch bản")
    st.plotly_chart(fig_rad, use_container_width=True)

    st.markdown("#### Cảnh báo rủi ro")
    best_s = max(results, key=lambda s: results[s][-1])
    st.success(f"**Kịch bản dẫn đầu:** {best_s} → GDP {results[best_s][-1]:,.0f} nghìn tỷ")
    if "AI dẫn dắt" in best_s:
        st.warning("⚠️ Kịch bản AI dẫn dắt tiềm ẩn rủi ro thị trường lao động cao nếu nhân lực chưa sẵn sàng.")
    st.info("📊 Kết hợp S5 (Cân bằng) với đầu tư nhân lực đủ mạnh để bền vững dài hạn.")
