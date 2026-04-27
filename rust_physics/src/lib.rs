use pyo3::prelude::*;
use pyo3::types::PyModule;

const C: f64 = 299_792_458.0; // Speed of light in m/s

#[pyclass]
struct RelativisticParticle {
    #[pyo3(get, set)]
    mass: f64,
    #[pyo3(get, set)]
    velocity: f64,
    #[pyo3(get, set)]
    charge: f64,
}

#[pymethods]
impl RelativisticParticle {
    #[new]
    fn new(mass: f64, velocity: f64, charge: f64) -> Self {
        RelativisticParticle { mass, velocity, charge }
    }

    fn gamma(&self) -> f64 {
        1.0 / (1.0 - (self.velocity / C).powi(2)).sqrt()
    }

    fn relativistic_mass(&self) -> f64 {
        self.mass * self.gamma()
    }

    fn kinetic_energy(&self) -> f64 {
        (self.gamma() - 1.0) * self.mass * C * C
    }

    fn momentum(&self) -> f64 {
        self.gamma() * self.mass * self.velocity
    }
}

#[pyfunction]
fn create_electron(velocity: f64) -> RelativisticParticle {
    RelativisticParticle::new(9.10938e-31, velocity, -1.602176e-19)
}

#[pyfunction]
fn create_proton(velocity: f64) -> RelativisticParticle {
    RelativisticParticle::new(1.67262e-27, velocity, 1.602176e-19)
}

#[pyfunction]
fn create_photon() -> RelativisticParticle {
    RelativisticParticle::new(0.0, C, 0.0)
}

#[pyfunction]
fn create_tachyon(velocity: f64) -> RelativisticParticle {
    RelativisticParticle::new(1e-30, velocity, 0.0)
}

#[pymodule]
fn relativistic_physics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RelativisticParticle>()?;
    m.add_function(wrap_pyfunction!(create_electron, m)?)?;
    m.add_function(wrap_pyfunction!(create_proton, m)?)?;
    m.add_function(wrap_pyfunction!(create_photon, m)?)?;
    m.add_function(wrap_pyfunction!(create_tachyon, m)?)?;
    Ok(())
}
