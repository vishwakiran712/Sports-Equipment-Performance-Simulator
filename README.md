# 🏆 Sports Equipment Performance Simulator

> **Sports Technology • Sports Engineering • Physics Simulation • Product Design • Performance Engineering • Numerical Optimization • Python**

An interactive **sports-equipment physics and performance simulation platform** for evaluating how equipment design parameters influence dynamic response, performance, impact behavior, energy transfer, and overall performance scores.

The simulator supports five equipment domains:

* 🎾 Racket
* 🏏 Bat
* 👟 Shoe
* 🪖 Helmet
* 🚴 Bicycle Component

Users can modify physical and engineering parameters, run simulations, analyze parameter sensitivity, and use numerical optimization to search for improved equipment configurations.

<img width="913" height="479" alt="image" src="https://github.com/user-attachments/assets/19bcda1f-a446-4ac9-b1e7-37fae533c2fd" />


---

# 🎯 Project Overview

Sports equipment performance is governed by a combination of:

* Mass
* Stiffness
* Damping
* Moment of inertia
* Coefficient of restitution
* Friction
* Aerodynamic drag

This project converts these engineering parameters into simulated performance characteristics using simplified physics-based models.

```text
             EQUIPMENT DESIGN
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      MASS      STIFFNESS     DAMPING
        │           │           │
        └───────────┼───────────┘
                    ▼
             DYNAMIC MODEL
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
       COR         MOI        FRICTION
        │           │           │
        └───────────┼───────────┘
                    ▼
              PERFORMANCE
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      SPEED       FORCE       ENERGY
                    │
                    ▼
             PERFORMANCE SCORE
```

---

# 🧩 Equipment Domains

## 🎾 Racket

The racket model evaluates swing and ball-exit mechanics using parameters such as:

* Racket mass
* Stiffness
* Damping
* Moment of inertia
* Coefficient of restitution
* String/ball friction
* Aerodynamic drag

The simulator estimates **ball exit velocity**, impact response and an overall performance score.

---

## 🏏 Bat

The bat model evaluates:

* Bat mass
* Structural stiffness
* Damping
* Moment of inertia
* Coefficient of restitution
* Friction
* Aerodynamic drag

A simplified collision model estimates the resulting **ball exit velocity**.

The implementation uses conservation-of-momentum and coefficient-of-restitution concepts to model the collision between the bat and incoming ball.

---

## 👟 Shoe

The shoe model focuses on:

* Energy return
* Shock absorption
* Ground interaction
* Traction
* Mass
* Midsole stiffness
* Damping

The simulation calculates an estimated:

* Energy return percentage
* Impact energy
* Absorbed energy
* Peak shock response
* Performance score

---

## 🪖 Helmet

The helmet model focuses on **impact attenuation and head acceleration**.

Key parameters include:

* Helmet mass
* Liner stiffness
* Damping
* Coefficient of restitution
* Impact response

The model estimates:

* Peak head acceleration
* Impact force
* Shock attenuation
* Approximate HIC-style metric
* Overall performance score

> ⚠️ The helmet calculations are a simplified engineering model and are **not a certified injury-assessment method**.

---

## 🚴 Bicycle Component

The bicycle-component model focuses on the relationship between:

* Mass
* Structural stiffness
* Moment of inertia
* Aerodynamic drag

The simulator estimates:

* Aerodynamic power loss
* Stiffness-to-weight ratio
* Frame/component dynamic response
* Overall performance score

The current model uses a representative cycling speed of **12.5 m/s (45 km/h)** for the aerodynamic calculation.

---

# ⚙️ Engineering Parameters

The simulator exposes seven primary design parameters:

