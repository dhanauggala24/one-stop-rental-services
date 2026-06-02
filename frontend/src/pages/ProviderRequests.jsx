import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function ProviderRequests() {
  const [requests, setRequests] = useState([]);

  const fetchRequests = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.get("/provider-requests", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setRequests(response.data);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Only admin can view provider requests");
    }
  };

  const approveProvider = async (userId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.put(
        `/approve-provider/${userId}`,
        null,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
      fetchRequests();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to approve provider");
    }
  };

  useEffect(() => {
  const loadRequests = async () => {
    await fetchRequests();
  };

  loadRequests();
}, []);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">Provider Requests</h1>

        {requests.length === 0 ? (
          <div className="alert alert-info">
            No pending provider requests
          </div>
        ) : (
          <div className="row">
            {requests.map((request) => (
              <div className="col-md-4 mb-4" key={request.id}>
                <div className="card shadow p-3">
                  <h5>{request.name}</h5>

                  <p>
                    <strong>Email:</strong> {request.email}
                  </p>

                  <p>
                    <strong>Current Role:</strong> {request.role}
                  </p>

                  <p>
                    <strong>Status:</strong> {request.provider_status}
                  </p>

                  <button
                    className="btn btn-success"
                    onClick={() => approveProvider(request.id)}
                  >
                    Approve Provider
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProviderRequests;