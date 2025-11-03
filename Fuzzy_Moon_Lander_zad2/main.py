import numpy as np
import gymnasium as gym
import skfuzzy as fuzz
from skfuzzy import control as ctrl


theta   = ctrl.Antecedent(np.linspace(-1.8, 1.8, 121),  'theta')
dtheta  = ctrl.Antecedent(np.linspace(-3.5, 3.5, 121),  'dtheta')
vx      = ctrl.Antecedent(np.linspace(-3.5, 3.5, 121),  'vx')
vy      = ctrl.Antecedent(np.linspace(-7.0, 3.0, 121),  'vy')
x_pos   = ctrl.Antecedent(np.linspace(-1.6, 1.6, 121),  'x')
y_alt   = ctrl.Antecedent(np.linspace(0.0, 1.6, 121),   'y')

main_thrust = ctrl.Consequent(np.linspace(0.0, 1.0, 121), 'main_thrust')
lat_thrust  = ctrl.Consequent(np.linspace(-1.0, 1.0, 121), 'lat_thrust')


theta['right'] = fuzz.trimf(theta.universe, [-1.8, -0.5,  0.0])
theta['level'] = fuzz.trimf(theta.universe, [-0.07, 0.0,  0.07])
theta['left']  = fuzz.trimf(theta.universe, [ 0.0,  0.5,  1.8])

dtheta['cw']   = fuzz.trimf(dtheta.universe, [-3.5, -1.0, -0.25])
dtheta['zero'] = fuzz.trimf(dtheta.universe, [-0.25, 0.0, 0.25])
dtheta['ccw']  = fuzz.trimf(dtheta.universe, [ 0.25, 1.0,  3.5])

vx['left']  = fuzz.trimf(vx.universe,  [-3.5, -1.2, -0.25])
vx['zero']  = fuzz.trimf(vx.universe,  [-0.30, 0.0,  0.30])
vx['right'] = fuzz.trimf(vx.universe,  [ 0.25, 1.2,  3.5])

vy['fast'] = fuzz.trimf(vy.universe,  [-7.0, -7.0, -2.0])
vy['down'] = fuzz.trimf(vy.universe,  [-2.8, -1.2, -0.25])
vy['soft'] = fuzz.trimf(vy.universe,  [-0.5, -0.05, 1.2])

x_pos['far_left']  = fuzz.trimf(x_pos.universe, [-1.6, -0.7, -0.20])
x_pos['center']    = fuzz.trimf(x_pos.universe, [-0.12, 0.0,  0.12])
x_pos['far_right'] = fuzz.trimf(x_pos.universe, [ 0.20, 0.7,  1.6])

y_alt['very_high'] = fuzz.trimf(y_alt.universe, [0.9,  1.6, 1.6])
y_alt['high']      = fuzz.trimf(y_alt.universe, [0.5,  0.9,  1.3])
y_alt['mid']       = fuzz.trimf(y_alt.universe, [0.25, 0.60, 1.05])
y_alt['low']       = fuzz.trimf(y_alt.universe, [0.06, 0.18, 0.40])
y_alt['very_low']  = fuzz.trimf(y_alt.universe, [0.0,  0.03, 0.10])

main_thrust['low']   = fuzz.trimf(main_thrust.universe, [0.0,  0.0,  0.35])
main_thrust['med']   = fuzz.trimf(main_thrust.universe, [0.20, 0.55, 0.85])
main_thrust['high']  = fuzz.trimf(main_thrust.universe, [0.70, 1.0,  1.0])

lat_thrust['left']  = fuzz.trimf(lat_thrust.universe,  [-1.0, -1.0, -0.25])
lat_thrust['zero']  = fuzz.trimf(lat_thrust.universe,  [-0.20, 0.0,  0.20])
lat_thrust['right'] = fuzz.trimf(lat_thrust.universe,  [ 0.25, 1.0,  1.0])