| Parameter                      | Engineering Meaning                   |
| ------------------------------ | ------------------------------------- |
| **Mass**                       | Equipment weight                      |
| **Stiffness**                  | Resistance to deformation             |
| **Damping**                    | Energy dissipation                    |
| **Moment of Inertia**          | Resistance to rotational acceleration |
| **Coefficient of Restitution** | Elasticity of collision               |
| **Friction**                   | Surface/contact interaction           |
| **Aerodynamic Drag**           | Resistance due to air                 |

These parameters can be adjusted interactively through the GUI.

---

# 🧮 Physics Engine

The core simulation is implemented through the `EquipmentPhysicsEngine` class.

The model evaluates a **50 ms transient response window** with 500 time points.

```text
t = 0 ───────────────────────────────► 50 ms
       │
       │  Dynamic / Impact Response
       │
       ▼
   Equipment
       │
       ▼
   Physical Model
       │
       ▼
   Time-Series Response
```

---

# 📐 Natural Frequency

The simulator calculates the undamped natural frequency using:

```text
              k
ωₙ = √( ───────── )
              m
```

Where:

* `ωₙ` = natural angular frequency
* `k` = stiffness
* `m` = mass

The corresponding frequency is reported in Hz.

---

# 🌀 Damping Model

The model calculates critical damping and uses the specified damping ratio to determine the damped response.

```text
Undamped System
      │
      ▼
Natural Frequency
      │
      ▼
Damping Ratio
      │
      ▼
Damped Response
      │
      ▼
Transient Decay
```

The resulting transient response is used to visualize how the equipment responds following an impact or dynamic event.

---

# 💥 Impact Response

A simplified transient impact-force model is generated from:

* Equipment stiffness
* Coefficient of restitution
* Damping
* Natural frequency

Conceptually:

```text
              IMPACT
                 │
                 ▼
          ┌─────────────┐
          │   STIFFNESS │
          └──────┬──────┘
                 │
                 ▼
           IMPACT FORCE
                 │
        ┌────────┴────────┐
        ▼                 ▼
     DAMPING             COR
        │                 │
        └────────┬────────┘
                 ▼
          TRANSIENT RESPONSE
```

---

# 🏏🎾 Ball Exit Velocity

For racket and bat simulations, the model estimates ball exit velocity using a simplified collision model.

```text
ATHLETE
   │
   ▼
SWING
   │
   ▼
BAT / RACKET
   │
   ▼
COLLISION
   │
   ├──── MASS
   ├──── MOMENT OF INERTIA
   ├──── COR
   └──── INCOMING BALL SPEED
   │
   ▼
BALL EXIT VELOCITY
```

The current model assumes:

* An applied swing force
* A representative incoming ball velocity
* Equipment mass
* Coefficient of restitution
* Equipment rotational inertia

The resulting value is reported in **km/h**.

---

# 👟 Shoe Energy Model

For footwear, the simulator calculates impact energy using:

```text
E = ½mv²
```

It then estimates the portion absorbed and returned based on the simplified equipment parameters.

```text
FOOT STRIKE
     │
     ▼
IMPACT ENERGY
     │
     ├──────────────┐
     ▼              ▼
ABSORBED          RETURNED
ENERGY            ENERGY
     │              │
     └──────┬───────┘
            ▼
      SHOE PERFORMANCE
```

---

# 🪖 Helmet Impact Model

Helmet performance is modeled around impact force and headform acceleration.

```text
              IMPACT
                 │
                 ▼
             HELMET
                 │
                 ▼
          ENERGY ABSORPTION
                 │
                 ▼
          HEADFORM RESPONSE
                 │
                 ▼
        PEAK ACCELERATION
                 │
                 ▼
          PERFORMANCE SCORE
```

The implementation uses a simplified **4.5 kg headform assumption** when estimating peak acceleration.

---

# 🚴 Aerodynamic Power Loss

For bicycle components, aerodynamic power loss is modeled using:

```text
P = ½ρ(CdA)v³
```

Where:

* `P` = aerodynamic power loss
* `ρ` = air density
* `CdA` = aerodynamic drag area
* `v` = cycling velocity

