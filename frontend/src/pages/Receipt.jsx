import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api/axios";

function Receipt() {
  const { bookingId } = useParams();
  const [receipt, setReceipt] = useState(null);

  useEffect(() => {
    const loadReceipt = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await API.get(`/booking-receipt/${bookingId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setReceipt(response.data);
      } catch (error) {
        console.log(error.response?.data || error.message);
        alert("Failed to load receipt");
      }
    };

    loadReceipt();
  }, [bookingId]);

  if (!receipt) {
    return <div className="container mt-5">Loading receipt...</div>;
  }

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h2 className="text-center mb-4">Booking Receipt</h2>

        <p><strong>Booking ID:</strong> {receipt.booking_id}</p>
        <p><strong>Item:</strong> {receipt.item_title}</p>
        <p><strong>Location:</strong> {receipt.location}</p>
        <p><strong>Price / Day:</strong> ₹{receipt.price_per_day}</p>
        <p><strong>Start Date:</strong> {receipt.start_date}</p>
        <p><strong>End Date:</strong> {receipt.end_date}</p>
        <p><strong>Status:</strong> {receipt.status}</p>

        <div className="alert alert-success mt-3">
          Receipt verified successfully ✅
        </div>
      </div>
    </div>
  );
}

export default Receipt;