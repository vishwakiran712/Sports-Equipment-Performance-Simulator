import sys
import numpy as np
from scipy.optimize import minimize

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget,
    QGroupBox, QHeaderView, QDoubleSpinBox, QSplitter, QTextEdit,
    QFormLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class EquipmentPhysicsEngine:
    """Calculates physical responses, dynamics, performance scores, and sensitivity analysis across 5 sports equipment domains."""

    EQUIPMENT_TYPES = ["Racket", "Bat", "Shoe", "Helmet", "Bicycle Component"]

    DEFAULT_PRESETS = {
        "Racket": {
            "mass": 0.30,          # kg
            "stiffness": 68.0,     # RA index / kN/m
            "damping": 0.05,       # damping ratio zeta
            "moi": 0.032,          # kg*m^2
            "cor": 0.82,           # coefficient of restitution
            "friction": 0.40,      # string/ball friction
            "drag": 0.045          # aerodynamic CdA
        },
        "Bat": {
            "mass": 1.15,          # kg
            "stiffness": 120.0,    # kN/m
            "damping": 0.08,
            "moi": 0.35,           # kg*m^2
            "cor": 0.88,
            "friction": 0.35,
            "drag": 0.080
        },
        "Shoe": {
            "mass": 0.28,          # kg
            "stiffness": 45.0,     # midsole stiffness kN/m
            "damping": 0.25,       # shock absorption damping ratio
            "moi": 0.005,
            "cor": 0.65,           # energy return
            "friction": 0.85,      # outsole traction
            "drag": 0.020
        },
        "Helmet": {
            "mass": 0.32,          # kg
            "stiffness": 85.0,     # liner compression stiffness kN/m
            "damping": 0.40,       # impact energy dissipation
            "moi": 0.012,
            "cor": 0.20,           # low COR = high energy absorption
            "friction": 0.30,
            "drag": 0.015          # aero drag coefficient
        },
        "Bicycle Component": {
            "mass": 0.18,          # kg (e.g. carbon wheel rim)
            "stiffness": 150.0,    # lateral/radial stiffness kN/m
            "damping": 0.02,
            "moi": 0.085,          # rotational inertia
            "cor": 0.90,
            "friction": 0.005,     # bearing resistance
            "drag": 0.008          # aero CdA
        }
    }

    @classmethod
    def simulate_performance(cls, eq_type, params):
        """Simulates time-series dynamic responses and computes performance key metrics."""
        t = np.linspace(0, 0.05, 500)  # 50 ms impact / evaluation frame

        mass = params["mass"]
        k = params["stiffness"] * 1000.0  # Convert kN/m to N/m
        damping = params["damping"]
        moi = params["moi"]
        cor = params["cor"]
        friction = params["friction"]
        drag = params["drag"]

        # Natural frequency and damped oscillation modeling
        omega_n = np.sqrt(max(1.0, k / max(0.01, mass)))
        c_crit = 2.0 * np.sqrt(max(1.0, k * mass))
        c = damping * c_crit
        omega_d = omega_n * np.sqrt(max(0.001, 1.0 - min(0.99, damping**2)))

        # Transient Force / Impact Response Impulse
        F_peak = 2500.0 * (k / 50000.0)**0.4 * (1.0 + cor)
        impact_response = F_peak * np.exp(-damping * omega_n * t) * np.sin(omega_d * t)

        # Domain Specific Metrics & Time Curves
        if eq_type in ["Racket", "Bat"]:
            # Swing dynamics & Exit Ball Velocity Mechanics
            swing_force = 350.0  # N applied athlete torque force
            swing_speed_mps = (swing_force * 0.35 / max(0.005, moi))**0.5 * 0.8
            pitch_speed_mps = 35.0  # Incoming ball speed ~78 mph

            # Collision mechanics (Cons. of momentum + COR)
            m_ball = 0.058 if eq_type == "Racket" else 0.160
            v_exit_mps = (mass * swing_speed_mps * (1.0 + cor) + m_ball * pitch_speed_mps * (cor - 1.0)) / (mass + m_ball)
            v_exit_kmh = max(0.0, v_exit_mps * 3.6)

            primary_metric_label = "Ball Exit Velocity"
            primary_metric_val = f"{v_exit_kmh:.1f} km/h"

            # Score formula
            score = (v_exit_kmh / 160.0) * 50.0 + (cor * 30.0) - (moi * 80.0) + (1.0 - drag) * 20.0
            
            curve_y = impact_response
            curve_label = "Impact Force Transient (N)"

        elif eq_type == "Shoe":
            # Energy Return, Shock Absorption, Traction
            impact_energy = 0.5 * mass * (4.5**2)  # Foot strike impact
            absorbed_energy = impact_energy * (1.0 - cor)
            energy_return_pct = cor * 100.0
            peak_shock_g = (F_peak / (mass * 9.81)) * (1.0 - damping)

            primary_metric_label = "Energy Return"
            primary_metric_val = f"{energy_return_pct:.1f} %"

            score = (energy_return_pct * 0.4) + (friction * 35.0) + (damping * 25.0) - (mass * 40.0)
            
            curve_y = F_peak * np.exp(-damping * omega_n * t)
            curve_label = "Ground Force Dissipation (N)"

        elif eq_type == "Helmet":
            # Head Injury Criterion (HIC) & Shock Attenuation
            peak_accel_g = (F_peak / (4.5 * 9.81)) * (1.0 - damping)  # 4.5kg headform
            hic_estimate = (peak_accel_g**2.5) * 0.015 * (1.0 - damping)

            primary_metric_label = "Peak Head Acceleration"
            primary_metric_val = f"{peak_accel_g:.1f} G"

            score = max(0.0, 100.0 - (peak_accel_g * 0.4) - (mass * 50.0) + (damping * 40.0))
            
            curve_y = (F_peak / 4.5) * np.exp(-damping * omega_n * t) / 9.81
            curve_label = "Headform Acceleration (G)"

        else:  # Bicycle Component
            # Aerodynamic Drag Power Loss & Stiffness-to-Weight
            v_bike_mps = 12.5  # 45 km/h TT speed
            aero_drag_power_watts = 0.5 * 1.225 * drag * (v_bike_mps**3)
            stiffness_to_weight = (k / 1000.0) / max(0.05, mass)

            primary_metric_label = "Aero Power Loss"
            primary_metric_val = f"{aero_drag_power_watts:.2f} W"

            score = (stiffness_to_weight * 0.3) - (aero_drag_power_watts * 2.0) - (mass * 60.0) - (moi * 100.0)
            
            curve_y = aero_drag_power_watts + (impact_response * 0.01)
            curve_label = "Power Loss & Frame Flex (W)"

        score = max(0.0, min(100.0, score))

        metrics = {
            primary_metric_label: primary_metric_val,
            "Impact Peak Force": f"{F_peak:.0f} N",
            "Natural Frequency": f"{omega_n / (2 * np.pi):.1f} Hz",
            "Damping Ratio": f"{damping:.2f}",
            "Overall Performance Score": f"{score:.1f} / 100"
        }

        return {
            "time": t,
            "curve_y": curve_y,
            "curve_label": curve_label,
            "score": score,
            "metrics": metrics
        }

    @classmethod
    def run_sensitivity_analysis(cls, eq_type, base_params):
        """Evaluates overall score sensitivity to ±15% parameter variations."""
        base_score = cls.simulate_performance(eq_type, base_params)["score"]
        sensitivities = {}

        for param_name, base_val in base_params.items():
            if base_val == 0.0:
                continue
            
            # Plus 15% variation
            p_high = base_params.copy()
            p_high[param_name] = base_val * 1.15
            score_high = cls.simulate_performance(eq_type, p_high)["score"]

            # Score derivative impact
            delta_score = score_high - base_score
            sensitivities[param_name] = delta_score

        return sensitivities

    @classmethod
    def optimize_parameters(cls, eq_type, target_objective="Maximize Overall Performance"):
        """Finds optimal parameter combination using SciPy numerical optimization."""
        preset = cls.DEFAULT_PRESETS[eq_type]
        param_names = list(preset.keys())
        x0 = [preset[k] for k in param_names]

        # Bounds for parameters [mass, stiffness, damping, moi, cor, friction, drag]
        bounds = [
            (0.05, 2.5),     # mass
            (10.0, 300.0),   # stiffness
            (0.01, 0.80),    # damping
            (0.001, 0.60),   # moi
            (0.10, 0.95),    # cor
            (0.05, 1.20),    # friction
            (0.002, 0.20)    # drag
        ]

        def objective_func(x):
            params = {name: val for name, val in zip(param_names, x)}
            res = cls.simulate_performance(eq_type, params)
            # Minimize negative performance score
            return -res["score"]

        opt_res = minimize(objective_func, x0, method='L-BFGS-B', bounds=bounds)

        opt_params = {name: float(val) for name, val in zip(param_names, opt_res.x)}
        return opt_params


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sports Equipment Performance Simulator")
        self.setGeometry(50, 50, 1480, 920)

        self.spin_boxes = {}
        self.current_res = None

        self.init_ui()
        self.load_preset_defaults()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sidebar Controls
        sidebar = QGroupBox("Equipment Parameter Definition")
        sidebar_layout = QVBoxLayout(sidebar)
        form = QFormLayout()

        self.cmb_eq_type = QComboBox()
        self.cmb_eq_type.addItems(EquipmentPhysicsEngine.EQUIPMENT_TYPES)
        self.cmb_eq_type.currentTextChanged.connect(self.load_preset_defaults)

        form.addRow("Equipment Category:", self.cmb_eq_type)

        # Parameter Spin Boxes
        param_configs = [
            ("mass", "Mass (kg):", 0.01, 5.0, 0.01, 3),
            ("stiffness", "Stiffness (kN/m):", 1.0, 500.0, 1.0, 1),
            ("damping", "Damping Ratio (ζ):", 0.001, 1.0, 0.01, 3),
            ("moi", "Moment of Inertia (kg·m²):", 0.0001, 1.0, 0.005, 4),
            ("cor", "Coeff. of Restitution (COR):", 0.05, 0.98, 0.01, 2),
            ("friction", "Friction Coefficient (μ):", 0.01, 2.0, 0.02, 2),
            ("drag", "Aero Drag (CdA m²):", 0.001, 0.50, 0.002, 3)
        ]

        for p_key, p_label, min_v, max_v, step_v, decimals in param_configs:
            spn = QDoubleSpinBox()
            spn.setRange(min_v, max_v)
            spn.setSingleStep(step_v)
            spn.setDecimals(decimals)
            spn.valueChanged.connect(self.run_simulation)
            self.spin_boxes[p_key] = spn
            form.addRow(p_label, spn)

        sidebar_layout.addLayout(form)

        btn_run = QPushButton("Run Simulation")
        btn_run.setStyleSheet("background-color: #1A237E; color: white; font-weight: bold; padding: 8px;")
        btn_run.clicked.connect(self.run_simulation)
        sidebar_layout.addWidget(btn_run)

        btn_optimize = QPushButton("Optimize Parameters (SciPy)")
        btn_optimize.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold; padding: 8px;")
        btn_optimize.clicked.connect(self.optimize_equipment)
        sidebar_layout.addWidget(btn_optimize)

        self.lbl_score = QLabel("Overall Score: -- / 100")
        self.lbl_score.setStyleSheet("font-size: 15px; font-weight: bold; color: #1A237E; padding: 10px; border: 2px solid #1A237E; border-radius: 5px;")
        sidebar_layout.addWidget(self.lbl_score)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar, stretch=1)

        # Right Area Splitter
        splitter = QSplitter(Qt.Horizontal)

        # Plots Column
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        self.fig = Figure(figsize=(7, 8))
        self.canvas = FigureCanvas(self.fig)
        graph_layout.addWidget(self.canvas)
        splitter.addWidget(graph_widget)

        # Dashboard Tabs Area
        dash_widget = QWidget()
        dash_layout = QVBoxLayout(dash_widget)
        self.tabs = QTabWidget()

        # Tab 1: Simulated Metrics Table
        tab_metrics = QWidget()
        lay_metrics = QVBoxLayout(tab_metrics)
        self.table_metrics = QTableWidget()
        lay_metrics.addWidget(self.table_metrics)
        self.tabs.addTab(tab_metrics, "Performance Metrics")

        # Tab 2: Parameter Sensitivity Breakdown
        tab_sens = QWidget()
        lay_sens = QVBoxLayout(tab_sens)
        self.table_sens = QTableWidget()
        lay_sens.addWidget(self.table_sens)
        self.tabs.addTab(tab_sens, "Sensitivity Analysis")

        # Tab 3: Benchmarking & Optimization Log
        tab_log = QWidget()
        lay_log = QVBoxLayout(tab_log)
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("font-size: 13px; line-height: 1.4; padding: 10px;")
        lay_log.addWidget(self.txt_log)
        self.tabs.addTab(tab_log, "Optimization Log")

        dash_layout.addWidget(self.tabs)
        splitter.addWidget(dash_widget)

        splitter.setSizes([850, 450])
        main_layout.addWidget(splitter, stretch=3)

    def load_preset_defaults(self):
        eq_type = self.cmb_eq_type.currentText()
        preset = EquipmentPhysicsEngine.DEFAULT_PRESETS.get(eq_type, {})
        for p_key, spn in self.spin_boxes.items():
            if p_key in preset:
                spn.blockSignals(True)
                spn.setValue(preset[p_key])
                spn.blockSignals(False)
        self.run_simulation()

    def get_current_params(self):
        return {p_key: spn.value() for p_key, spn in self.spin_boxes.items()}

    def run_simulation(self):
        eq_type = self.cmb_eq_type.currentText()
        params = self.get_current_params()

        self.current_res = EquipmentPhysicsEngine.simulate_performance(eq_type, params)
        sensitivities = EquipmentPhysicsEngine.run_sensitivity_analysis(eq_type, params)

        self.lbl_score.setText(f"Overall Score: {self.current_res['score']:.1f} / 100")

        self.plot_visualizations(sensitivities)
        self.update_metrics_table()
        self.update_sensitivity_table(sensitivities)

    def plot_visualizations(self, sensitivities):
        self.fig.clear()
        eq_type = self.cmb_eq_type.currentText()
        res = self.current_res

        # Subplot 1: Transient Dynamic Performance Curve
        ax1 = self.fig.add_subplot(211)
        ax1.plot(res["time"] * 1000.0, res["curve_y"], 'b-', lw=2, label=res["curve_label"])
        ax1.set_title(f"{eq_type} Transient Dynamic Response")
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel(res["curve_label"])
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc="upper right", fontsize=8)

        # Subplot 2: Parameter Sensitivity Tornado Chart (Impact on overall score)
        ax2 = self.fig.add_subplot(212)
        params_list = list(sensitivities.keys())
        impacts = [sensitivities[p] for p in params_list]

        y_pos = np.arange(len(params_list))
        bar_colors = ['green' if x >= 0 else 'red' for x in impacts]

        ax2.barh(y_pos, impacts, align='center', color=bar_colors, alpha=0.75)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(params_list)
        ax2.axvline(0, color='black', lw=1)
        ax2.set_title("Parameter Sensitivity (+15% Parameter Variation Impact on Score)")
        ax2.set_xlabel("Score Change (Points)")
        ax2.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def update_metrics_table(self):
        self.table_metrics.clear()
        m = self.current_res["metrics"]

        self.table_metrics.setRowCount(len(m))
        self.table_metrics.setColumnCount(2)
        self.table_metrics.setHorizontalHeaderLabels(["Performance Characteristic", "Simulated Metric"])

        for idx, (param, val) in enumerate(m.items()):
            self.table_metrics.setItem(idx, 0, QTableWidgetItem(param))
            self.table_metrics.setItem(idx, 1, QTableWidgetItem(val))

        self.table_metrics.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_sensitivity_table(self, sensitivities):
        self.table_sens.clear()
        self.table_sens.setRowCount(len(sensitivities))
        self.table_sens.setColumnCount(2)
        self.table_sens.setHorizontalHeaderLabels(["Design Parameter", "Score Sensitivity (+15% Delta)"])

        for idx, (p_name, delta) in enumerate(sensitivities.items()):
            self.table_sens.setItem(idx, 0, QTableWidgetItem(p_name))
            self.table_sens.setItem(idx, 1, QTableWidgetItem(f"{delta:+.2f} pts"))

        self.table_sens.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def optimize_equipment(self):
        eq_type = self.cmb_eq_type.currentText()
        opt_params = EquipmentPhysicsEngine.optimize_parameters(eq_type)

        # Apply optimized values to spin boxes
        for p_key, val in opt_params.items():
            if p_key in self.spin_boxes:
                self.spin_boxes[p_key].blockSignals(True)
                self.spin_boxes[p_key].setValue(val)
                self.spin_boxes[p_key].blockSignals(False)

        self.run_simulation()

        opt_res = self.current_res
        html = f"<h2>Parameter Optimization Completed ({eq_type})</h2>"
        html += f"<p>Optimized Score Target Achieved: <b style='color:#2E7D32;'>{opt_res['score']:.1f} / 100</b></p>"
        html += "<h3>Recommended Design Specifications:</h3><ul>"
        for p_name, val in opt_params.items():
            html += f"<li><b>{p_name}:</b> {val:.4f}</li>"
        html += "</ul>"

        self.txt_log.setHtml(html)
        self.tabs.setCurrentIndex(2)  # Switch to log tab
        QMessageBox.information(self, "Optimization Complete", f"SciPy optimization finished!\nNew Performance Score: {opt_res['score']:.1f} / 100")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())