The model therefore allows aerodynamic drag to be evaluated alongside mass and structural characteristics.

---

# 📊 Performance Scoring

Each equipment category generates an **Overall Performance Score from 0–100**.

The scoring model is equipment-specific.

```text
                 EQUIPMENT
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       PHYSICS     DYNAMICS   DESIGN
          │          │          │
          └──────────┼──────────┘
                     ▼
             PERFORMANCE MODEL
                     │
                     ▼
              SCORE / 100
```

Different equipment categories prioritize different characteristics.

For example:

```text
RACKET / BAT
    ↓
Ball Exit Velocity
    +
COR
    +
Rotational Inertia
    +
Aerodynamics


SHOE
    ↓
Energy Return
    +
Traction
    +
Damping
    +
Mass


HELMET
    ↓
Shock Attenuation
    +
Head Acceleration
    +
Damping
    +
Mass


BICYCLE COMPONENT
    ↓
Stiffness-to-Weight
    +
Aerodynamics
    +
Rotational Inertia
```

---

# 📈 Sensitivity Analysis

The simulator performs parameter sensitivity analysis by increasing each non-zero parameter by **15%** and measuring the resulting change in overall performance score.

```text
BASE CONFIGURATION
        │
        ▼
   PERFORMANCE SCORE
        │
        ├── Mass +15%
        ├── Stiffness +15%
        ├── Damping +15%
        ├── MOI +15%
        ├── COR +15%
        ├── Friction +15%
        └── Drag +15%
        │
        ▼
   SCORE DIFFERENCE
        │
        ▼
 PARAMETER SENSITIVITY
```

This helps answer:

> **Which equipment parameter has the greatest influence on simulated performance?**

---

# 🌪️ Sensitivity Tornado Chart

The GUI visualizes sensitivity using a horizontal bar chart.

```text
Parameter       Score Impact

Stiffness       ███████████ +
COR             ███████     +
Mass            ███         -
MOI             █████       -
Drag            ██          -
```

A positive value indicates that increasing the parameter improves the simulated score, while a negative value indicates a reduction.

---

# 🤖 Numerical Optimization

The simulator includes an optimization engine based on **SciPy's L-BFGS-B algorithm**.

The optimizer searches within predefined physical parameter bounds to maximize the simulated performance score.

```text
INITIAL DESIGN
      │
      ▼
PARAMETER SPACE
      │
      ▼
NUMERICAL OPTIMIZER
      │
      ├── Mass
      ├── Stiffness
      ├── Damping
      ├── MOI
      ├── COR
      ├── Friction
      └── Drag
      │
      ▼
MAXIMUM SCORE
      │
      ▼
OPTIMIZED DESIGN
```

This transforms the application from a simple simulator into a basic **computational design-optimization platform**.

---

# 🧠 Design Optimization Concept

The project demonstrates a simplified engineering workflow:

```text
DESIGN
  │
  ▼
SIMULATE
  │
  ▼
MEASURE
  │
  ▼
ANALYZE
  │
  ▼
OPTIMIZE
  │
  ▼
NEW DESIGN
  │
  └──────────────► ITERATE
```

This approach can be extended to real sports-equipment development.

---

# 🖥️ Application Interface

The application provides an interactive desktop dashboard.

```text
┌──────────────────────────────────────────────────────────────┐
│          SPORTS EQUIPMENT PERFORMANCE SIMULATOR              │
├──────────────────────┬───────────────────────────────────────┤
│                      │                                       │
│ EQUIPMENT PARAMETERS │       DYNAMIC RESPONSE GRAPH          │
│                      │                                       │
│ Category             │                                       │
│ Mass                 │                                       │
│ Stiffness            │                                       │
│ Damping              │                                       │
│ Moment of Inertia    │                                       │
│ COR                  │                                       │
│ Friction             │                                       │
│ Aerodynamic Drag     │                                       │
│                      │                                       │
│ [Run Simulation]     │                                       │
│ [Optimize]           │                                       │
│                      │                                       │
│ Score: XX / 100      │                                       │
├──────────────────────┴───────────────────────────────────────┤
│ Performance Metrics │ Sensitivity │ Optimization Log         │
└──────────────────────────────────────────────────────────────┘
```

