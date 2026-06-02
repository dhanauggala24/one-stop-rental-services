import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

const BACKEND_URL = "https://one-stop-rental-backend.onrender.com";

function Payment() {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [paymentSuccess, setPaymentSuccess] = useState(false);
  const [receipt, setReceipt] = useState(null);
  const [qrPath, setQrPath] = useState("");
  const [smsMessage, setSmsMessage] = useState("");
  const [smsResult, setSmsResult] = useState(null);

  const navigate = useNavigate();

  const getFileUrl = (filePath) => {
    if (!filePath) {
      return "";
    }

    if (filePath.startsWith("http")) {
      return filePath;
    }

    const cleanPath = filePath.replaceAll("\\", "/").replace(/^\/+/, "");

    return `${BACKEND_URL}/${cleanPath}`;
  };

  const loadCart = useCallback(async () => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Please login again");
        navigate("/login");
        return;
      }

      const response = await API.get("/my-cart", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setCartItems(response.data);

      const total = response.data.reduce(
        (sum, item) => sum + Number(item.total_price || 0),
        0
      );

      setTotalAmount(total);
    } catch (error) {
      console.log(error.response?.data || error.message);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        alert("Session expired. Please login again.");
        navigate("/login");
        return;
      }

      alert("Failed to load payment details");
    }
  }, [navigate]);

  const handlePayment = async () => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Please login again");
        navigate("/login");
        return;
      }

      const response = await API.post(
        "/confirm-payment",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setPaymentSuccess(true);
      setReceipt(response.data.receipt);
      setQrPath(response.data.qr_path);
      setSmsMessage(response.data.sms_message);
      setSmsResult(response.data.sms_result);

      alert("Payment Successful! QR generated and message process completed.");
    } catch (error) {
      console.log(error.response?.data || error.message);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        alert("Session expired. Please login again.");
        navigate("/login");
        return;
      }

      alert(
        error.response?.data?.detail ||
          JSON.stringify(error.response?.data) ||
          "Payment failed"
      );
    }
  };

  useEffect(() => {
    loadCart();
  }, [loadCart]);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">Payment Simulation</h1>

        {!paymentSuccess && cartItems.length === 0 ? (
          <div className="alert alert-info">No items found in cart</div>
        ) : (
          <>
            {!paymentSuccess && (
              <>
                <div className="card shadow p-4 mb-4">
                  <h3>Order Summary</h3>

                  {cartItems.map((item) => (
                    <div key={item.cart_id} className="border-bottom py-3">
                      <h5>{item.title}</h5>

                      <p className="mb-1">
                        <strong>Location:</strong> {item.location}
                      </p>

                      <p className="mb-1">
                        <strong>Dates:</strong> {item.start_date} to{" "}
                        {item.end_date}
                      </p>

                      <p className="mb-1">
                        <strong>Total:</strong> ₹{item.total_price}
                      </p>
                    </div>
                  ))}

                  <h3 className="mt-4">Grand Total: ₹{totalAmount}</h3>
                </div>

                <div className="card shadow p-4">
                  <h3>Select Payment Method</h3>

                  <div className="form-check mt-3">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="payment"
                      defaultChecked
                    />
                    <label className="form-check-label">UPI</label>
                  </div>

                  <div className="form-check mt-2">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="payment"
                    />
                    <label className="form-check-label">Card</label>
                  </div>

                  <div className="form-check mt-2">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="payment"
                    />
                    <label className="form-check-label">Cash on Delivery</label>
                  </div>

                  <button
                    className="btn btn-success mt-4"
                    onClick={handlePayment}
                  >
                    Pay Now
                  </button>
                </div>
              </>
            )}

            {paymentSuccess && receipt && (
              <div className="card shadow p-4 mt-4">
                <div className="alert alert-success">
                  Payment Successful ✅
                </div>

                <h3>Booking Receipt</h3>

                <p>
                  <strong>User Name:</strong> {receipt.user_name}
                </p>

                <p>
                  <strong>Email:</strong> {receipt.email}
                </p>

                <p>
                  <strong>Phone Number:</strong> {receipt.phone_number}
                </p>

                <h5 className="mt-4">Booked Items</h5>

                {receipt.items.map((item) => (
                  <div key={item.booking_id} className="border rounded p-3 mb-3">
                    <p>
                      <strong>Booking ID:</strong> {item.booking_id}
                    </p>

                    <p>
                      <strong>Item:</strong> {item.item_name}
                    </p>

                    <p>
                      <strong>Location:</strong> {item.location}
                    </p>

                    <p>
                      <strong>Dates:</strong> {item.start_date} to{" "}
                      {item.end_date}
                    </p>

                    <p>
                      <strong>Total:</strong> ₹{item.total_price}
                    </p>
                  </div>
                ))}

                <h4>Total Paid: ₹{receipt.total_amount}</h4>

                {qrPath && (
                  <div className="mt-4 text-center">
                    <h4>Booking QR Code</h4>

                    <img
                      src={getFileUrl(qrPath)}
                      alt="Booking QR"
                      style={{
                        width: "250px",
                        height: "250px",
                        objectFit: "contain",
                      }}
                    />
                  </div>
                )}

                {smsMessage && (
                  <div className="alert alert-info mt-4">📩 {smsMessage}</div>
                )}

                {smsResult && (
                  <div
                    className={
                      smsResult.success
                        ? "alert alert-success mt-3"
                        : "alert alert-danger mt-3"
                    }
                  >
                    <strong>Message API Status:</strong>{" "}
                    {smsResult.success ? "Sent Successfully" : "Failed"}
                    <br />
                    <small>
                      {JSON.stringify(smsResult.response || smsResult.message)}
                    </small>
                  </div>
                )}

                <button
                  className="btn btn-primary mt-3"
                  onClick={() => navigate("/my-bookings")}
                >
                  Go To My Bookings
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Payment;