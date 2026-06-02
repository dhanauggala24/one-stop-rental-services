import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await API.post("/login", {
        email,
        password,
      });

      const token = response.data.access_token;

      localStorage.setItem("token", token);

      const decoded = JSON.parse(atob(token.split(".")[1]));

      alert("Login Successful");

      if (decoded.role === "user") {
        navigate("/user-dashboard");
      } else if (decoded.role === "admin") {
        navigate("/admin-dashboard");
      } else {
        alert("Invalid role. Only user and admin are allowed.");
        localStorage.removeItem("token");
        navigate("/login");
      }
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Invalid Credentials");
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow p-4" style={{ width: "400px" }}>
        <h2 className="text-center mb-4">Login</h2>

        <input
          type="email"
          className="form-control mb-3"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="btn btn-primary w-100" onClick={handleLogin}>
          Login
        </button>

        <p className="text-center mt-3">
          Don&apos;t have an account? <Link to="/register">Register</Link>
        </p>

        <p className="text-center">
          <Link to="/forgot-password">Forgot Password?</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;