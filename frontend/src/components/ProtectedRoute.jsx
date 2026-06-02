import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

function ProtectedRoute({ children, allowedRoles }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  let role;

  try {
    const decoded = jwtDecode(token);
    role = decoded.role;
  } catch (error) {
    console.log("Invalid token:", error);
    localStorage.removeItem("token");
    return <Navigate to="/" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    if (role === "user") {
      return <Navigate to="/user-dashboard" replace />;
    }

    if (role === "admin") {
      return <Navigate to="/admin-dashboard" replace />;
    }

    localStorage.removeItem("token");
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;