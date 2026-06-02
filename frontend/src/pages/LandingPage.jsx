import { Link } from "react-router-dom";

function LandingPage() {
  return (
    <div>
      <nav className="navbar navbar-dark bg-dark px-4">
        <Link className="navbar-brand" to="/">
          One Stop Rental Services
        </Link>

        <div>
          <Link className="btn btn-outline-light me-2" to="/login">
            Login
          </Link>

          <Link className="btn btn-warning" to="/register">
            Register
          </Link>
        </div>
      </nav>

      <section className="text-center p-5 bg-light">
        <h1 className="display-4 fw-bold">
          Rent Anything, Anytime
        </h1>

        <p className="lead mt-3">
          Find properties, vehicles, cameras, equipment, and camping items in one place.
        </p>

        <Link className="btn btn-primary btn-lg mt-3" to="/login">
          Browse Rentals
        </Link>
      </section>

      <div className="container mt-5">
        <h2 className="text-center mb-4">Rental Categories</h2>

        <div className="row">
          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>🏠</h3>
              <h5>Property Rentals</h5>
              <p>Homes, rooms, and vacation stays.</p>
            </div>
          </div>

          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>🚗</h3>
              <h5>Vehicles</h5>
              <p>Cars, bikes, and travel rentals.</p>
            </div>
          </div>

          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>📷</h3>
              <h5>Photography</h5>
              <p>Cameras, drones, and shooting gear.</p>
            </div>
          </div>

          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>🔧</h3>
              <h5>Equipment</h5>
              <p>Tools, projectors, and event equipment.</p>
            </div>
          </div>

          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>🏕️</h3>
              <h5>Camping</h5>
              <p>Tents, trekking kits, and outdoor gear.</p>
            </div>
          </div>

          <div className="col-md-4 mb-4">
            <div className="card shadow text-center p-4">
              <h3>✅</h3>
              <h5>Verified Providers</h5>
              <p>Providers are approved by admin.</p>
            </div>
          </div>
        </div>
      </div>

      <footer className="text-center bg-dark text-white p-3 mt-5">
        One Stop Rental Services © 2026
      </footer>
    </div>
  );
}

export default LandingPage;