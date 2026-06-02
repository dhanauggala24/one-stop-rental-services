import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

const BACKEND_URL = "https://one-stop-rental-backend.onrender.com";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  const navigate = useNavigate();

  const getImageUrl = (imagePath) => {
    if (!imagePath) {
      return "";
    }

    if (imagePath.startsWith("http")) {
      return imagePath;
    }

    const cleanPath = imagePath.replaceAll("\\", "/").replace(/^\/+/, "");

    return `${BACKEND_URL}/${cleanPath}`;
  };

  const loadCart = async () => {
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

      let total = 0;

      response.data.forEach((item) => {
        total += item.total_price;
      });

      setTotalAmount(total);
    } catch (error) {
      console.log(error.response?.data || error.message);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        alert("Session expired. Please login again.");
        navigate("/login");
        return;
      }

      alert("Failed to load cart");
    }
  };

  const removeItem = async (cartId) => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Please login again");
        navigate("/login");
        return;
      }

      await API.delete(`/remove-from-cart/${cartId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      loadCart();
    } catch (error) {
      console.log(error.response?.data || error.message);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        alert("Session expired. Please login again.");
        navigate("/login");
        return;
      }

      alert("Failed to remove item");
    }
  };

  useEffect(() => {
    loadCart();
  }, []);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">My Cart</h1>

        {cartItems.length === 0 ? (
          <div className="alert alert-info">No items in cart</div>
        ) : (
          <>
            <div className="row">
              {cartItems.map((item) => (
                <div className="col-md-4 mb-4" key={item.cart_id}>
                  <div className="card shadow h-100">
                    {item.image && (
                      <img
                        src={getImageUrl(item.image)}
                        className="card-img-top"
                        alt={item.title}
                        style={{
                          height: "220px",
                          objectFit: "cover",
                        }}
                        onError={(e) => {
                          e.currentTarget.style.display = "none";
                        }}
                      />
                    )}

                    <div className="card-body">
                      <h5>{item.title}</h5>

                      <p>{item.description}</p>

                      <p>
                        <strong>Location:</strong> {item.location}
                      </p>

                      <p>
                        <strong>Start Date:</strong> {item.start_date}
                      </p>

                      <p>
                        <strong>End Date:</strong> {item.end_date}
                      </p>

                      <p>
                        <strong>Total:</strong> ₹{item.total_price}
                      </p>

                      <button
                        className="btn btn-danger"
                        onClick={() => removeItem(item.cart_id)}
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="card shadow p-4 mt-3">
              <h3>Grand Total : ₹{totalAmount}</h3>

              <button
                className="btn btn-success mt-3"
                onClick={() => navigate("/payment")}
              >
                Proceed To Payment
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Cart;