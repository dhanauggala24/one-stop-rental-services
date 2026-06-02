import { jwtDecode } from "jwt-decode";

function ProtectedRoute({ children, allowedRoles }) {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "/";
    return null;
  }

  const decoded = jwtDecode(token);
  const role = decoded.role;

  if (allowedRoles && !allowedRoles.includes(role)) {
    if (role === "user") {
      window.location.href = "/user-dashboard";
    } else if (role === "provider") {
      window.location.href = "/provider-dashboard";
    } else if (role === "admin") {
      window.location.href = "/admin-dashboard";
    }

    return null;
  }

  return children;
}

export default ProtectedRoute;