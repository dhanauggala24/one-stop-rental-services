import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

const BACKEND_URL = "https://one-stop-rental-backend.onrender.com";

function AllItems() {
  const location = useLocation();
  const navigate = useNavigate();

 const queryParams = new URLSearchParams(
  location.search || window.location.hash.split("?")[1] || ""
);

const categoryFromUrl = queryParams.get("category") || "All";
  const [items, setItems] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [dateInputs, setDateInputs] = useState({});

  const categories = [
    "All",
    "Property Rental",
    "PG & Hostel",
    "Vehicles",
    "Photography",
    "Equipment",
    "Camping",
  ];

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await API.get("/all-items");
        setItems(response.data);
      } catch (error) {
        console.log(error);
        alert("Failed to load items");
      }
    };

    fetchItems();
  }, []);

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

  const currentCategory = categoryFromUrl;

  const filteredItems = items.filter((item) => {
    const search = searchText.toLowerCase();

    const title = item.title?.toLowerCase() || "";
    const description = item.description?.toLowerCase() || "";
    const itemLocation = item.location?.toLowerCase() || "";
    const category = item.category || "";

    const matchesSearch =
      title.includes(search) ||
      description.includes(search) ||
      itemLocation.includes(search);

    const matchesCategory =
      currentCategory === "All" || category === currentCategory;

    return matchesSearch && matchesCategory;
  });

  const handleCategoryClick = (category) => {
    if (category === "All") {
      navigate("/items");
    } else {
      navigate(`/items?category=${encodeURIComponent(category)}`);
    }
  };

  const handleDateChange = (itemId, field, value) => {
    setDateInputs((prev) => ({
      ...prev,
      [itemId]: {
        ...prev[itemId],
        [field]: value,
      },
    }));
  };

  const addToCart = async (itemId) => {
    const itemDates = dateInputs[itemId] || {};
    const startDate = itemDates.startDate;
    const endDate = itemDates.endDate;

    if (!startDate || !endDate) {
      alert("Please select start date and end date for this item");
      return;
    }

    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Please login again");
        navigate("/login");
        return;
      }

      const response = await API.post(
        "/add-to-cart",
        {
          item_id: itemId,
          start_date: startDate,
          end_date: endDate,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
    } catch (error) {
      console.log(error.response?.data || error.message);

      const errorMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to add item to cart";

      if (
        errorMessage === "Invalid or expired token" ||
        error.response?.status === 401
      ) {
        localStorage.removeItem("token");
        alert("Session expired. Please login again.");
        navigate("/login");
        return;
      }

      alert(errorMessage);
    }
  };

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">
          {currentCategory === "All" ? "All Rental Items" : currentCategory}
        </h1>

        <div className="card shadow p-3 mb-4">
          <h4>Search by Location / Item</h4>

          <input
            type="text"
            className="form-control"
            placeholder="Search by item name, description, or location..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
        </div>

        <div className="card shadow p-3 mb-4">
          <h4>Filter by Category</h4>

          <div>
            {categories.map((category) => (
              <button
                key={category}
                className={
                  currentCategory === category
                    ? "btn btn-primary me-2 mb-2"
                    : "btn btn-outline-primary me-2 mb-2"
                }
                onClick={() => handleCategoryClick(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {filteredItems.length === 0 ? (
          <div className="alert alert-info">No matching items found</div>
        ) : (
          <div className="row">
            {filteredItems.map((item) => (
              <div className="col-md-4 mb-4" key={item.id}>
                <div className="card h-100 shadow">
                  {item.image && (
                    <img
                      src={getImageUrl(item.image)}
                      className="card-img-top"
                      alt={item.title}
                      style={{ height: "220px", objectFit: "cover" }}
                      onError={(e) => {
                        e.currentTarget.style.display = "none";
                      }}
                    />
                  )}

                  <div className="card-body">
                    <span className="badge bg-secondary mb-2">
                      {item.category}
                    </span>

                    <h5>{item.title}</h5>

                    <p>{item.description}</p>

                    <p>
                      <strong>Location:</strong> {item.location}
                    </p>

                    <p>
                      <strong>₹{item.price_per_day}</strong> / day
                    </p>

                    <div className="mb-2">
                      <label className="form-label">Start Date</label>
                      <input
                        type="date"
                        className="form-control"
                        value={dateInputs[item.id]?.startDate || ""}
                        onChange={(e) =>
                          handleDateChange(
                            item.id,
                            "startDate",
                            e.target.value
                          )
                        }
                      />
                    </div>

                    <div className="mb-3">
                      <label className="form-label">End Date</label>
                      <input
                        type="date"
                        className="form-control"
                        value={dateInputs[item.id]?.endDate || ""}
                        onChange={(e) =>
                          handleDateChange(
                            item.id,
                            "endDate",
                            e.target.value
                          )
                        }
                      />
                    </div>

                    <button
                      className="btn btn-primary me-2"
                      onClick={() => addToCart(item.id)}
                    >
                      Add To Cart
                    </button>

                    <a
                      className="btn btn-success"
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                        item.location || ""
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View Location
                    </a>
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

export default AllItems;