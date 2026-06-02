import { useNavigate } from "react-router-dom";

function LoginSelector() {
  const navigate = useNavigate();

  return (
    <div className="login-selector-page">
      <div className="login-overlay">
        <div className="login-selector-card">
          <h1 className="login-title">
            Welcome to <br />
            One Stop Rental Services
          </h1>

          <p className="login-subtitle">
            Choose your portal to continue
          </p>

          <button
            className="login-option user-login"
            onClick={() => navigate("/signin")}
          >
            👤 User Login
          </button>

          <button
            className="login-option admin-login"
            onClick={() => navigate("/signin")}
          >
            🔐 Admin Login
          </button>

          <p className="register-link">
            New User?{" "}
            <span onClick={() => navigate("/register")}>
              Register Here
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginSelector;