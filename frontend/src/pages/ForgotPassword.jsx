import { useState } from "react";
import axios from "../api/axios";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [step, setStep] = useState(1);

  const sendOtp = async () => {
    try {
      await axios.post("/forgot-password", { email });
      alert("OTP sent to your email");
      setStep(2);
    } catch (error) {
      alert(error.response?.data?.detail || "Failed to send OTP");
    }
  };

  const verifyOtp = async () => {
    try {
      await axios.post("/verify-otp", { email, otp });
      alert("OTP verified");
      setStep(3);
    } catch (error) {
      alert(error.response?.data?.detail || "Invalid OTP");
    }
  };

  const resetPassword = async () => {
    try {
      await axios.post("/reset-password", {
        email,
        new_password: newPassword,
      });

      alert("Password reset successful");
      window.location.href = "/signin";
    } catch (error) {
      alert(error.response?.data?.detail || "Password reset failed");
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "400px" }}>
      <h3 className="text-center mb-4">Forgot Password</h3>

      {step === 1 && (
        <>
          <input
            type="email"
            className="form-control mb-3"
            placeholder="Enter registered email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button className="btn btn-primary w-100" onClick={sendOtp}>
            Send OTP
          </button>
        </>
      )}

      {step === 2 && (
        <>
          <input
            type="text"
            className="form-control mb-3"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
          />

          <button className="btn btn-success w-100" onClick={verifyOtp}>
            Verify OTP
          </button>
        </>
      )}

      {step === 3 && (
        <>
          <input
            type="password"
            className="form-control mb-3"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />

          <button className="btn btn-danger w-100" onClick={resetPassword}>
            Reset Password
          </button>
        </>
      )}
    </div>
  );
}

export default ForgotPassword;