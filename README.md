# StellarLab Propulsion Simulator

StellarLab is an interactive rocket propulsion simulator built with Python. It allows users to model various rocket engine types, simulate complex multi-stage mission profiles, and visualize the results through a sleek, web-based user interface.

### Live Demo

Below is a snapshot of the interactive StellarLab dashboard.

<img width="1920" height="907" alt="image" src="https://github.com/user-attachments/assets/52fd2ac3-cfa9-4222-8d51-23ee4365e7e2" />
---

## Features

-   **Modular Engine Models**: Simulates different engine types (Liquid, Solid, Hybrid) with distinct characteristics like throttling and ignition delay.
-   **Advanced Physics Simulation**:
    -   Uses a Runge-Kutta (RK4) integrator via SciPy for accurate trajectory calculations.
    -   Models gravitational pull based on altitude.
    -   Simulates real-time mass depletion during flight.
-   **Multi-Stage Missions**: Define complex, multi-stage rockets with configurable payloads, fuel loads, and engines via simple JSON files.
-   **Data**:
    -   Live simulation log output directly in the UI.
    -   Key performance indicators (max altitude, velocity) are prominently displayed.
    -   Export full simulation data to CSV for external analysis.

---
<img width="3290" height="1742" alt="image" src="https://github.com/user-attachments/assets/2ae70b00-e192-498c-a741-a9bc37dac181" />

## Tech Stack

-   **Backend & Simulation**: Python 3.9+
-   **Physics & Numerics**: SciPy, NumPy
-   **Web UI**: Streamlit
-   **Data Visualization**: Plotly, Matplotlib
-   **Data Handling**: Pandas
-   **Configuration**: JSON

---

## Project Structure

The project is organized to be clean and scalable

```
StellarLab/
│
├── app.py                  # Main entry point for the Streamlit UI
├── data/
│   ├── engine_configs/     # JSON files for engine specs (e.g., merlin.json)
│   └── missions/           # JSON files for mission profiles (e.g., LEO.json)
│
├── src/
│   ├── engines/            # Engine models (liquid, solid, etc.)
│   ├── mission/            # Mission loading and trajectory simulation logic
│   ├── utils/              # Shared utilities and constants
│   └── visualization/      # Plotting functions
│
├── tests/                  # (Future) Unit and integration tests
├── README.md               # You are here rn hahahaha
└── requirements.txt        # Project dependencies
```

---

## Installation Guide

Follow these steps to get StellarLab running on your local machine.

**1. Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/StellarLab.git
cd StellarLab
```

**2. Create and Activate a Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python3 -m venv env

# Activate it (macOS/Linux)
source env/bin/activate

# Activate it (Windows)
.\env\Scripts\activate
```

**3. Install Dependencies**

Install all the necessary packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

---

## How to Run

With the environment activated and dependencies installed, launching the simulator is simple:

1.  Open your terminal in the root `StellarLab` directory.
2.  Run the following command:

    ```bash
    streamlit run app.py
    ```

3.  This will automatically open a new tab in your web browser with the StellarLab application running.

From there, you can select a mission from the sidebar and click "Launch Simulation" to see it in action.

---

## Customization

StellarLab is designed to be easily customized.

### Creating a New Engine

1.  Create a new `.json` file in the `data/engine_configs/` directory.
2.  Follow the structure of `merlin.json`, specifying the `type` ("LiquidEngine", "SolidEngine", or "HybridEngine") and its parameters (thrust, isp, etc.).

### Designing a New Mission

1.  Create a new `.json` file in the `data/missions/` directory.
2.  Define the stages of your rocket, specifying the mass properties and pointing to the engine configuration file you want each stage to use. You can have as many stages as you like.

```json
{
  "name": "My Custom Mission to Mars",
  "stages": [
    {
      "stage_name": "Booster Stage",
      "dry_mass": 100000,
      "fuel_mass": 2000000,
      "engine_config": "data/engine_configs/my_powerful_engine.json",
      "num_engines": 5
    },
    {
      "stage_name": "Transfer Stage",
      "dry_mass": 5000,
      "fuel_mass": 50000,
      "engine_config": "data/engine_configs/my_efficient_engine.json",
      "num_engines": 1
    }
  ]
}
