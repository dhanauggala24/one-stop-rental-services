import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function Dashboard() {
  const [message, setMessage] = useState("");
  const [user, setUser] = useState(null);

  const requestProvider = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.post(
        "/request-provider",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to request provider access");
    }
  };

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await API.get("/dashboard", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setMessage(response.data.message);
        setUser(response.data.user);
      } catch (error) {
        console.log(error.response?.data || error.message);
        alert("Please login again");
        window.location.href = "/";
      }
    };

    fetchDashboard();
  }, []);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <div className="card shadow p-4">
          <h1 className="mb-3">Dashboard</h1>

          <h4 className="text-success">{message}</h4>

          {user && (
            <div className="mt-4">
              <p>
                <strong>Email:</strong> {user.email}
              </p>

              <p>
                <strong>Role:</strong> {user.role}
              </p>

              <p>
                <strong>User ID:</strong> {user.user_id}
              </p>

              {user.role === "user" && (
                <button
                  className="btn btn-warning mt-3"
                  onClick={requestProvider}
                >
                  Request Provider Access
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;