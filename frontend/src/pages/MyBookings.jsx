import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function MyBookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const loadBookings = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await API.get("/my-bookings", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setBookings(response.data);
      } catch (error) {
        console.log(error.response?.data || error.message);
        alert("Failed to load bookings");
      }
    };

    loadBookings();
  }, []);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">My Bookings</h1>

        {bookings.length === 0 ? (
          <div className="alert alert-info">No bookings found</div>
        ) : (
          <div className="row">
            {bookings.map((booking) => (
              <div className="col-md-4 mb-4" key={booking.booking_id}>
                <div className="card shadow h-100">
                  <div className="card-body">
                    <h5 className="card-title">
                      {booking.item_title}
                    </h5>

                    <p>
                      <strong>Booking ID:</strong> {booking.booking_id}
                    </p>

                    <p>
                      <strong>Location:</strong> {booking.location}
                    </p>

                    <p>
                      <strong>Start Date:</strong> {booking.start_date}
                    </p>

                    <p>
                      <strong>End Date:</strong> {booking.end_date}
                    </p>

                    <span
                      className={
                        booking.status === "approved"
                          ? "badge bg-success"
                          : booking.status === "rejected"
                          ? "badge bg-danger"
                          : "badge bg-warning text-dark"
                      }
                    >
                      {booking.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default MyBookings;