The current implementation contains:

* Equipment selection
* Parameter controls
* Run Simulation button
* SciPy optimization
* Dynamic response visualization
* Performance metrics table
* Sensitivity-analysis table
* Optimization log

---

# 📊 Dashboard Outputs

## Performance Metrics

The simulator reports:

* Primary equipment-specific performance metric
* Impact peak force
* Natural frequency
* Damping ratio
* Overall performance score

---

## Sensitivity Analysis

Displays the score change resulting from parameter perturbation.

```text
Parameter
    │
    ▼
+15% Variation
    │
    ▼
New Simulation
    │
    ▼
Δ Performance Score
```

---

## Optimization Log

The application records the result of the numerical optimization process and updates the equipment parameters with the optimized values.

---

# 🔬 Engineering Applications

This framework can be applied to early-stage sports-equipment research.

### Equipment Development

```text
Material
   ↓
Mass
   ↓
Stiffness
   ↓
Damping
   ↓
Dynamic Response
   ↓
Performance
```

### Product Optimization

```text
DESIGN VARIABLES
       ↓
PHYSICS MODEL
       ↓
PERFORMANCE SCORE
       ↓
SENSITIVITY
       ↓
OPTIMIZATION
       ↓
OPTIMIZED DESIGN
```

### Sports Engineering

Potential applications include:

* Racket design
* Cricket bat design
* Running shoe development
* Protective equipment research
* Bicycle component optimization
* Material-property studies
* Design-space exploration

---

# 🧪 Example Research Questions

The simulator can be used to explore questions such as:

### Racket

> How does increasing moment of inertia affect simulated ball-exit performance?

### Bat

> How does coefficient of restitution influence ball exit velocity?

### Shoe

> What is the trade-off between damping, energy return and traction?

### Helmet

> How does increasing damping affect simulated head acceleration?

### Bicycle Component

> How does reducing mass affect stiffness-to-weight performance while considering aerodynamic losses?

---

# 🛠️ Technology Stack

| Technology     | Purpose                   |
| -------------- | ------------------------- |
| **Python**     | Core programming language |
| **NumPy**      | Numerical calculations    |
| **SciPy**      | Numerical optimization    |
| **PyQt5**      | Desktop GUI               |
| **Matplotlib** | Engineering visualization |

The implementation directly uses NumPy for the physics calculations, SciPy's optimization routines for parameter optimization, PyQt5 for the interface, and Matplotlib for plotting.

---

# 📂 Project Structure

```text
Sports-Equipment-Performance-Simulator/
│
├── app.py
├── README.md
└── LICENSE
```

Core architecture:

```text
app.py
 │
 ├── EquipmentPhysicsEngine
 │   ├── Equipment Presets
 │   ├── Performance Simulation
 │   ├── Sensitivity Analysis
 │   └── Parameter Optimization
 │
 └── MainWindow
     ├── Equipment Controls
     ├── Simulation Dashboard
     ├── Performance Metrics
     ├── Sensitivity Analysis
     ├── Dynamic Graphs
     └── Optimization Log
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/vishwakiran712/Sports-Equipment-Performance-Simulator.git

cd Sports-Equipment-Performance-Simulator
```

## 2. Install dependencies

```bash
pip install numpy scipy matplotlib PyQt5
```

## 3. Run the application

```bash
python app.py
```

The **Sports Equipment Performance Simulator** desktop application will launch.

---

# 🧪 Basic Workflow

### Step 1 — Select Equipment

Choose:

