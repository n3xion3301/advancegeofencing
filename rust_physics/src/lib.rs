use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use std::f64::consts::PI;

#[derive(Debug, Clone)]
#[pyclass]
pub struct RelativisticParticle {
    #[pyo3(get, set)]
    velocity_c: f64,
    #[pyo3(get, set)]
    rest_mass: f64,
    #[pyo3(get, set)]
    charge: Option<f64>,
}

#[derive(Debug)]
pub enum ParticleState {
    Tardyonic { gamma: f64 },
    Luminal,
    Tachyonic { imaginary_gamma: f64 },
}

#[pymethods]
impl RelativisticParticle {
    #[new]
    fn new(velocity_c: f64, rest_mass: f64) -> Self {
        Self {
            velocity_c,
            rest_mass,
            charge: None,
        }
    }

    fn calculate_lorentz_factor(&self) -> PyResult<f64> {
        let v_squared = self.velocity_c.powi(2);
        let denominator = 1.0 - v_squared;
        
        const EPSILON: f64 = 1e-10;
        
        if denominator.abs() < EPSILON {
            Err(PyValueError::new_err("Particle at light speed (photon)"))
        } else if denominator > 0.0 {
            Ok(1.0 / denominator.sqrt())
        } else {
            let imaginary_gamma = 1.0 / (-denominator).sqrt();
            Err(PyValueError::new_err(format!(
                "Tachyonic: imaginary gamma = {}i", 
                imaginary_gamma
            )))
        }
    }

    fn get_particle_state(&self) -> String {
        let v_squared = self.velocity_c.powi(2);
        let denominator = 1.0 - v_squared;
        
        const EPSILON: f64 = 1e-10;
        
        if denominator.abs() < EPSILON {
            "luminal".to_string()
        } else if denominator > 0.0 {
            "tardyonic".to_string()
        } else {
            "tachyonic".to_string()
        }
    }

    fn relativistic_energy(&self) -> f64 {
        match self.calculate_lorentz_factor() {
            Ok(gamma) => gamma * self.rest_mass,
            Err(_) => f64::NAN,
        }
    }

    fn relativistic_momentum(&self) -> f64 {
        match self.calculate_lorentz_factor() {
            Ok(gamma) => gamma * self.rest_mass * self.velocity_c,
            Err(_) => f64::NAN,
        }
    }

    fn time_dilation(&self) -> f64 {
        match self.calculate_lorentz_factor() {
            Ok(gamma) => gamma,
            Err(_) => f64::NAN,
        }
    }

    fn length_contraction(&self) -> f64 {
        match self.calculate_lorentz_factor() {
            Ok(gamma) => 1.0 / gamma,
            Err(_) => f64::NAN,
        }
    }

    fn get_analysis(&self) -> String {
        let state = self.get_particle_state();
        
        let mut output = String::new();
        output.push_str(&format!("Velocity: {:.4}c\n", self.velocity_c));
        output.push_str(&format!("Rest Mass: {:.4}\n", self.rest_mass));
        output.push_str(&format!("State: {}\n", state));
        
        match self.calculate_lorentz_factor() {
            Ok(gamma) => {
                output.push_str(&format!("Lorentz Factor: {:.6}\n", gamma));
                output.push_str(&format!("Energy: {:.6}\n", self.relativistic_energy()));
                output.push_str(&format!("Momentum: {:.6}\n", self.relativistic_momentum()));
                output.push_str(&format!("Time Dilation: {:.6}x\n", gamma));
                output.push_str(&format!("Length Contraction: {:.6}x\n", 1.0/gamma));
            }
            Err(e) => {
                output.push_str(&format!("Error: {}\n", e));
            }
        }
        
        output
    }

    fn __repr__(&self) -> String {
        format!(
            "RelativisticParticle(v={:.3}c, m={:.3}, state={})",
            self.velocity_c,
            self.rest_mass,
            self.get_particle_state()
        )
    }
}

#[pyfunction]
fn create_electron(velocity_c: f64) -> RelativisticParticle {
    RelativisticParticle {
        velocity_c,
        rest_mass: 9.109e-31,
        charge: Some(-1.602e-19),
    }
}

#[pyfunction]
fn create_proton(velocity_c: f64) -> RelativisticParticle {
    RelativisticParticle {
        velocity_c,
        rest_mass: 1.673e-27,
        charge: Some(1.602e-19),
    }
}

#[pyfunction]
fn create_photon() -> RelativisticParticle {
    RelativisticParticle {
        velocity_c: 1.0,
        rest_mass: 0.0,
        charge: None,
    }
}

#[pyfunction]
fn create_tachyon(velocity_c: f64) -> RelativisticParticle {
    if velocity_c <= 1.0 {
        panic!("Tachyon must have v > c");
    }
    RelativisticParticle {
        velocity_c,
        rest_mass: 1.0,
        charge: None,
    }
}

#[pymodule]
fn relativistic_physics(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RelativisticParticle>()?;
    m.add_function(wrap_pyfunction!(create_electron, m)?)?;
    m.add_function(wrap_pyfunction!(create_proton, m)?)?;
    m.add_function(wrap_pyfunction!(create_photon, m)?)?;
    m.add_function(wrap_pyfunction!(create_tachyon, m)?)?;
    Ok(())
}
