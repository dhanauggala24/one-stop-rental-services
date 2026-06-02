import { Link } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

function Navbar() {
  const token = localStorage.getItem("token");

  let role = "";
  let email = "";

  if (token) {
    const decoded = jwtDecode(token);
    role = decoded.role;
    email = decoded.email;
  }

  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <Link
        className="navbar-brand fw-bold"
        to={role === "admin" ? "/admin-dashboard" : "/user-dashboard"}
      >
        One Stop Rentals
      </Link>

      <div className="navbar-nav">
        {role === "user" && (
          <>
            <Link className="nav-link" to="/user-dashboard">
              Categories
            </Link>

            <Link className="nav-link" to="/items">
              All Items
            </Link>

            <Link className="nav-link" to="/cart">
              Cart
            </Link>

            <Link className="nav-link" to="/my-bookings">
              My Bookings
            </Link>

            <Link className="nav-link" to="/create-item">
              Request/Add Item
            </Link>
          </>
        )}

        {role === "admin" && (
          <>
            <Link className="nav-link" to="/admin-dashboard">
              Admin Dashboard
            </Link>

            <Link className="nav-link" to="/items">
              All Items
            </Link>
          </>
        )}
      </div>

      <div className="dropdown ms-auto">
        <button
          className="btn btn-outline-light dropdown-toggle"
          type="button"
          data-bs-toggle="dropdown"
        >
          👤 {role}
        </button>

        <ul className="dropdown-menu dropdown-menu-end">
          <li>
            <span className="dropdown-item-text">{email}</span>
          </li>

          <li>
            <span className="dropdown-item-text text-muted">
              Role: {role}
            </span>
          </li>

          <li>
            <hr className="dropdown-divider" />
          </li>

          <li>
            <button className="dropdown-item" onClick={logout}>
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;