import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function ProviderBookings() {
  const [bookings, setBookings] = useState([]);

  const loadProviderBookings = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.get("/provider-bookings", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setBookings(response.data);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to load provider bookings");
    }
  };

  const updateStatus = async (bookingId, status) => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.put(
        `/update-booking-status/${bookingId}?status=${status}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);

      loadProviderBookings();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to update booking");
    }
  };

 useEffect(() => {
  const fetchData = async () => {
    await loadProviderBookings();
  };

  fetchData();
}, []);
  return (
    <div>
      <Navbar />

      <h1>Provider Bookings</h1>

      {bookings.length === 0 ? (
        <p>No booking requests found</p>
      ) : (
        bookings.map((booking) => (
          <div key={booking.id}>
            <h3>Booking #{booking.id}</h3>

            <p>Item ID: {booking.item_id}</p>

            <p>Renter ID: {booking.renter_id}</p>

            <p>Start Date: {booking.start_date}</p>

            <p>End Date: {booking.end_date}</p>

            <p>Status: {booking.status}</p>

            <button onClick={() => updateStatus(booking.id, "approved")}>
              Approve
            </button>

            <button onClick={() => updateStatus(booking.id, "rejected")}>
              Reject
            </button>

            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default ProviderBookings;