rules = [
    ctrl.Rule(theta['left']  | dtheta['ccw'],  lat_thrust['right']),
    ctrl.Rule(theta['right'] | dtheta['cw'],   lat_thrust['left']),
    ctrl.Rule(theta['level'] & dtheta['zero'], lat_thrust['zero']),
    ctrl.Rule(x_pos['far_right'] & theta['level'], lat_thrust['left']),
    ctrl.Rule(x_pos['far_left']  & theta['level'], lat_thrust['right']),
    ctrl.Rule(vx['right'], lat_thrust['left']),
    ctrl.Rule(vx['left'],  lat_thrust['right']),
    ctrl.Rule(vy['fast'], main_thrust['high']),
    ctrl.Rule(vy['down'], main_thrust['med']),
    ctrl.Rule(vy['soft'], main_thrust['med']),
    ctrl.Rule(y_alt['very_high'] & vy['fast'], main_thrust['med']),
    ctrl.Rule(y_alt['high']      & vy['fast'], main_thrust['high']),
    ctrl.Rule(y_alt['mid'] & (vy['down'] | vy['fast']), main_thrust['high']),
    ctrl.Rule(y_alt['low'] & (vy['down'] | vy['fast']), main_thrust['high']),
    ctrl.Rule(y_alt['very_low'] & vy['soft'], main_thrust['low']),
    ctrl.Rule(y_alt['low'] & (theta['left']  | dtheta['ccw']),  lat_thrust['right']),
    ctrl.Rule(y_alt['low'] & (theta['right'] | dtheta['cw']),   lat_thrust['left']),
]

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

_prev_action = np.array([0.0, 0.0], dtype=np.float32)
ALPHA = 0.50


def _lateral_shaper(lat: float, deadzone: float = 0.5) -> float:
    """Apply deadzone and smooth shaping to lateral thruster input."""
    s = np.sign(lat)
    a = abs(lat)
    if a <= deadzone:
        return 0.0
    out = (a - deadzone) / (1.0 - deadzone)
    out = np.tanh(1.8 * out)
    return float(np.clip(s * out, -1.0, 1.0))


def fuzzy_action(obs):
    """Compute control action using fuzzy logic and safety heuristics."""
    global _prev_action
    x, y, vx_val, vy_val, th, dth, leg_l, leg_r = obs

    sim.reset()
    sim.input['theta']  = float(np.clip(th,     -1.8, 1.8))
    sim.input['dtheta'] = float(np.clip(dth,    -3.5, 3.5))
    sim.input['vx']     = float(np.clip(vx_val, -3.5, 3.5))
    sim.input['vy']     = float(np.clip(vy_val, -7.0, 3.0))
    sim.input['x']      = float(np.clip(x,      -1.6, 1.6))
    sim.input['y']      = float(np.clip(y,       0.0, 1.6))

    try:
        sim.compute()
    except Exception:
        return _prev_action

    if 'main_thrust' not in sim.output or 'lat_thrust' not in sim.output:
        return _prev_action

    main = float(sim.output['main_thrust'])
    lat  = float(sim.output['lat_thrust'])

    if vy_val < -0.2:
        main = 1.0
    elif y < 0.40 and vy_val < -0.5:
        main = max(main, 0.80)
    elif y < 0.28 and vy_val < -0.35:
        main = max(main, 0.90)

    lat = _lateral_shaper(lat, deadzone=0.12)

    main_cmd = 2.0 * main - 1.0
    lat_cmd  = np.clip(lat, -1.0, 1.0)

    if y > 0.80 and vy_val > 0.15:
        main_cmd = min(main_cmd, -0.15)
    if y > 1.25:
        main_cmd = -1.0

    if leg_l > 0.5 or leg_r > 0.5:
        main_cmd = -0.8
        lat_cmd  = 0.0

    action_raw = np.array([np.clip(main_cmd, -1.0, 1.0),
                           np.clip(lat_cmd,  -1.0, 1.0)], dtype=np.float32)
    action = (1 - ALPHA) * _prev_action + ALPHA * action_raw
    _prev_action = action
    return action


def run_episode(render=True, seed=None, max_steps=600):
    """Run a single simulation episode and return the total reward."""
    env = gym.make("LunarLanderContinuous-v3", render_mode="human")
    obs, info = env.reset(seed=seed)
    global _prev_action; _prev_action = np.array([0.0, 0.0], dtype=np.float32)

    total_reward = 0.0
    for _ in range(max_steps):
        action = fuzzy_action(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        if terminated or truncated:
            break
    env.close()
    return total_reward


if __name__ == "__main__":
    """Run one randomized flight and print results."""
    import random
    seed = random.randint(0, 10_000_000)
    print(f"Running flight (seed={seed})...\n")

    score = run_episode(render=True, seed=seed, max_steps=1600)

    print("\n========== FLIGHT RESULT ==========")
    print(f"Score: {score:.2f}")
    print(f"Seed:  {seed}")
    print("===================================")
