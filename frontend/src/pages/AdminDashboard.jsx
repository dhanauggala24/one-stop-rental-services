import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [pendingItems, setPendingItems] = useState([]);

  const fetchAdminStats = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.get("/admin-dashboard", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setStats(response.data);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Only admin can access this page");
    }
  };

  const fetchPendingItems = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.get("/pending-items", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPendingItems(response.data);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to load pending item requests");
    }
  };

  const approveItem = async (itemId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.put(
        `/approve-item/${itemId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
      fetchAdminStats();
      fetchPendingItems();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to approve item");
    }
  };

  const rejectItem = async (itemId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.put(
        `/reject-item/${itemId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
      fetchAdminStats();
      fetchPendingItems();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to reject item");
    }
  };

 useEffect(() => {
  const loadData = async () => {
    await fetchAdminStats();
    await fetchPendingItems();
  };

  loadData();
}, []);

  const bookings = stats?.bookings || [];

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">Admin Dashboard</h1>

        {!stats ? (
          <p>Loading...</p>
        ) : (
          <>
            <div className="row mb-4">
              <div className="col-md-3 mb-3">
                <div className="card shadow text-center p-4">
                  <h5>Total Users</h5>
                  <h2>{stats.total_users}</h2>
                </div>
              </div>

              <div className="col-md-3 mb-3">
                <div className="card shadow text-center p-4">
                  <h5>Total Items</h5>
                  <h2>{stats.total_items}</h2>
                </div>
              </div>

              <div className="col-md-3 mb-3">
                <div className="card shadow text-center p-4">
                  <h5>Total Bookings</h5>
                  <h2>{stats.total_bookings}</h2>
                </div>
              </div>

              <div className="col-md-3 mb-3">
                <div className="card shadow text-center p-4">
                  <h5>Pending Items</h5>
                  <h2>{stats.pending_items || 0}</h2>
                </div>
              </div>
            </div>

            <div className="card shadow p-4 mb-4">
              <h3 className="mb-3">Pending Item Requests</h3>

              {pendingItems.length === 0 ? (
                <div className="alert alert-info">
                  No pending item requests
                </div>
              ) : (
                <div className="table-responsive">
                  <table className="table table-bordered table-hover">
                    <thead className="table-dark">
                      <tr>
                        <th>Item ID</th>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Location</th>
                        <th>Price / Day</th>
                        <th>Requested By</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {pendingItems.map((item) => (
                        <tr key={item.item_id}>
                          <td>{item.item_id}</td>
                          <td>{item.title}</td>
                          <td>{item.category}</td>
                          <td>{item.location}</td>
                          <td>₹{item.price_per_day}</td>
                          <td>
                            {item.owner_name}
                            <br />
                            <small className="text-muted">
                              {item.owner_email}
                            </small>
                          </td>
                          <td>
                            <span className="badge bg-warning text-dark">
                              {item.approval_status}
                            </span>
                          </td>
                          <td>
                            <button
                              className="btn btn-success btn-sm me-2"
                              onClick={() => approveItem(item.item_id)}
                            >
                              Approve
                            </button>

                            <button
                              className="btn btn-danger btn-sm"
                              onClick={() => rejectItem(item.item_id)}
                            >
                              Reject
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            <div className="card shadow p-4">
              <h3 className="mb-3">All Rental Bookings</h3>

              <div className="table-responsive">
                <table className="table table-bordered table-hover">
                  <thead className="table-dark">
                    <tr>
                      <th>Booking ID</th>
                      <th>Item Owner</th>
                      <th>User Name</th>
                      <th>Item Name</th>
                      <th>Start Date</th>
                      <th>End Date</th>
                      <th>Price / Day</th>
                      <th>Total Cost</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {bookings.length === 0 ? (
                      <tr>
                        <td colSpan="9" className="text-center">
                          No bookings found
                        </td>
                      </tr>
                    ) : (
                      bookings.map((booking) => (
                        <tr key={booking.booking_id}>
                          <td>{booking.booking_id}</td>
                          <td>
                            {booking.item_owner_name ||
                              booking.provider_name ||
                              "Unknown"}
                          </td>
                          <td>{booking.user_name || "Unknown"}</td>
                          <td>{booking.item_name || "Unknown"}</td>
                          <td>{booking.start_date}</td>
                          <td>{booking.end_date}</td>
                          <td>₹{booking.price_per_day || 0}</td>
                          <td>₹{booking.total_cost || 0}</td>
                          <td>
                            <span
                              className={
                                booking.status === "approved"
                                  ? "badge bg-success"
                                  : booking.status === "rejected"
                                  ? "badge bg-danger"
                                  : "badge bg-warning text-dark"
                              }
                            >
                              {booking.status || "pending"}
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;