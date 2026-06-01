"""
Lean Athlete v6 — value-maximisation COMBINATION simulation (equal weights 33/33/33).

Models a training session as a COVERAGE problem over 13 goal sub-dimensions.
Key mechanic: coverage of each sub-dimension SATURATES, so a second movement
hitting an already-covered sub-dimension adds little ("don't double-count").
That is what surfaces overlap and rewards movements with UNIQUE coverage.

Run: python value_sim.py
"""
import math

# ---- 13 goal sub-dimensions; equal goal weights, equal split within each goal ----
SUBDIMS = {
    # Longevity (goal weight 1/3 -> 1/9 each)
    "VO2":    ("L", 1/9), "STR": ("L", 1/9), "TIS": ("L", 1/9),
    # Aesthetics (1/3 -> 1/12 each)
    "VTAPER": ("A", 1/12), "LEAN": ("A", 1/12), "UCHEST": ("A", 1/12), "ARMS": ("A", 1/12),
    # Basketball (1/3 -> 1/18 each)
    "POWER": ("B", 1/18), "SPEED": ("B", 1/18), "COD": ("B", 1/18),
    "SKILL": ("B", 1/18), "COND": ("B", 1/18), "CONTACT": ("B", 1/18),
}

# ---- movement x sub-dimension stimulus (0-5), minutes (incl setup), ramp flag ----
# ramp: ok / gated (no/limited in re-entry) / mod (modified loading)
M = {
    #                         VO2 STR TIS VTAP LEAN UCH ARM POW SPD COD SKL CND CON  min ramp
    "4x4 intervals":   dict(VO2=5,LEAN=3,COND=5,SPEED=1,                         t=28, ramp="gated"),
    "Zone-2 cardio":   dict(VO2=4,LEAN=2,COND=3,                                 t=25, ramp="ok"),
    "Accel sprints":   dict(VO2=1,STR=1,POWER=3,SPEED=5,COND=2,                  t=15, ramp="gated"),
    "Jumps/plyo":      dict(STR=1,TIS=2,POWER=5,SPEED=1,COD=2,                   t=8,  ramp="gated"),
    "Decel ladder":    dict(TIS=3,POWER=1,COD=5,CONTACT=1,                       t=7,  ramp="mod"),
    "Bulgarian SS":    dict(STR=4,TIS=2,LEAN=1,POWER=2,CONTACT=2,               t=8,  ramp="mod"),
    "Single-leg RDL":  dict(STR=3,TIS=3,POWER=1,CONTACT=1,                       t=6,  ramp="ok"),
    "Lateral lunge":   dict(STR=1,TIS=2,LEAN=1,COD=2,                            t=5,  ramp="ok"),
    "Ham slider/Nordic":dict(STR=2,TIS=4,SPEED=1,                               t=5,  ramp="mod"),
    "Incline DB press":dict(STR=3,UCHEST=4,ARMS=2,CONTACT=1,                     t=8,  ramp="ok"),
    "DB OHP":          dict(STR=2,VTAPER=1,UCHEST=1,ARMS=1,CONTACT=1,           t=6,  ramp="ok"),
    "Lateral raise":   dict(VTAPER=5,                                           t=5,  ramp="ok"),
    "Pull-ups":        dict(STR=3,VTAPER=4,ARMS=2,CONTACT=2,                     t=7,  ramp="ok"),
    "Chin-ups":        dict(STR=3,VTAPER=3,ARMS=4,CONTACT=2,                     t=7,  ramp="ok"),
    "DB Row":          dict(STR=3,VTAPER=4,ARMS=1,CONTACT=3,                     t=6,  ramp="ok"),
    "Rear delt fly":   dict(VTAPER=2,TIS=1,                                     t=4,  ramp="ok"),
    "Face pull":       dict(VTAPER=2,TIS=2,CONTACT=1,                            t=4,  ramp="ok"),
    "Pullover":        dict(VTAPER=2,UCHEST=2,                                  t=5,  ramp="ok"),
    "Curls/triceps":   dict(ARMS=4,                                            t=5,  ramp="ok"),
    "Carries":         dict(STR=2,TIS=2,ARMS=1,COND=1,CONTACT=3,               t=5,  ramp="ok"),
    "Pallof":          dict(TIS=2,CONTACT=3,                                   t=3,  ramp="ok"),
    "Med-ball throw":  dict(POWER=2,COD=1,CONTACT=2,                            t=4,  ramp="ok"),
    "Abs/leg raise":   dict(TIS=2,CONTACT=2,                                   t=5,  ramp="ok"),
    "Soleus/calf":     dict(TIS=4,POWER=1,                                     t=5,  ramp="ok"),
    "Copenhagen":      dict(TIS=3,CONTACT=1,                                   t=5,  ramp="ok"),
    "Skills":          dict(SKILL=5,CONTACT=1,                                 t=20, ramp="ok"),
}

def stim(mv):
    return {k: v for k, v in M[mv].items() if k in SUBDIMS}

def value(bundle, TAU=4.0):
    """Saturating coverage value of a set of movements."""
    tot = {s: 0.0 for s in SUBDIMS}
    for mv in bundle:
        for k, v in stim(mv).items():
            tot[k] += v
    val = 0.0
    for s, (goal, w) in SUBDIMS.items():
        val += w * (1 - math.exp(-tot[s] / TAU))
    return val

def marginal(mv, bundle, TAU=4.0):
    return value(bundle + [mv], TAU) - value(bundle, TAU)

def goal_breakdown(bundle, TAU=4.0):
    tot = {s: 0.0 for s in SUBDIMS}
    for mv in bundle:
        for k, v in stim(mv).items():
            tot[k] += v
    g = {"L": 0.0, "A": 0.0, "B": 0.0}
    for s, (goal, w) in SUBDIMS.items():
        g[goal] += w * (1 - math.exp(-tot[s] / TAU))
    return g  # each maxes at 1/3

# ---------------- 1. GLOBAL GREEDY by marginal value per minute ----------------
print("="*70)
print("1. GLOBAL GREEDY  — pick the next movement with highest marginal value/min")
print("="*70)
chosen, pool = [], list(M.keys())
order = []
while pool:
    best = max(pool, key=lambda mv: marginal(mv, chosen) / M[mv]["t"])
    mvval = marginal(best, chosen)
    order.append((best, mvval, mvval / M[best]["t"]))
    chosen.append(best); pool.remove(best)
cum = 0.0
print(f"{'#':>2} {'movement':<18}{'marg.val':>9}{'val/min':>9}{'cum_v':>8}{'cum_min':>8}")
cmin = 0
for i, (mv, mval, permin) in enumerate(order, 1):
    cum += mval; cmin += M[mv]["t"]
    print(f"{i:>2} {mv:<18}{mval*100:>8.2f}{permin*1000:>9.2f}{cum*100:>7.1f}%{cmin:>7}m")
print(f"\n(marg.val & cum shown x100; val/min x1000. Max possible cum = 100%.)")

# ---------------- 2. UNIQUE coverage: standalone value & how much is unique ------
print("\n" + "="*70)
print("2. STANDALONE value/min  vs  UNIQUE coverage (value lost if removed from ALL)")
print("="*70)
allmv = list(M.keys())
full = value(allmv)
rows = []
for mv in allmv:
    sv = value([mv])
    uniq = full - value([x for x in allmv if x != mv])
    rows.append((mv, sv, sv / M[mv]["t"], uniq))
rows.sort(key=lambda r: -r[2])
print(f"{'movement':<18}{'standalone':>11}{'val/min':>9}{'unique':>9}{'ramp':>7}")
for mv, sv, permin, uniq in rows:
    print(f"{mv:<18}{sv*100:>10.2f}{permin*1000:>9.2f}{uniq*100:>8.2f}{M[mv]['ramp']:>7}")

