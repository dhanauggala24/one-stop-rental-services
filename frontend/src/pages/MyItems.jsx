import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

const BACKEND_URL = "https://one-stop-rental-backend.onrender.com";

const getImageUrl = (imagePath) => {
  if (!imagePath) return "";
  if (imagePath.startsWith("http")) return imagePath;
  const cleanPath = imagePath.replaceAll("\\", "/").replace(/^\/+/, "");
  return `${BACKEND_URL}/${cleanPath}`;
};

function MyItems() {
  const [items, setItems] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState({});

  const fetchMyItems = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.get("/my-items", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setItems(response.data);
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to load my items");
    }
  };

  const deleteItem = async (itemId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.delete(`/delete-item/${itemId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert(response.data.message);
      fetchMyItems();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to delete item");
    }
  };

  const updateItem = async (item) => {
    const newTitle = prompt("Enter new title", item.title);
    const newDescription = prompt("Enter new description", item.description);
    const newPrice = prompt("Enter new price", item.price_per_day);
    const newLocation = prompt("Enter new location", item.location);

    if (!newTitle || !newDescription || !newPrice || !newLocation) {
      alert("All fields are required");
      return;
    }

    try {
      const token = localStorage.getItem("token");

      const response = await API.put(
        `/update-item/${item.id}`,
        {
          title: newTitle,
          description: newDescription,
          price_per_day: Number(newPrice),
          location: newLocation,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);
      fetchMyItems();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to update item");
    }
  };

  const uploadImage = async (itemId) => {
    try {
      const token = localStorage.getItem("token");
      const file = selectedFiles[itemId];

      if (!file) {
        alert("Please select an image first");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      const response = await API.post(
        `/upload-item-image/${itemId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert(response.data.message);
      fetchMyItems();
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Image upload failed");
    }
  };

  useEffect(() => {
    const loadItems = async () => {
      await fetchMyItems();
    };

    loadItems();
  }, []);

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-4">My Items</h1>

        {items.length === 0 ? (
          <p>No items created by you</p>
        ) : (
          <div className="row">
            {items.map((item) => (
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
                    <h5 className="card-title">{item.title}</h5>

                    <p className="card-text">{item.description}</p>

                    <p>
                      <strong>Location:</strong> {item.location}
                    </p>

                    <p>
                      <strong>₹{item.price_per_day}</strong> / day
                    </p>

                    <input
                      type="file"
                      className="form-control mb-2"
                      onChange={(e) =>
                        setSelectedFiles({
                          ...selectedFiles,
                          [item.id]: e.target.files[0],
                        })
                      }
                    />

                    <button
                      className="btn btn-secondary me-2 mb-2"
                      onClick={() => uploadImage(item.id)}
                    >
                      Upload Image
                    </button>

                    <button
                      className="btn btn-warning me-2 mb-2"
                      onClick={() => updateItem(item)}
                    >
                      Update
                    </button>

                    <button
                      className="btn btn-danger mb-2"
                      onClick={() => deleteItem(item.id)}
                    >
                      Delete
                    </button>
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

export default MyItems;