```text
Racket
Bat
Shoe
Helmet
Bicycle Component
```

### Step 2 — Define Parameters

Adjust:

```text
Mass
Stiffness
Damping
Moment of Inertia
Coefficient of Restitution
Friction
Aerodynamic Drag
```

### Step 3 — Run Simulation

The physics engine calculates the equipment-specific dynamic response and performance metrics.

### Step 4 — Analyze Sensitivity

Investigate how a **+15% parameter change** influences the performance score.

### Step 5 — Optimize

Run the SciPy optimization engine to search for a higher-performing parameter configuration.

---

# 🔮 Development Roadmap

## Phase 1 — Physics Simulation

* [x] Multi-equipment simulation
* [x] Dynamic response modeling
* [x] Equipment-specific performance metrics
* [x] Performance scoring
* [x] Visualization

## Phase 2 — Engineering Analysis

* [x] Parameter sensitivity analysis
* [x] Transient response analysis
* [x] Natural-frequency calculations
* [x] Damping modeling
* [x] Stiffness-to-weight analysis

## Phase 3 — Optimization

* [x] Numerical optimization
* [x] Parameter bounds
* [x] Optimized equipment configurations
* [x] Optimization logging

## Phase 4 — Advanced Sports Engineering

* [ ] Material-property libraries
* [ ] Finite-element-model integration
* [ ] Experimental validation
* [ ] Real equipment datasets
* [ ] CAD parameter integration
* [ ] Multi-objective optimization

## Phase 5 — Digital Engineering Platform

* [ ] CAD-to-simulation workflow
* [ ] Material database
* [ ] Experimental test-data import
* [ ] Automated model calibration
* [ ] Pareto optimization
* [ ] Product-design comparison
* [ ] Digital twin integration

---

# 🏗️ Future Architecture

```text
                 SPORTS EQUIPMENT
                        │
                        ▼
                 CAD / DESIGN DATA
                        │
                        ▼
                 MATERIAL PROPERTIES
                        │
                        ▼
                 PHYSICS SIMULATION
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      Dynamics        Impact         Aerodynamics
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 PERFORMANCE MODEL
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Sensitivity      Validation      Optimization
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 OPTIMIZED DESIGN
                        │
                        ▼
                  PHYSICAL PROTOTYPE
                        │
                        ▼
                  EXPERIMENTAL TEST
                        │
                        └──────────────► MODEL UPDATE
```

---

# ⚠️ Model Limitations

This project uses **simplified physics-based models** intended for research, education and design exploration.

The results should not be interpreted as experimentally validated product-performance specifications.

Real sports-equipment behavior can depend on additional factors including:

* Material anisotropy
* Geometry
* Manufacturing tolerances
* Temperature
* Material nonlinearity
* Contact mechanics
* Boundary conditions
* Athlete technique
* Equipment orientation
* Ball/shuttle characteristics
* Real aerodynamic conditions
* Viscoelastic behavior
* Structural deformation

For production engineering, the models should be calibrated and validated against experimental testing and higher-fidelity numerical methods such as FEA.

---

# 📌 Project Status

**Status:** 🟢 Sports Engineering Prototype

### Current capabilities

* ✅ 5 equipment categories
* ✅ Physics-based simulation
* ✅ Dynamic response modeling
* ✅ Performance scoring
* ✅ Sensitivity analysis
* ✅ Numerical optimization
* ✅ Engineering visualization
* ✅ Interactive desktop GUI

### Future capabilities

* 🔄 Experimental validation
* 🔄 Material database
* 🔄 FEA integration
* 🔄 CAD integration
* 🔄 Multi-objective optimization
* 🔄 Digital-twin workflow

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Sports Technology • Biomechanics • Sports Engineering • AI & Computer Vision • Product Research

GitHub:
https://github.com/vishwakiran712

---

# 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## ⭐ Project Philosophy

> **Model the physics. Quantify performance. Optimize the design.**