# ---------------- 3. SESSION bundles — captured value & marginal within session --
def session_report(name, bundle, TAU=4.0):
    tmin = sum(M[mv]["t"] for mv in bundle)
    v = value(bundle, TAU)
    g = goal_breakdown(bundle, TAU)
    print(f"\n--- {name}  ({tmin} min) ---")
    print(f"captured value {v*100:.1f}% of max   "
          f"[L {g['L']/(1/3)*100:.0f}% A {g['A']/(1/3)*100:.0f}% B {g['B']/(1/3)*100:.0f}% of each goal]")
    # marginal of each movement given the REST of the bundle (redundancy detector)
    for mv in bundle:
        rest = [x for x in bundle if x != mv]
        mg = v - value(rest, TAU)
        flag = "  <-- LOW marginal (redundant)" if mg*100 < 0.8 else ""
        print(f"   {mv:<18} marginal-in-session {mg*100:>5.2f}{flag}")
    return v, tmin

print("\n" + "="*70)
print("3. CANDIDATE LPP SESSIONS — captured value + in-session redundancy")
print("="*70)

mon = ["Jumps/plyo","Bulgarian SS","Single-leg RDL","Ham slider/Nordic",
       "Soleus/calf","Copenhagen","Pallof","Decel ladder"]
tue = ["Incline DB press","Lateral raise","DB OHP","Curls/triceps","Pullover"]
thu = ["Pull-ups","DB Row","Carries","Med-ball throw","Face pull"]
sun = ["Accel sprints","4x4 intervals"]
sat = ["Skills"]

for nm, b in [("MON Lower",mon),("TUE Push",tue),("THU Pull",thu),
              ("SUN Run",sun),("SAT Court",sat)]:
    session_report(nm, b)

# ---------------- 4. Trimmed sessions (drop redundant) re-scored ----------------
print("\n" + "="*70)
print("4. TRIMMED program — drop low-marginal items, re-score value/min")
print("="*70)
mon_t = ["Jumps/plyo","Bulgarian SS","Single-leg RDL","Soleus/calf","Copenhagen","Pallof","Decel ladder"]
tue_t = ["Incline DB press","Lateral raise","Curls/triceps"]
thu_t = ["Pull-ups","DB Row","Carries"]
sun_t = ["Accel sprints","4x4 intervals"]
sat_t = ["Skills"]
prog = []
for nm, b in [("MON Lower",mon_t),("TUE Push",tue_t),("THU Pull",thu_t),
              ("SUN Run",sun_t),("SAT Court",sat_t)]:
    v, t = session_report(nm, b); prog += b
tot_t = sum(M[mv]["t"] for mv in set(prog))
print(f"\nFULL PROGRAM captured value: {value(list(set(prog)))*100:.1f}% of max  in {tot_t} min/wk")
g = goal_breakdown(list(set(prog)))
print(f"goal coverage: L {g['L']/(1/3)*100:.0f}%  A {g['A']/(1/3)*100:.0f}%  B {g['B']/(1/3)*100:.0f}%")

# 4-day BASE only (no Thu/Sat bonus)
base = list(set(mon_t+tue_t+sun_t))
gb = goal_breakdown(base)
print(f"\n4-DAY BASE only (Mon+Tue+Sun+game-skills): {value(base)*100:.1f}% of max")
print(f"   L {gb['L']/(1/3)*100:.0f}%  A {gb['A']/(1/3)*100:.0f}%  B {gb['B']/(1/3)*100:.0f}%")

# ---------------- 5. Sensitivity: does the top-tier ordering survive TAU? --------
print("\n" + "="*70)
print("5. SENSITIVITY — top-8 greedy order across saturation TAU (robustness)")
print("="*70)
for TAU in (2.0, 3.0, 4.0, 6.0):
    ch, pl = [], list(M.keys())
    seq = []
    while pl:
        best = max(pl, key=lambda mv: marginal(mv, ch, TAU)/M[mv]["t"])
        seq.append(best); ch.append(best); pl.remove(best)
    print(f"TAU={TAU}: " + " > ".join(seq[:8]))
